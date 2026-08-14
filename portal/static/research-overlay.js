(() => {
  "use strict";

  const API_BASE =
    window.__CANTON_RESEARCH_API__ ||
    window.sessionStorage.getItem("canton-research-api") ||
    "http://127.0.0.1:8787";
  const MERMAID_FALLBACK_URL =
    "https://cdn.jsdelivr.net/npm/mermaid@11.16.1/dist/mermaid.min.js";
  const MERMAID_FALLBACK_INTEGRITY =
    "sha384-aBQXj4hK6Jm05i7aQAsUV3bLdSUrHX1BGYfMB0166TtWt/RRaw+h0Eelme9OCOvy";
  const DOCUMENT_NAVIGATION_FALLBACK_MS = 1500;
  const PROGRESS_ORDER = ["unreviewed", "complete"];
  const PROGRESS_DISPLAY = {
    unreviewed: { icon: "", label: "Unreviewed" },
    complete: { icon: "✓", label: "Complete" },
    excluded: { icon: "✕", label: "Excluded from scope" },
  };
  const state = {
    statusByPath: new Map(),
    activePath: null,
    favoritesNavigationSignature: null,
    commentsNavigationSignature: null,
    comments: [],
    commentAnchors: [],
    commentData: null,
    commentDraft: null,
    selectedCommentTarget: null,
    refreshTimer: null,
    navigationFallbackTimer: null,
    commentDraftTimer: null,
    commentHoverTimer: null,
    mermaidTimer: null,
    mermaidPromise: null,
    mermaidRenderId: 0,
  };

  function decodeMermaidSource(encoded) {
    const bytes = Uint8Array.from(window.atob(encoded), (character) =>
      character.charCodeAt(0)
    );
    return new TextDecoder().decode(bytes);
  }

  function mermaidTarget(marker) {
    let candidate = marker.nextElementSibling;
    while (candidate && !candidate.matches("h1, h2, h3, h4, h5, h6")) {
      if (candidate.matches(".mermaid")) return candidate;
      const nested = candidate.querySelector(".mermaid");
      if (nested) return nested;
      if (candidate.matches("[data-research-mermaid-source]")) return null;
      candidate = candidate.nextElementSibling;
    }
    return null;
  }

  function loadMermaidFallback() {
    if (window.mermaid?.render) return Promise.resolve(window.mermaid);
    if (state.mermaidPromise) return state.mermaidPromise;

    state.mermaidPromise = new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = MERMAID_FALLBACK_URL;
      script.integrity = MERMAID_FALLBACK_INTEGRITY;
      script.crossOrigin = "anonymous";
      script.dataset.researchMermaidFallback = "true";
      script.onload = () => {
        if (window.mermaid?.render) resolve(window.mermaid);
        else reject(new Error("Mermaid fallback loaded without a renderer"));
      };
      script.onerror = () => reject(new Error("Unable to load the Mermaid fallback"));
      document.head.append(script);
    });
    return state.mermaidPromise;
  }

  async function renderMissingMermaid() {
    const markers = [...document.querySelectorAll("[data-research-mermaid-source]")];
    const pending = markers.filter((marker) => {
      const target = mermaidTarget(marker);
      return target && !target.querySelector("svg");
    });
    if (!pending.length) return;

    let renderer;
    try {
      renderer = await loadMermaidFallback();
    } catch (error) {
      console.warn("Mermaid fallback unavailable", error);
      for (const marker of pending) {
        const target = mermaidTarget(marker);
        if (!target || target.querySelector("svg")) continue;
        target.classList.add("research-mermaid-error");
        target.textContent = "Diagram unavailable. Check the network connection and reload.";
      }
      return;
    }

    const theme = document.documentElement.classList.contains("dark") ? "dark" : "default";
    renderer.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      fontFamily: "inherit",
      theme,
      suppressErrorRendering: true,
    });

    for (const marker of pending) {
      const target = mermaidTarget(marker);
      if (!target || target.querySelector("svg")) continue;
      try {
        const chart = decodeMermaidSource(marker.dataset.researchMermaidSource || "");
        const id = `research-mermaid-${Date.now()}-${++state.mermaidRenderId}`;
        const { svg } = await renderer.render(id, chart);
        if (!marker.isConnected || !target.isConnected || target.querySelector("svg")) continue;
        target.innerHTML = svg;
        target.classList.remove("research-mermaid-error");
        target.dataset.researchMermaidFallback = "true";
        target.setAttribute("role", "img");
        target.setAttribute("aria-label", "Mermaid diagram");
      } catch (error) {
        console.warn("Unable to render Mermaid diagram", error);
        target.classList.add("research-mermaid-error");
        target.textContent = "This diagram could not be rendered.";
      }
    }
  }

  function scheduleMermaidFallback() {
    window.clearTimeout(state.mermaidTimer);
    state.mermaidTimer = window.setTimeout(renderMissingMermaid, 1200);
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function canonicalPath(value = window.location.pathname) {
    const url = new URL(value, window.location.origin);
    let path = url.pathname.replace(/^\/+|\/+$/g, "");
    if (path.startsWith("ko/")) path = path.slice(3);
    return path.replace(/\.(?:mdx?|html)$/i, "") || "index";
  }

  async function request(path, options = {}) {
    const response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(payload.error || `Request failed: ${response.status}`);
    return payload;
  }

  function normalizeProgress(current) {
    return PROGRESS_ORDER.includes(current) ? current : "unreviewed";
  }

  async function setProgress(item, status) {
    await request(`/api/progress/${encodeURIComponent(item.source_id)}`, {
      method: "PUT",
      body: JSON.stringify({ status }),
    });
    item.progress = status;
    decorateNavigation();
    const currentControl = document.querySelector("[data-page-progress-control]");
    if (currentControl) updateProgressControl(currentControl, item);
  }

  function updateProgressControl(control, item) {
    const status = item.scope === "excluded" ? "excluded" : normalizeProgress(item.progress);
    const display = PROGRESS_DISPLAY[status];
    if (control.textContent !== display.icon) control.textContent = display.icon;
    control.dataset.status = status;
    control.title = display.label;
    control.setAttribute(
      "aria-label",
      `${display.label}. Activate to change the document status.`
    );
  }

  function updateFavoriteControl(control, item) {
    const favorite = Boolean(item.favorite);
    const label = favorite ? "Favorite" : "Not a favorite";
    const icon = favorite ? "★" : "☆";
    if (control.textContent !== icon) {
      control.textContent = icon;
    }
    control.dataset.favorite = String(favorite);
    control.title = favorite
      ? `${label}. Click to remove from Favorites.`
      : `${label}. Click to add to Favorites.`;
    control.setAttribute("aria-label", control.title);
  }

  async function setScope(item, scope, reason = "") {
    const research = await request(`/api/pages/${encodeURIComponent(item.source_id)}/scope`, {
      method: "PUT",
      body: JSON.stringify({
        scope,
        reason,
        base_file_sha256: item.research_file_sha256 || null,
      }),
    });
    Object.assign(item, {
      scope: research.scope,
      scope_reason: research.scope_reason,
      scope_category: research.scope_category,
      scope_category_label: research.scope_category_label,
      scope_source: research.scope_source,
      research_file_sha256: research.file_sha256,
    });
  }

  async function setFavorite(item, favorite) {
    const payload = await request(`/api/favorites/${encodeURIComponent(item.source_id)}`, {
      method: "PUT",
      body: JSON.stringify({ favorite }),
    });
    item.favorite = payload.favorite;
  }

  async function toggleFavorite(item, control) {
    control.dataset.busy = "true";
    control.setAttribute("aria-busy", "true");
    try {
      await setFavorite(item, !item.favorite);
      state.favoritesNavigationSignature = null;
      renderFavoritesNavigation();
      decorateNavigation();
      if (canonicalPath() === item.path || canonicalPath() === "research/favorites") {
        await refreshCurrentPage(true);
      }
    } catch (error) {
      console.warn("Unable to update page navigation state", error);
      window.alert(`Page state update failed: ${error.message}`);
    } finally {
      if (control.isConnected) {
        control.removeAttribute("aria-busy");
        delete control.dataset.busy;
      }
    }
  }

  async function cycleDocumentStatus(item, control) {
    if (control.dataset.busy === "true") return;
    control.dataset.busy = "true";
    control.setAttribute("aria-busy", "true");
    try {
      if (item.scope === "excluded") {
        await setScope(item, "included");
        await setProgress(item, "unreviewed");
      } else if (normalizeProgress(item.progress) === "complete") {
        const reason = window.prompt(
          "Reason for excluding this page from the current scope:",
          ""
        );
        if (!reason) return;
        await setProgress(item, "unreviewed");
        await setScope(item, "excluded", reason);
      } else {
        await setProgress(item, "complete");
      }
      decorateNavigation();
      if (canonicalPath() === item.path) await refreshCurrentPage(true);
    } catch (error) {
      console.warn("Unable to update document status", error);
      window.alert(`Document status update failed: ${error.message}`);
    } finally {
      if (control.isConnected) {
        control.removeAttribute("aria-busy");
        delete control.dataset.busy;
      }
    }
  }

  function decorateNavigation() {
    if (!state.statusByPath.size) return;
    document.querySelectorAll("aside a[href], nav a[href]").forEach((link) => {
      if (link.closest("main")) return;
      const item = state.statusByPath.get(canonicalPath(link.href));
      if (!item) return;

      let favoriteControl = link.querySelector(".research-nav-favorite");
      if (!favoriteControl) {
        favoriteControl = document.createElement("span");
        favoriteControl.className = "research-nav-favorite";
        favoriteControl.setAttribute("role", "button");
        favoriteControl.setAttribute("tabindex", "0");
        link.prepend(favoriteControl);
      }
      updateFavoriteControl(favoriteControl, item);
      const changeFavorite = async (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (favoriteControl.dataset.busy === "true") return;
        await toggleFavorite(item, favoriteControl);
      };
      favoriteControl.onclick = changeFavorite;
      favoriteControl.onkeydown = (event) => {
        if (event.key === "Enter" || event.key === " ") changeFavorite(event);
      };

      let marker = link.querySelector(".research-nav-marker");
      if (!marker) {
        marker = document.createElement("span");
        marker.className = "research-nav-marker";
        link.append(marker);
      }

      updateProgressControl(marker, item);
      if (item.scope === "excluded") {
        link.classList.add("research-nav-excluded");
      } else {
        link.classList.remove("research-nav-excluded");
      }
      marker.setAttribute("role", "button");
      marker.setAttribute("tabindex", "0");
      link.removeAttribute("title");
      const advance = async (event) => {
        event.preventDefault();
        event.stopPropagation();
        await cycleDocumentStatus(item, marker);
      };
      marker.onclick = advance;
      marker.onkeydown = (event) => {
        if (event.key === "Enter" || event.key === " ") advance(event);
      };
    });
  }

  function favoritesLanguage() {
    const requested = new URLSearchParams(window.location.search).get("lang");
    return requested === "ko" || window.location.pathname.startsWith("/ko/")
      ? "ko"
      : "en";
  }

  function favoriteDocumentHref(item) {
    return favoritesLanguage() === "ko" && item.translation_available
      ? `/ko/${item.path}`
      : `/${item.path}`;
  }

  function decorateFavoritesHeaderLink() {
    const themeButton = [...document.querySelectorAll("header button")].find((button) =>
      /change theme preference/i.test(
        `${button.getAttribute("aria-label") || ""} ${button.getAttribute("title") || ""}`
      )
    );
    if (!themeButton?.parentElement) return;

    let link = document.querySelector(".research-favorites-header-link");
    if (!link) {
      link = document.createElement("a");
      link.className = "research-favorites-header-link";
      link.innerHTML = '<span aria-hidden="true">★</span><span>Favorites</span>';
      themeButton.parentElement.insertBefore(link, themeButton);
    }
    const language = favoritesLanguage();
    link.href = `/research/favorites${language === "ko" ? "?lang=ko" : ""}`;
    link.setAttribute("aria-label", "Open Favorites");
    if (canonicalPath() === "research/favorites") link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");

    let commentsLink = document.querySelector(".research-comments-header-link");
    if (!commentsLink) {
      commentsLink = document.createElement("a");
      commentsLink.className = "research-comments-header-link";
      commentsLink.innerHTML = '<span aria-hidden="true">💬</span><span>Comments</span>';
      themeButton.parentElement.insertBefore(commentsLink, themeButton);
    }
    commentsLink.href = `/research/comments${language === "ko" ? "?lang=ko" : ""}`;
    commentsLink.setAttribute("aria-label", "Open Comments");
    if (canonicalPath() === "research/comments") {
      commentsLink.setAttribute("aria-current", "page");
    } else {
      commentsLink.removeAttribute("aria-current");
    }
  }

  function renderFavoritesNavigation() {
    if (canonicalPath() !== "research/favorites") return;
    const navigation = document.querySelector('nav[aria-label="Pages"]');
    if (!navigation || !state.statusByPath.size) return;

    const favorites = [...state.statusByPath.values()]
      .filter((item) => item.favorite)
      .sort((left, right) => left.title.localeCompare(right.title));
    const signature = `${favoritesLanguage()}:${favorites
      .map((item) => item.source_id)
      .join(",")}`;
    if (state.favoritesNavigationSignature === signature) return;
    state.favoritesNavigationSignature = signature;

    navigation.innerHTML = `<div class="research-favorites-navigation">
      <div class="research-favorites-navigation-heading">
        <span aria-hidden="true">★</span>
        <h3>Favorites</h3>
        <span>${favorites.length}</span>
      </div>
      ${
        favorites.length
          ? `<ul>${favorites
              .map(
                (item) => `<li><a class="research-favorite-navigation-link" href="${escapeHtml(
                  favoriteDocumentHref(item)
                )}" data-favorite-document-link><span>${escapeHtml(item.title)}</span></a></li>`
              )
              .join("")}</ul>`
          : '<p class="research-favorites-navigation-empty">No favorite pages yet.</p>'
      }
    </div>`;
    navigation.querySelectorAll("[data-favorite-document-link]").forEach((link) => {
      link.onclick = (event) => {
        event.preventDefault();
        window.location.assign(link.href);
      };
    });
  }

  function commentDisplayTitle(item) {
    return favoritesLanguage() === "ko" && item.translated_title
      ? item.translated_title
      : item.title;
  }

  function commentDocumentHref(item) {
    const prefix = item.language === "ko" && item.translation_available ? "/ko" : "";
    return `${prefix}/${item.source_path}?comment=${encodeURIComponent(item.comment_id)}`;
  }

  function groupedComments(comments) {
    const groups = new Map();
    for (const comment of comments) {
      if (!groups.has(comment.source_id)) {
        groups.set(comment.source_id, {
          source_id: comment.source_id,
          source_path: comment.source_path,
          title: comment.title,
          translated_title: comment.translated_title,
          comments: [],
        });
      }
      groups.get(comment.source_id).comments.push(comment);
    }
    return [...groups.values()].sort((left, right) =>
      commentDisplayTitle(left).localeCompare(commentDisplayTitle(right))
    );
  }

  function renderCommentsNavigation() {
    if (canonicalPath() !== "research/comments") return;
    const navigation = document.querySelector('nav[aria-label="Pages"]');
    if (!navigation) return;
    const groups = groupedComments(state.comments);
    const signature = `${favoritesLanguage()}:${groups
      .map((group) => `${group.source_id}:${group.comments.length}`)
      .join(",")}`;
    if (state.commentsNavigationSignature === signature) return;
    state.commentsNavigationSignature = signature;
    navigation.innerHTML = `<div class="research-comments-navigation">
      <div class="research-comments-navigation-heading">
        <span aria-hidden="true">💬</span>
        <h3>Comments</h3>
        <span>${state.comments.length}</span>
      </div>
      ${
        groups.length
          ? `<ul>${groups
              .map(
                (group) => `<li><a class="research-comment-navigation-link" href="#comment-page-${escapeHtml(
                  group.source_id.toLowerCase()
                )}"><span>${escapeHtml(commentDisplayTitle(group))}</span><small>${
                  group.comments.length
                }</small></a></li>`
              )
              .join("")}</ul>`
          : '<p class="research-comments-navigation-empty">No shared comments yet.</p>'
      }
    </div>`;
  }

  function localizeKoreanDocumentLinks() {
    if (!window.location.pathname.startsWith("/ko/")) return;
    document.querySelectorAll("main a[href]").forEach((link) => {
      if (link.closest("#research-summary-panel")) return;
      const rawHref = link.getAttribute("href");
      if (!rawHref || rawHref.startsWith("#")) return;

      const target = new URL(rawHref, window.location.href);
      if (target.origin !== window.location.origin || target.pathname.startsWith("/ko/")) {
        return;
      }
      const item = state.statusByPath.get(canonicalPath(target.pathname));
      if (!item?.translation_available) return;

      target.pathname = `/ko/${item.path}`;
      const localizedHref = `${target.pathname}${target.search}${target.hash}`;
      link.setAttribute("href", localizedHref);
      link.dataset.researchLocalizedHref = localizedHref;
    });
  }

  function preserveKoreanDocumentNavigation(event) {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return;
    }
    if (event.target.closest?.(".research-nav-favorite, .research-nav-marker")) return;
    const link = event.target.closest?.("a[data-research-localized-href]");
    if (!link || link.target === "_blank" || link.hasAttribute("download")) return;

    event.preventDefault();
    event.stopImmediatePropagation();
    window.location.assign(link.dataset.researchLocalizedHref);
  }

  function hasReadyDocumentPrefetch(target) {
    return window.performance.getEntriesByType("resource").some((entry) => {
      const resource = new URL(entry.name, window.location.href);
      return (
        resource.origin === target.origin &&
        resource.pathname === target.pathname &&
        resource.searchParams.has("_rsc") &&
        entry.responseEnd > 0
      );
    });
  }

  function recoverSlowDocumentNavigation(event) {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey ||
      event.target.closest?.(".research-nav-favorite, .research-nav-marker")
    ) {
      return;
    }
    const link = event.target.closest?.("a[href]");
    if (!link || link.target === "_blank" || link.hasAttribute("download")) return;
    if (link.dataset.researchLocalizedHref) return;
    if (!link.closest('nav[aria-label="Pages"], nav[aria-label="Pagination"]')) {
      return;
    }

    const target = new URL(link.href, window.location.href);
    const currentPath = canonicalPath(window.location.pathname);
    const targetPath = canonicalPath(target.pathname);
    if (
      target.origin !== window.location.origin ||
      !targetPath ||
      targetPath === currentPath
    ) {
      return;
    }

    if (!hasReadyDocumentPrefetch(target)) {
      event.preventDefault();
      event.stopImmediatePropagation();
      window.location.assign(target.href);
      return;
    }

    window.clearTimeout(state.navigationFallbackTimer);
    state.navigationFallbackTimer = window.setTimeout(() => {
      state.navigationFallbackTimer = null;
      if (canonicalPath(window.location.pathname) === currentPath) {
        window.location.assign(target.href);
      }
    }, DOCUMENT_NAVIGATION_FALLBACK_MS);
  }

  function articleRoot() {
    return document.querySelector("article") || document.querySelector("main");
  }

  function summaryBadge(research) {
    if (research.stale) return '<span class="research-badge stale">Stale</span>';
    const status = research.summary_status || "missing";
    return `<span class="research-badge ${escapeHtml(status)}">${escapeHtml(
      status.replaceAll("_", " ")
    )}</span>`;
  }

  function scopeBadge(research) {
    if (research.scope !== "excluded") return "";
    const reason = research.scope_reason || "Excluded from the current public testnet scope";
    return `<a class="research-scope-badge" href="/research/scope" title="${escapeHtml(
      reason
    )}"><span aria-hidden="true">✕</span> Out of testnet scope</a>`;
  }

  function relatedRecords(data) {
    const claims = data.related_claims || [];
    const questions = data.related_questions || [];
    if (!claims.length && !questions.length) return "";
    return `
      <div class="research-related">
        <strong>Related evidence</strong>
        <div>${claims
          .map(
            (item) =>
              `<a href="/research/claims#${escapeHtml(item.id.toLowerCase())}">${escapeHtml(
                item.id
              )}</a>`
          )
          .join(" ")}${questions
      .map(
        (item) =>
          `<a href="/research/questions#${escapeHtml(item.id.toLowerCase())}">${escapeHtml(
            item.id
          )}</a>`
      )
      .join(" ")}</div>
      </div>`;
  }

  function selectedEvidence(root, data) {
    const selection = window.getSelection();
    const quote = selection?.toString().trim() || "";
    const node = selection?.anchorNode;
    const element = node?.nodeType === Node.ELEMENT_NODE ? node : node?.parentElement;
    if (
      !quote ||
      !element ||
      !root.contains(element) ||
      element.closest("#research-summary-panel")
    ) {
      throw new Error("Select text in the official document before capturing evidence");
    }
    const heading = [...root.querySelectorAll("h1, h2, h3, h4")]
      .filter(
        (item) =>
          item === element ||
          Boolean(item.compareDocumentPosition(element) & Node.DOCUMENT_POSITION_FOLLOWING)
      )
      .at(-1);
    return {
      quote,
      heading: heading?.textContent?.trim() || data.title,
      source_id: data.source_id,
      title: data.title,
      source_url: data.source_url,
    };
  }

  const COMMENT_BLOCK_SELECTOR =
    'p, li, td, th, pre, blockquote, [data-as="p"], [data-as="blockquote"]';
  const COMMENT_EXCLUDED_SELECTOR = [
    "#research-summary-panel",
    "[data-research-comment-ui]",
    "button",
    "input",
    "textarea",
    "select",
    "script",
    "style",
    "noscript",
    "nav",
    "footer",
  ].join(", ");

  function currentDocumentLanguage() {
    return window.location.pathname.startsWith("/ko/") ? "ko" : "en";
  }

  function currentDocumentSha(data) {
    return currentDocumentLanguage() === "ko"
      ? data.translation?.file_sha256
      : data.research?.source_sha256;
  }

  function commentTextIndex(root = articleRoot()) {
    if (!root) return { text: "", entries: [] };
    const entries = [];
    let text = "";
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        const parent = node.parentElement;
        if (!parent || !node.data || parent.closest(COMMENT_EXCLUDED_SELECTOR)) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    while (walker.nextNode()) {
      const node = walker.currentNode;
      const start = text.length;
      const rawOffsets = [];
      let normalized = "";
      for (let offset = 0; offset < node.data.length; offset += 1) {
        if (/[\u200B-\u200D\uFEFF]/.test(node.data[offset])) continue;
        rawOffsets.push(offset);
        normalized += node.data[offset];
      }
      rawOffsets.push(node.data.length);
      text += normalized;
      entries.push({ node, start, end: text.length, rawOffsets });
    }
    return { text, entries };
  }

  function commentHeading(root, element, fallback) {
    const headings = [...root.querySelectorAll("h1, h2, h3, h4, h5, h6")].filter(
      (heading) => !heading.closest(COMMENT_EXCLUDED_SELECTOR)
    );
    return (
      headings
        .filter(
          (heading) =>
            heading === element ||
            Boolean(heading.compareDocumentPosition(element) & Node.DOCUMENT_POSITION_FOLLOWING)
        )
        .at(-1)
        ?.textContent?.replace(/[\u200B-\u200D\uFEFF]/g, "").trim() || fallback
    );
  }

  function selectionBoundary(entries, node, offset, boundary) {
    if (node.nodeType !== Node.TEXT_NODE) return null;
    const entry = entries.find((candidate) => candidate.node === node);
    if (!entry || offset < 0 || offset > node.data.length) return null;
    const normalizedOffset = node.data
      .slice(0, offset)
      .replace(/[\u200B-\u200D\uFEFF]/g, "").length;
    const position = entry.start + normalizedOffset;
    if (boundary === "start" && position === entry.end && offset > 0) return position;
    if (boundary === "end" && position === entry.start && offset === 0) return position;
    return position;
  }

  function selectionOnlyExtendsPastBlock(range, block) {
    const clipped = range.cloneRange();
    try {
      clipped.setEndAfter(block);
    } catch (_error) {
      return false;
    }
    const visibleText = (value) => value.replace(/[\u200B-\u200D\uFEFF]/g, "").trim();
    return visibleText(range.toString()) === visibleText(clipped.toString());
  }

  function blockEndPosition(entries, block) {
    return entries.filter((entry) => block.contains(entry.node)).at(-1)?.end ?? null;
  }

  function selectorFromSelection(data) {
    const root = articleRoot();
    const selection = window.getSelection();
    if (!root || !selection || selection.rangeCount !== 1 || selection.isCollapsed) {
      throw new Error("Select a sentence or paragraph first");
    }
    const range = selection.getRangeAt(0);
    const startElement =
      range.startContainer.nodeType === Node.ELEMENT_NODE
        ? range.startContainer
        : range.startContainer.parentElement;
    const endElement =
      range.endContainer.nodeType === Node.ELEMENT_NODE
        ? range.endContainer
        : range.endContainer.parentElement;
    if (!startElement || !endElement || !root.contains(startElement) || !root.contains(endElement)) {
      throw new Error("Select text inside the document body");
    }
    const startBlock = startElement.closest(COMMENT_BLOCK_SELECTOR);
    const endBlock = endElement.closest(COMMENT_BLOCK_SELECTOR);
    const clampEndToStartBlock =
      Boolean(startBlock) && startBlock !== endBlock && selectionOnlyExtendsPastBlock(range, startBlock);
    if (
      startElement.closest(COMMENT_EXCLUDED_SELECTOR) ||
      (!clampEndToStartBlock && endElement.closest(COMMENT_EXCLUDED_SELECTOR))
    ) {
      throw new Error("Comments can only be attached to official document text");
    }
    if (!startBlock || (startBlock !== endBlock && !clampEndToStartBlock)) {
      throw new Error("Keep the selection inside one paragraph, list item, table cell, or code block");
    }

    const index = commentTextIndex(root);
    const start = selectionBoundary(index.entries, range.startContainer, range.startOffset, "start");
    const end = clampEndToStartBlock
      ? blockEndPosition(index.entries, startBlock)
      : selectionBoundary(index.entries, range.endContainer, range.endOffset, "end");
    if (start === null || end === null || end <= start) {
      throw new Error("This selection cannot be anchored reliably. Select plain text and try again");
    }
    const exact = index.text.slice(start, end);
    if (!exact.trim()) throw new Error("Select visible text before adding a comment");
    if (exact.length > 4000) throw new Error("Select no more than 4000 characters");
    return {
      type: "TextQuoteSelector",
      exact,
      prefix: index.text.slice(Math.max(0, start - 96), start),
      suffix: index.text.slice(end, end + 96),
      start,
      end,
      heading: commentHeading(root, startBlock, data.title),
    };
  }

  function boundaryForPosition(entries, position, kind) {
    if (kind === "start") {
      const entry = entries.find((candidate) => position >= candidate.start && position < candidate.end);
      return entry
        ? { node: entry.node, offset: entry.rawOffsets[position - entry.start] }
        : null;
    }
    const entry = entries.find((candidate) => position > candidate.start && position <= candidate.end);
    return entry
      ? { node: entry.node, offset: entry.rawOffsets[position - entry.start] }
      : null;
  }

  function rangeFromOffsets(index, start, end) {
    const first = boundaryForPosition(index.entries, start, "start");
    const last = boundaryForPosition(index.entries, end, "end");
    if (!first || !last) return null;
    const range = document.createRange();
    try {
      range.setStart(first.node, first.offset);
      range.setEnd(last.node, last.offset);
    } catch (_error) {
      return null;
    }
    return range.collapsed ? null : range;
  }

  function quoteCandidateOffsets(text, selector) {
    const candidates = [];
    let position = text.indexOf(selector.exact);
    while (position !== -1) {
      const prefix = text.slice(Math.max(0, position - selector.prefix.length), position);
      const end = position + selector.exact.length;
      const suffix = text.slice(end, end + selector.suffix.length);
      if (
        (!selector.prefix || prefix.endsWith(selector.prefix)) &&
        (!selector.suffix || suffix.startsWith(selector.suffix))
      ) {
        candidates.push({ start: position, end });
      }
      position = text.indexOf(selector.exact, position + 1);
    }
    return candidates;
  }

  function restoreCommentRange(index, selector) {
    const positioned = index.text.slice(selector.start, selector.end);
    if (positioned === selector.exact) {
      return rangeFromOffsets(index, selector.start, selector.end);
    }
    const candidates = quoteCandidateOffsets(index.text, selector);
    return candidates.length === 1
      ? rangeFromOffsets(index, candidates[0].start, candidates[0].end)
      : null;
  }

  function clearCommentHighlight() {
    if (window.CSS?.highlights) {
      CSS.highlights.delete("research-comments");
    }
    state.commentAnchors = [];
    document.querySelectorAll("[data-research-comment-ui]").forEach((element) => element.remove());
    window.clearTimeout(state.commentDraftTimer);
    state.commentDraftTimer = null;
    state.selectedCommentTarget = null;
  }

  function applyCommentHighlight() {
    if (!window.CSS?.highlights || typeof window.Highlight !== "function") return;
    CSS.highlights.set(
      "research-comments",
      new Highlight(...state.commentAnchors.map((anchor) => anchor.range))
    );
  }

  function commentAtPoint(x, y) {
    return state.commentAnchors.find((anchor) =>
      [...anchor.range.getClientRects()].some(
        (rect) => x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom
      )
    );
  }

  function positionFloating(element, rect, width = 320) {
    const left = Math.min(
      Math.max(12, rect.left + rect.width / 2 - width / 2),
      Math.max(12, window.innerWidth - width - 12)
    );
    const above = rect.top - element.offsetHeight - 10;
    element.style.left = `${left}px`;
    element.style.top = `${above > 10 ? above : Math.min(window.innerHeight - 12, rect.bottom + 10)}px`;
  }

  function removeCommentPopover() {
    document.querySelector(".research-comment-popover")?.remove();
  }

  function handleCommentEscape(event) {
    if (event.key !== "Escape" || !document.querySelector(".research-comment-popover")) return;
    window.clearTimeout(state.commentHoverTimer);
    removeCommentPopover();
  }

  function showCommentPopover(anchor, rect = null) {
    removeCommentPopover();
    const comment = anchor.comment;
    const popover = document.createElement("aside");
    popover.className = "research-comment-popover";
    popover.dataset.researchCommentUi = "true";
    popover.setAttribute("role", "dialog");
    popover.setAttribute("aria-label", "Document comment");
    popover.innerHTML = `
      <div class="research-comment-popover-meta">
        <span>${escapeHtml(comment.heading)}</span>
        ${comment.stale ? '<span class="research-comment-state">Source changed</span>' : ""}
      </div>
      <blockquote>${escapeHtml(comment.selector.exact)}</blockquote>
      <p>${escapeHtml(comment.content)}</p>
      <footer>
        <time datetime="${escapeHtml(comment.updated_at)}">${escapeHtml(
          new Date(comment.updated_at).toLocaleString()
        )}</time>
        <span class="research-comment-popover-actions">
          <button type="button" data-comment-edit>Edit</button>
          <button type="button" data-comment-delete>Delete</button>
        </span>
      </footer>`;
    document.body.append(popover);
    const targetRect = rect || anchor.range.getBoundingClientRect();
    positionFloating(popover, targetRect, 360);
    popover.onmouseleave = () => {
      state.commentHoverTimer = window.setTimeout(removeCommentPopover, 220);
    };
    popover.onmouseenter = () => window.clearTimeout(state.commentHoverTimer);
    popover.querySelector("[data-comment-edit]").onclick = () => openCommentEditor(anchor);
    popover.querySelector("[data-comment-delete]").onclick = () => deleteComment(anchor);
  }

  function showCommentFeedback(message, kind = "") {
    let toast = document.querySelector(".research-comment-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "research-comment-toast";
      toast.dataset.researchCommentUi = "true";
      toast.setAttribute("role", "status");
      document.body.append(toast);
    }
    toast.dataset.kind = kind;
    toast.textContent = message;
    window.setTimeout(() => toast.remove(), 2600);
  }

  async function saveCommentDraft(data, selector, content, feedback) {
    try {
      const saved = await request(
        `/api/comment-drafts/${encodeURIComponent(data.source_id)}/${currentDocumentLanguage()}`,
        {
          method: "PUT",
          body: JSON.stringify({
            selector,
            content,
            expected_version: state.commentDraft?.version || 0,
          }),
        }
      );
      state.commentDraft = saved;
      if (feedback) feedback.textContent = "Draft saved locally";
    } catch (error) {
      if (feedback) feedback.textContent = error.message;
    }
  }

  async function openCommentComposer(data, selector, targetRect) {
    document.querySelector(".research-comment-selection-action")?.remove();
    removeCommentPopover();
    document.querySelector(".research-comment-composer")?.remove();
    let existingDraft = null;
    try {
      const payload = await request(
        `/api/comment-drafts/${encodeURIComponent(data.source_id)}/${currentDocumentLanguage()}`
      );
      existingDraft = payload.draft;
    } catch (error) {
      console.warn("Unable to load comment draft", error);
    }
    state.commentDraft = existingDraft;
    const matchingDraft =
      existingDraft?.selector?.exact === selector.exact &&
      existingDraft?.selector?.start === selector.start;
    const composer = document.createElement("aside");
    composer.className = "research-comment-composer";
    composer.dataset.researchCommentUi = "true";
    composer.setAttribute("role", "dialog");
    composer.setAttribute("aria-label", "Add a shared comment");
    composer.innerHTML = `
      <header>
        <span><span aria-hidden="true">💬</span> Add comment</span>
        <button type="button" data-comment-close aria-label="Close comment editor">×</button>
      </header>
      <div class="research-comment-context">
        <strong>${escapeHtml(selector.heading)}</strong>
        <blockquote>${escapeHtml(selector.exact)}</blockquote>
      </div>
      <label>
        <span>Comment</span>
        <textarea rows="4" maxlength="20000" placeholder="Add context, a question, or a research note..."></textarea>
      </label>
      <div class="research-comment-composer-footer">
        <small data-comment-draft-status>${matchingDraft ? "Local draft restored" : "Saved locally while typing"}</small>
        <button type="button" class="research-button primary" data-comment-publish>Publish to Git</button>
      </div>`;
    document.body.append(composer);
    positionFloating(composer, targetRect, 390);
    const textarea = composer.querySelector("textarea");
    const feedback = composer.querySelector("[data-comment-draft-status]");
    textarea.value = matchingDraft ? existingDraft.content : "";
    textarea.focus();
    textarea.setSelectionRange(textarea.value.length, textarea.value.length);
    const close = () => {
      window.clearTimeout(state.commentDraftTimer);
      if (textarea.value.trim()) saveCommentDraft(data, selector, textarea.value, null);
      composer.remove();
      window.getSelection()?.removeAllRanges();
    };
    composer.querySelector("[data-comment-close]").onclick = close;
    textarea.oninput = () => {
      window.clearTimeout(state.commentDraftTimer);
      feedback.textContent = "Saving local draft...";
      state.commentDraftTimer = window.setTimeout(
        () => saveCommentDraft(data, selector, textarea.value, feedback),
        500
      );
    };
    composer.querySelector("[data-comment-publish]").onclick = async (event) => {
      const button = event.currentTarget;
      const content = textarea.value.trim();
      if (!content) {
        feedback.textContent = "Write a comment before publishing";
        textarea.focus();
        return;
      }
      button.disabled = true;
      feedback.textContent = "Publishing...";
      try {
        await request("/api/comments", {
          method: "POST",
          body: JSON.stringify({
            source_id: data.source_id,
            document_sha256: currentDocumentSha(data),
            language: currentDocumentLanguage(),
            selector,
            content,
          }),
        });
        composer.remove();
        window.getSelection()?.removeAllRanges();
        showCommentFeedback("Comment published to the shared Git workspace", "success");
        await refreshCurrentPage(true);
      } catch (error) {
        feedback.textContent = error.message;
        button.disabled = false;
      }
    };
  }

  function showSelectionCommentAction(event) {
    document.querySelector(".research-comment-selection-action")?.remove();
    if (!state.commentData || event.target.closest?.("[data-research-comment-ui]")) return;
    let selector;
    try {
      selector = selectorFromSelection(state.commentData);
    } catch (_error) {
      return;
    }
    const selection = window.getSelection();
    const rect = selection.getRangeAt(0).getBoundingClientRect();
    const button = document.createElement("button");
    button.type = "button";
    button.className = "research-comment-selection-action";
    button.dataset.researchCommentUi = "true";
    button.innerHTML = '<span aria-hidden="true">💬</span> Comment';
    document.body.append(button);
    positionFloating(button, rect, 116);
    button.onclick = () => openCommentComposer(state.commentData, selector, rect);
  }

  async function openCommentEditor(anchor) {
    removeCommentPopover();
    const comment = anchor.comment;
    const editor = document.createElement("aside");
    editor.className = "research-comment-composer research-comment-editor";
    editor.dataset.researchCommentUi = "true";
    editor.setAttribute("role", "dialog");
    editor.setAttribute("aria-label", "Edit shared comment");
    editor.innerHTML = `
      <header><span><span aria-hidden="true">💬</span> Edit comment</span><button type="button" data-comment-close aria-label="Close comment editor">×</button></header>
      <div class="research-comment-context"><strong>${escapeHtml(comment.heading)}</strong><blockquote>${escapeHtml(
        comment.selector.exact
      )}</blockquote></div>
      <label><span>Comment</span><textarea rows="4" maxlength="20000"></textarea></label>
      <div class="research-comment-composer-footer"><small data-comment-draft-status>Changes update the shared Markdown file</small><button type="button" class="research-button primary" data-comment-save>Save changes</button></div>`;
    document.body.append(editor);
    positionFloating(editor, anchor.range.getBoundingClientRect(), 390);
    const textarea = editor.querySelector("textarea");
    const feedback = editor.querySelector("[data-comment-draft-status]");
    textarea.value = comment.content;
    textarea.focus();
    editor.querySelector("[data-comment-close]").onclick = () => editor.remove();
    editor.querySelector("[data-comment-save]").onclick = async (event) => {
      if (!textarea.value.trim()) {
        feedback.textContent = "Comment cannot be empty";
        return;
      }
      event.currentTarget.disabled = true;
      try {
        await request(`/api/comments/${encodeURIComponent(comment.comment_id)}`, {
          method: "PUT",
          body: JSON.stringify({
            content: textarea.value.trim(),
            base_file_sha256: comment.file_sha256,
          }),
        });
        editor.remove();
        showCommentFeedback("Shared comment updated", "success");
        await refreshCurrentPage(true);
      } catch (error) {
        feedback.textContent = error.message;
        event.currentTarget.disabled = false;
      }
    };
  }

  async function deleteComment(anchor) {
    const comment = anchor.comment;
    if (!window.confirm("Delete this shared comment from the Git workspace?")) return;
    try {
      await request(`/api/comments/${encodeURIComponent(comment.comment_id)}`, {
        method: "DELETE",
        body: JSON.stringify({ base_file_sha256: comment.file_sha256 }),
      });
      removeCommentPopover();
      showCommentFeedback("Shared comment deleted", "success");
      await refreshCurrentPage(true);
    } catch (error) {
      showCommentFeedback(error.message, "error");
    }
  }

  function handleCommentPointerMove(event) {
    if (event.target.closest?.("[data-research-comment-ui]")) return;
    const anchor = commentAtPoint(event.clientX, event.clientY);
    if (!anchor) {
      window.clearTimeout(state.commentHoverTimer);
      state.commentHoverTimer = window.setTimeout(removeCommentPopover, 180);
      return;
    }
    window.clearTimeout(state.commentHoverTimer);
    const existing = document.querySelector(".research-comment-popover");
    if (existing?.dataset.commentId === anchor.comment.comment_id) return;
    showCommentPopover(anchor, { left: event.clientX, right: event.clientX, top: event.clientY, bottom: event.clientY, width: 0, height: 0 });
    document.querySelector(".research-comment-popover").dataset.commentId = anchor.comment.comment_id;
  }

  function renderInlineComments(data) {
    clearCommentHighlight();
    state.commentData = data;
    if (!Array.isArray(data.comments)) return;
    const language = currentDocumentLanguage();
    const comments = data.comments.filter((comment) => comment.language === language);
    const index = commentTextIndex();
    state.commentAnchors = comments
      .map((comment) => ({ comment, range: restoreCommentRange(index, comment.selector) }))
      .filter((anchor) => anchor.range);
    applyCommentHighlight();
    const requested = new URLSearchParams(window.location.search).get("comment");
    if (requested) {
      const anchor = state.commentAnchors.find((item) => item.comment.comment_id === requested);
      if (anchor) {
        anchor.range.startContainer.parentElement?.scrollIntoView({ block: "center" });
        window.setTimeout(() => showCommentPopover(anchor), 160);
      } else if (comments.some((comment) => comment.comment_id === requested)) {
        showCommentFeedback("The source changed and this comment anchor cannot be restored safely", "error");
      }
    }
  }

  function evidenceTemplate(kind, evidence) {
    const source = `${evidence.source_id} / ${evidence.title} / ${evidence.heading}`;
    if (kind === "question") {
      return [
        "Question:",
        "Category:",
        `Source section: ${source}`,
        `Evidence: ${evidence.quote}`,
        "Impact:",
        "Required next step:",
      ].join("\n");
    }
    return [
      "Claim:",
      "Topic:",
      `Source section: ${source}`,
      `Evidence: ${evidence.quote}`,
      "Classification: EXPLICIT",
      "Confidence:",
      "Related claims:",
      "Open questions:",
    ].join("\n");
  }

  function renderSummaryPanel(data) {
    document.getElementById("research-summary-panel")?.remove();
    const root = articleRoot();
    if (!root) return;

    const research = data.research;
    const lines = research.summary.length
      ? research.summary
      : ["No shared summary has been published for this page."];
    const translation = data.translation;
    const languageLink = translation.available
      ? `<a class="research-button subtle" href="${escapeHtml(translation.path)}">KOR</a>`
      : '<span class="research-button disabled" title="Korean translation is unavailable">KOR</span>';
    const compareButton = translation.available
      ? '<button class="research-button subtle" type="button" data-compare>Compare ENG/KOR</button>'
      : "";

    const panel = document.createElement("section");
    panel.id = "research-summary-panel";
    panel.className = "research-summary-panel";
    panel.innerHTML = `
      <details>
        <summary>
          <span>Research summary</span>
          <span class="research-summary-meta">${scopeBadge(research)}${summaryBadge(
            research
          )}</span>
        </summary>
        <div class="research-summary-body">
          <div class="research-toolbar">
            <button class="research-button" type="button" data-page-progress-control></button>
            <a class="research-button subtle" href="/${escapeHtml(data.path)}">ENG</a>
            ${languageLink}
            ${compareButton}
            <button class="research-button subtle" type="button" data-edit-summary>Edit</button>
            <button class="research-button subtle" type="button" data-capture-evidence>Capture evidence</button>
            <button class="research-button subtle" type="button" data-toggle-scope>${
              research.scope === "excluded" ? "Include in scope" : "Exclude from scope"
            }</button>
            <a class="research-button subtle" href="${escapeHtml(
              data.source_url.replace(/\.md$/, "")
            )}" target="_blank" rel="noreferrer">Official source</a>
          </div>
          <ol class="research-summary-lines">${lines
            .map((line) => `<li>${escapeHtml(line)}</li>`)
            .join("")}</ol>
          ${
            research.scope === "excluded"
              ? `<aside class="research-scope-note">
                  <div><span class="research-scope-x" aria-hidden="true">✕</span><strong>${escapeHtml(
                    research.scope_category_label || "Excluded from current scope"
                  )}</strong></div>
                  <p>${escapeHtml(research.scope_reason)}</p>
                  <a href="/research/scope">View all excluded pages</a>
                </aside>`
              : ""
          }
          ${relatedRecords(data)}
          <div class="research-editor" hidden>
            <label>Exactly three summary lines
              <textarea rows="6">${escapeHtml(
                (data.draft?.content || research.summary.join("\n")).trim()
              )}</textarea>
            </label>
            <div class="research-editor-actions">
              <button type="button" class="research-button subtle" data-save-draft>Save draft</button>
              <button type="button" class="research-button primary" data-publish-summary>Publish to workspace</button>
              <span class="research-feedback" role="status"></span>
            </div>
          </div>
          <div class="research-evidence" hidden>
            <label>Source-linked evidence draft
              <textarea rows="9"></textarea>
            </label>
            <div class="research-editor-actions">
              <button type="button" class="research-button subtle" data-save-evidence>Save locally</button>
              <button type="button" class="research-button subtle" data-copy-claim>Copy claim draft</button>
              <button type="button" class="research-button subtle" data-copy-question>Copy question draft</button>
              <span class="research-feedback" role="status"></span>
            </div>
          </div>
          <div class="research-comparison" hidden>
            <div><strong>Official English</strong><pre><code data-compare-english></code></pre></div>
            <div><strong>Unofficial Korean</strong><pre><code data-compare-korean></code></pre></div>
          </div>
        </div>
      </details>`;

    const heading = root.querySelector("h1");
    const pageHeader = heading?.closest("#header, header");
    if (pageHeader?.parentNode && root.contains(pageHeader)) {
      pageHeader.parentNode.insertBefore(panel, pageHeader.nextSibling);
    } else if (heading?.parentElement?.parentNode) {
      const titleRow = heading.parentElement;
      titleRow.parentNode.insertBefore(panel, titleRow.nextSibling);
    } else {
      root.prepend(panel);
    }

    const item = state.statusByPath.get(data.path) || {
      source_id: data.source_id,
      progress: data.progress,
      scope: research.scope,
    };
    const progressControl = panel.querySelector("[data-page-progress-control]");
    if (progressControl) {
      updateProgressControl(progressControl, item);
      progressControl.onclick = () => cycleDocumentStatus(item, progressControl);
    }

    const editor = panel.querySelector(".research-editor");
    const feedback = panel.querySelector(".research-feedback");
    const evidencePanel = panel.querySelector(".research-evidence");
    const evidenceText = evidencePanel.querySelector("textarea");
    const evidenceFeedback = evidencePanel.querySelector(".research-feedback");
    evidenceText.value = data.note_draft?.content || "";
    let capturedEvidence = null;
    panel.querySelector("[data-edit-summary]").onclick = () => {
      editor.hidden = !editor.hidden;
    };
    panel.querySelector("[data-save-draft]").onclick = async () => {
      try {
        const content = editor.querySelector("textarea").value;
        const saved = await request(`/api/drafts/${encodeURIComponent(data.source_id)}/summary`, {
          method: "PUT",
          body: JSON.stringify({
            content,
            base_file_sha256: research.file_sha256,
            expected_version: data.draft?.version || 0,
          }),
        });
        data.draft = saved;
        feedback.textContent = "Draft saved locally";
      } catch (error) {
        feedback.textContent = error.message;
      }
    };
    panel.querySelector("[data-publish-summary]").onclick = async () => {
      try {
        const linesToPublish = editor
          .querySelector("textarea")
          .value.split("\n")
          .map((line) => line.trim())
          .filter(Boolean);
        await request(`/api/pages/${encodeURIComponent(data.source_id)}/summary`, {
          method: "POST",
          body: JSON.stringify({
            lines: linesToPublish,
            status: "human_edited",
            base_file_sha256: research.file_sha256,
          }),
        });
        feedback.textContent = "Published to the shared Markdown file";
        await refreshCurrentPage(true);
      } catch (error) {
        feedback.textContent = error.message;
      }
    };
    panel.querySelector("[data-toggle-scope]").onclick = async () => {
      const excluded = research.scope !== "excluded";
      const reason = excluded
        ? window.prompt("Reason for excluding this page from the current scope:", "")
        : "";
      if (excluded && !reason) return;
      try {
        await request(`/api/pages/${encodeURIComponent(data.source_id)}/scope`, {
          method: "PUT",
          body: JSON.stringify({
            scope: excluded ? "excluded" : "included",
            reason,
            base_file_sha256: research.file_sha256,
          }),
        });
        await loadStatuses();
        await refreshCurrentPage(true);
      } catch (error) {
        feedback.textContent = error.message;
      }
    };
    panel.querySelector("[data-capture-evidence]").onclick = () => {
      try {
        capturedEvidence = selectedEvidence(root, data);
        evidenceText.value = evidenceTemplate("claim", capturedEvidence);
        evidencePanel.hidden = false;
        evidenceFeedback.textContent = `Captured ${capturedEvidence.source_id} / ${capturedEvidence.heading}`;
      } catch (error) {
        evidencePanel.hidden = false;
        evidenceFeedback.textContent = error.message;
      }
    };
    panel.querySelector("[data-save-evidence]").onclick = async () => {
      try {
        const saved = await request(`/api/drafts/${encodeURIComponent(data.source_id)}/note`, {
          method: "PUT",
          body: JSON.stringify({
            content: evidenceText.value,
            base_file_sha256: research.file_sha256,
            expected_version: data.note_draft?.version || 0,
          }),
        });
        data.note_draft = saved;
        evidenceFeedback.textContent = "Evidence draft saved locally";
      } catch (error) {
        evidenceFeedback.textContent = error.message;
      }
    };
    panel.querySelector("[data-copy-claim]").onclick = async () => {
      try {
        if (capturedEvidence) evidenceText.value = evidenceTemplate("claim", capturedEvidence);
        await navigator.clipboard.writeText(evidenceText.value);
        evidenceFeedback.textContent = "Claim draft copied";
      } catch (error) {
        evidenceFeedback.textContent = `Copy failed: ${error.message}`;
      }
    };
    panel.querySelector("[data-copy-question]").onclick = async () => {
      try {
        if (capturedEvidence) evidenceText.value = evidenceTemplate("question", capturedEvidence);
        await navigator.clipboard.writeText(evidenceText.value);
        evidenceFeedback.textContent = "Question draft copied";
      } catch (error) {
        evidenceFeedback.textContent = `Copy failed: ${error.message}`;
      }
    };
    const compare = panel.querySelector("[data-compare]");
    if (compare) {
      compare.onclick = async () => {
        const comparison = panel.querySelector(".research-comparison");
        if (comparison.dataset.loaded === "true") {
          comparison.hidden = !comparison.hidden;
          return;
        }
        compare.disabled = true;
        compare.textContent = "Loading...";
        try {
          const payload = await request(`/api/compare?path=${encodeURIComponent(data.path)}`);
          comparison.querySelector("[data-compare-english]").textContent = payload.english;
          comparison.querySelector("[data-compare-korean]").textContent = payload.korean;
          comparison.dataset.loaded = "true";
          comparison.hidden = false;
        } catch (error) {
          feedback.textContent = error.message;
        } finally {
          compare.disabled = false;
          compare.textContent = "Compare ENG/KOR";
        }
      };
    }
  }

  function statusCounts(items) {
    return items.reduce(
      (counts, item) => {
        if (item.scope === "excluded") counts.excluded += 1;
        else counts[normalizeProgress(item.progress)] += 1;
        return counts;
      },
      { unreviewed: 0, complete: 0, excluded: 0 }
    );
  }

  function card(label, value) {
    return `<div class="research-stat"><span>${escapeHtml(label)}</span><strong>${escapeHtml(
      value
    )}</strong></div>`;
  }

  function renderStatusTable(items) {
    return `<div class="research-table-wrap"><table class="research-table">
      <thead><tr><th>Page</th><th>Progress</th><th>Scope</th><th>Summary</th><th>KOR</th></tr></thead>
      <tbody>${items
        .map(
          (item) => `<tr>
            <td><a href="/${escapeHtml(item.path)}">${escapeHtml(item.title)}</a></td>
            <td>${escapeHtml(normalizeProgress(item.progress))}</td>
            <td>${escapeHtml(item.scope)}</td>
            <td>${escapeHtml(item.summary_status)}${item.summary_stale ? " / stale" : ""}</td>
            <td>${item.translation_available ? (item.translation_stale ? "stale" : "available") : "missing"}</td>
          </tr>`
        )
        .join("")}</tbody>
    </table></div>`;
  }

  function optionMarkup(value, label) {
    return `<option value="${escapeHtml(value)}">${escapeHtml(label)}</option>`;
  }

  function renderExcludedCard(item) {
    const koreanLink = item.translation_available
      ? `<a class="research-button subtle" href="/ko/${escapeHtml(item.path)}">Open KOR</a>`
      : "";
    return `<article class="research-excluded-card">
      <header>
        <span class="research-scope-badge"><span aria-hidden="true">✕</span> ${escapeHtml(
          item.scope_category_label
        )}</span>
        <span class="research-area-badge">${escapeHtml(item.area)}</span>
      </header>
      <h3><a href="/${escapeHtml(item.path)}">${escapeHtml(item.title)}</a></h3>
      <code>/${escapeHtml(item.path)}</code>
      <p>${escapeHtml(item.scope_reason)}</p>
      <footer>
        <a class="research-button subtle" href="/${escapeHtml(item.path)}">Open ENG</a>
        ${koreanLink}
      </footer>
    </article>`;
  }

  function renderFavoriteCard(item) {
    const href = favoriteDocumentHref(item);
    const language = href.startsWith("/ko/") ? "KOR" : "ENG";
    return `<a class="research-favorite-card" href="${escapeHtml(href)}">
      <span class="research-favorite-card-star" aria-hidden="true">★</span>
      <span>
        <strong>${escapeHtml(item.title)}</strong>
        <small>${escapeHtml(item.area)} / ${language}</small>
      </span>
    </a>`;
  }

  function renderCommentCard(comment) {
    return `<article class="research-comment-card" id="${escapeHtml(
      comment.comment_id.toLowerCase()
    )}">
      <div class="research-comment-card-meta">
        <span>${escapeHtml(comment.heading)}</span>
        <span>${escapeHtml(comment.language.toUpperCase())}</span>
        ${comment.stale ? '<span class="research-comment-state">Source changed</span>' : ""}
      </div>
      <blockquote>${escapeHtml(comment.selector.exact)}</blockquote>
      <p>${escapeHtml(comment.content)}</p>
      <footer>
        <time datetime="${escapeHtml(comment.updated_at)}">${escapeHtml(
          new Date(comment.updated_at).toLocaleString()
        )}</time>
        <a href="${escapeHtml(commentDocumentHref(comment))}">Open in document <span aria-hidden="true">→</span></a>
      </footer>
    </article>`;
  }

  function renderCommentsDashboard(comments, root) {
    state.comments = comments;
    state.commentsNavigationSignature = null;
    const groups = groupedComments(comments);
    root.innerHTML = `<section class="research-comments-page">
      <div class="research-comments-page-heading">
        <span class="research-comments-page-icon" aria-hidden="true">💬</span>
        <div>
          <span class="research-eyebrow">Shared Git-backed annotations</span>
          <h2>Comments</h2>
          <p>${comments.length} comment${comments.length === 1 ? "" : "s"} across ${
      groups.length
    } page${groups.length === 1 ? "" : "s"}</p>
        </div>
      </div>
      <p class="research-comments-page-intro">Select text in an official document to publish a source-anchored comment. Draft text remains local until you publish it.</p>
      ${
        groups.length
          ? `<div class="research-comment-groups">${groups
              .map(
                (group) => `<section class="research-comment-group" id="comment-page-${escapeHtml(
                  group.source_id.toLowerCase()
                )}">
                  <header>
                    <div>
                      <span class="research-area-badge">${escapeHtml(group.source_id)}</span>
                      <h3>${escapeHtml(commentDisplayTitle(group))}</h3>
                      <code>/${escapeHtml(group.source_path)}</code>
                    </div>
                    <span class="research-comment-count">${group.comments.length}</span>
                  </header>
                  <div class="research-comment-card-list">${group.comments
                    .map(renderCommentCard)
                    .join("")}</div>
                </section>`
              )
              .join("")}</div>`
          : '<p class="research-empty">No shared comments yet. Select text in a document and choose Comment to add the first one.</p>'
      }
    </section>`;
    renderCommentsNavigation();
  }

  function renderScopeDashboard(payload, root) {
    const profile = payload.profile || {};
    const items = [...(payload.items || [])].sort(
      (left, right) =>
        left.area.localeCompare(right.area) || left.title.localeCompare(right.title)
    );
    const areaCounts = items.reduce((counts, item) => {
      counts.set(item.area, (counts.get(item.area) || 0) + 1);
      return counts;
    }, new Map());
    const areas = [...areaCounts].sort((left, right) => left[0].localeCompare(right[0]));
    const categoryCounts = items.reduce((counts, item) => {
      const current = counts.get(item.scope_category) || {
        label: item.scope_category_label,
        count: 0,
      };
      current.count += 1;
      counts.set(item.scope_category, current);
      return counts;
    }, new Map());
    const categories = [...categoryCounts].sort((left, right) =>
      left[1].label.localeCompare(right[1].label)
    );
    const includedCount = Math.max(0, (profile.total_pages || 0) - items.length);

    root.innerHTML = `
      <section class="research-scope-hero">
        <span class="research-eyebrow">Current launch profile</span>
        <h2>${escapeHtml(profile.title || "Public testnet scope")}</h2>
        <p>${escapeHtml(profile.decision || "")}</p>
        <details>
          <summary>Decision conditions</summary>
          <ul>${(profile.conditions || [])
            .map((condition) => `<li>${escapeHtml(condition)}</li>`)
            .join("")}</ul>
        </details>
      </section>
      <div class="research-stats research-scope-stats">
        ${card("Official pages", profile.total_pages || 0)}
        ${card("In launch scope", includedCount)}
        ${card("Excluded with X", items.length)}
      </div>
      <section class="research-scope-browser" aria-labelledby="excluded-pages-heading">
        <div class="research-scope-browser-heading">
          <div>
            <span class="research-eyebrow">Scope review queue</span>
            <h2 id="excluded-pages-heading">Excluded pages</h2>
          </div>
          <p data-scope-count role="status" aria-live="polite"></p>
        </div>
        <form class="research-scope-filters" data-scope-filters>
          <label class="research-scope-search">Search
            <input type="search" name="query" autocomplete="off" placeholder="Title, path, or reason">
          </label>
          <label>Documentation area
            <select name="area">${optionMarkup("", "All areas")}${areas
              .map(([area, total]) => optionMarkup(area, `${area} (${total})`))
              .join("")}</select>
          </label>
          <label>Exclusion reason
            <select name="category">${optionMarkup("", "All reasons")}${categories
              .map(([value, item]) => optionMarkup(value, `${item.label} (${item.count})`))
              .join("")}</select>
          </label>
          <button class="research-button subtle" type="reset">Clear filters</button>
        </form>
        <div class="research-excluded-list" data-scope-results></div>
      </section>`;

    const form = root.querySelector("[data-scope-filters]");
    const results = root.querySelector("[data-scope-results]");
    const count = root.querySelector("[data-scope-count]");
    const update = () => {
      const formData = new FormData(form);
      const query = String(formData.get("query") || "").trim().toLocaleLowerCase();
      const area = String(formData.get("area") || "");
      const category = String(formData.get("category") || "");
      const filtered = items.filter((item) => {
        const searchable = [
          item.title,
          item.path,
          item.scope_reason,
          item.scope_category_label,
          item.area,
        ]
          .join(" ")
          .toLocaleLowerCase();
        return (
          (!query || searchable.includes(query)) &&
          (!area || item.area === area) &&
          (!category || item.scope_category === category)
        );
      });
      count.textContent = `Showing ${filtered.length} of ${items.length}`;
      results.innerHTML = filtered.length
        ? filtered.map(renderExcludedCard).join("")
        : '<p class="research-empty">No excluded pages match these filters.</p>';
    };
    form.addEventListener("input", update);
    form.addEventListener("reset", () => window.setTimeout(update, 0));
    update();
  }

  async function renderDashboard(view, root) {
    root.innerHTML = '<p class="research-loading">Loading local research data...</p>';
    try {
      if (view === "claims") {
        const { items } = await request("/api/claims");
        root.innerHTML = `<div class="research-records">${items
          .map(
            (item) => `<article id="${escapeHtml(item.id.toLowerCase())}" class="research-record">
              <header><strong>${escapeHtml(item.id)}</strong><span class="research-badge ${escapeHtml(
                item.classification.toLowerCase()
              )}">${escapeHtml(item.classification)}</span></header>
              <h3>${escapeHtml(item.claim)}</h3>
              <p>${escapeHtml(item.evidence)}</p>
              <div class="research-record-sources">${(item.sources || [])
                .map(
                  (source) =>
                    `<a href="/${escapeHtml(source.path)}">${escapeHtml(source.source_id)}</a>`
                )
                .join(" ")}</div>
              <small>${escapeHtml(item.topic)} / ${escapeHtml(item.confidence)} confidence</small>
            </article>`
          )
          .join("")}</div>`;
        return;
      }
      if (view === "questions") {
        const { items } = await request("/api/questions");
        root.innerHTML = `<div class="research-records">${items
          .map(
            (item) => `<article id="${escapeHtml(item.id.toLowerCase())}" class="research-record">
              <header><strong>${escapeHtml(item.id)}</strong><span class="research-badge unclear">${escapeHtml(
                item.category
              )}</span></header>
              <h3>${escapeHtml(item.question)}</h3>
              <p><strong>Impact:</strong> ${escapeHtml(item.impact)}</p>
              <p><strong>Next:</strong> ${escapeHtml(item.next_step)}</p>
            </article>`
          )
          .join("")}</div>`;
        return;
      }

      if (view === "scope") {
        renderScopeDashboard(await request("/api/scope"), root);
        return;
      }
      if (view === "comments") {
        const { items } = await request("/api/comments");
        renderCommentsDashboard(items, root);
        return;
      }
      const statusPayload = await request("/api/pages/status");
      const items = statusPayload.items;
      if (view === "favorites") {
        const favorites = items
          .filter((item) => item.favorite)
          .sort((left, right) => left.title.localeCompare(right.title));
        root.innerHTML = `<section class="research-favorites-page">
          <div class="research-favorites-page-heading">
            <span class="research-favorites-page-star" aria-hidden="true">★</span>
            <div>
              <span class="research-eyebrow">Personal local collection</span>
              <h2>Favorites</h2>
              <p>${favorites.length} saved page${favorites.length === 1 ? "" : "s"}</p>
            </div>
          </div>
          ${
            favorites.length
              ? `<div class="research-favorite-grid">${favorites
                  .map(renderFavoriteCard)
                  .join("")}</div>`
              : '<p class="research-empty">Select ☆ next to a page title to add it here.</p>'
          }
        </section>`;
        return;
      }
      if (view === "changes") {
        const changed = items.filter((item) => item.summary_stale || item.translation_stale);
        root.innerHTML = changed.length
          ? renderStatusTable(changed)
          : '<p class="research-empty">No shared summaries or translations are stale.</p>';
        return;
      }
      if (view === "progress") {
        root.innerHTML = renderStatusTable(items.filter((item) => item.scope !== "excluded"));
        return;
      }

      const config = await request("/api/config");
      const counts = statusCounts(items);
      root.innerHTML = `
        <div class="research-stats">
          ${card("Official pages", config.documents)}
          ${card("Unreviewed", counts.unreviewed)}
          ${card("Complete", counts.complete)}
          ${card("Excluded", counts.excluded)}
        </div>
        <form class="research-search" data-research-search>
          <label>Search official English, Korean translations, and research notes
            <div><input name="q" type="search" required autocomplete="off" placeholder="Search the Canton workspace"><button class="research-button primary">Search</button></div>
          </label>
        </form>
        <div data-search-results></div>
        <p class="research-version">Pinned cf-docs commit: <code>${escapeHtml(
          config.upstream_commit.slice(0, 12)
        )}</code></p>`;
      root.querySelector("[data-research-search]").onsubmit = async (event) => {
        event.preventDefault();
        const query = new FormData(event.currentTarget).get("q");
        const target = root.querySelector("[data-search-results]");
        target.innerHTML = '<p class="research-loading">Searching...</p>';
        const result = await request(`/api/search?q=${encodeURIComponent(query)}`);
        target.innerHTML = result.items.length
          ? `<div class="research-search-results">${result.items
              .map(
                (item) => `<a class="research-search-result" href="${escapeHtml(item.path)}">
                  <strong>${escapeHtml(item.title)}</strong>
                  <span>${escapeHtml(item.language.toUpperCase())} / ${escapeHtml(item.kind)}</span>
                  <p>${escapeHtml(item.snippet)
                    .replaceAll("&lt;mark&gt;", "<mark>")
                    .replaceAll("&lt;/mark&gt;", "</mark>")}</p>
                </a>`
              )
              .join("")}</div>`
          : '<p class="research-empty">No matching documents.</p>';
      };
    } catch (error) {
      root.innerHTML = `<div class="research-api-error"><strong>Research API unavailable</strong><p>${escapeHtml(
        error.message
      )}</p><code>python3 -m portal serve</code></div>`;
    }
  }

  async function loadStatuses() {
    try {
      const payload = await request("/api/pages/status");
      state.statusByPath = new Map(payload.items.map((item) => [item.path, item]));
      renderFavoritesNavigation();
      renderCommentsNavigation();
      decorateNavigation();
      decorateFavoritesHeaderLink();
    } catch (error) {
      console.warn("Research API unavailable", error);
    }
  }

  async function refreshCurrentPage(force = false) {
    const currentPath = canonicalPath();
    if (!force && state.activePath === currentPath) return;
    state.activePath = currentPath;
    clearCommentHighlight();
    state.commentData = null;
    document.getElementById("research-summary-panel")?.remove();

    const dashboard = document.querySelector("#research-workspace-view[data-research-view]");
    if (dashboard) {
      await renderDashboard(dashboard.dataset.researchView || "overview", dashboard);
      return;
    }
    if (currentPath.startsWith("research/")) return;
    try {
      const data = await request(`/api/page?path=${encodeURIComponent(currentPath)}`);
      renderSummaryPanel(data);
      window.requestAnimationFrame(() => renderInlineComments(data));
    } catch (error) {
      if (!String(error.message).includes("Unknown official document")) {
        console.warn("Unable to render research summary", error);
      }
    }
  }

  function scheduleRefresh() {
    window.clearTimeout(state.refreshTimer);
    scheduleMermaidFallback();
    state.refreshTimer = window.setTimeout(() => {
      renderFavoritesNavigation();
      renderCommentsNavigation();
      decorateNavigation();
      decorateFavoritesHeaderLink();
      localizeKoreanDocumentLinks();
      refreshCurrentPage();
    }, 120);
  }

  async function boot() {
    document.documentElement.dataset.researchWorkspace = "ready";
    document.addEventListener("click", recoverSlowDocumentNavigation, true);
    document.addEventListener("click", preserveKoreanDocumentNavigation, true);
    document.addEventListener("mouseup", (event) =>
      window.setTimeout(() => showSelectionCommentAction(event), 20)
    );
    document.addEventListener("keydown", handleCommentEscape);
    document.addEventListener("pointermove", handleCommentPointerMove, { passive: true });
    await loadStatuses();
    await refreshCurrentPage(true);
    decorateFavoritesHeaderLink();
    localizeKoreanDocumentLinks();
    scheduleMermaidFallback();
    new MutationObserver(scheduleRefresh).observe(document.body, { childList: true, subtree: true });
    window.addEventListener("popstate", () => refreshCurrentPage(true));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();
