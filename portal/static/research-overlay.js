(() => {
  "use strict";

  const API_BASE = "http://127.0.0.1:8787";
  const PROGRESS_ORDER = ["unreviewed", "in_progress", "complete"];
  const PROGRESS_DISPLAY = {
    unreviewed: { icon: "□", label: "Unreviewed" },
    in_progress: { icon: "◩", label: "In progress" },
    complete: { icon: "✓", label: "Complete" },
  };
  const state = { statusByPath: new Map(), activePath: null, refreshTimer: null };

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

  function nextProgress(current) {
    const index = PROGRESS_ORDER.indexOf(current);
    return PROGRESS_ORDER[(index + 1) % PROGRESS_ORDER.length];
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
    const display = PROGRESS_DISPLAY[item.progress] || PROGRESS_DISPLAY.unreviewed;
    if (control.textContent !== display.icon) control.textContent = display.icon;
    control.dataset.status = item.progress;
    control.title = display.label;
    control.setAttribute("aria-label", `Research status: ${display.label}`);
  }

  function decorateNavigation() {
    if (!state.statusByPath.size) return;
    document.querySelectorAll("aside a[href], nav a[href]").forEach((link) => {
      if (link.closest("main")) return;
      const item = state.statusByPath.get(canonicalPath(link.href));
      if (!item) return;

      let marker = link.querySelector(".research-nav-marker");
      if (!marker) {
        marker = document.createElement("span");
        marker.className = "research-nav-marker";
        marker.setAttribute("role", "button");
        marker.setAttribute("tabindex", "0");
        link.append(marker);
      }

      if (item.scope === "excluded") {
        if (marker.textContent !== "✕") marker.textContent = "✕";
        marker.dataset.status = "excluded";
        marker.title = item.scope_reason || "Excluded from current research scope";
        marker.setAttribute("aria-label", marker.title);
        marker.onclick = null;
        marker.onkeydown = null;
      } else {
        updateProgressControl(marker, item);
        const advance = async (event) => {
          event.preventDefault();
          event.stopPropagation();
          await setProgress(item, nextProgress(item.progress));
        };
        marker.onclick = advance;
        marker.onkeydown = (event) => {
          if (event.key === "Enter" || event.key === " ") advance(event);
        };
      }
    });
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
          <span class="research-summary-meta">${summaryBadge(research)}</span>
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
          ${research.scope === "excluded" ? `<p class="research-scope-note">Excluded: ${escapeHtml(research.scope_reason)}</p>` : ""}
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
    if (heading?.parentNode) heading.parentNode.insertBefore(panel, heading.nextSibling);
    else root.prepend(panel);

    const item = state.statusByPath.get(data.path) || {
      source_id: data.source_id,
      progress: data.progress,
      scope: research.scope,
    };
    const progressControl = panel.querySelector("[data-page-progress-control]");
    updateProgressControl(progressControl, item);
    progressControl.onclick = () => setProgress(item, nextProgress(item.progress));

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
        counts[item.progress] = (counts[item.progress] || 0) + 1;
        if (item.scope === "excluded") counts.excluded += 1;
        return counts;
      },
      { unreviewed: 0, in_progress: 0, complete: 0, excluded: 0 }
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
            <td>${escapeHtml(item.progress.replaceAll("_", " "))}</td>
            <td>${escapeHtml(item.scope)}</td>
            <td>${escapeHtml(item.summary_status)}${item.summary_stale ? " / stale" : ""}</td>
            <td>${item.translation_available ? (item.translation_stale ? "stale" : "available") : "missing"}</td>
          </tr>`
        )
        .join("")}</tbody>
    </table></div>`;
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

      const statusPayload = await request("/api/pages/status");
      const items = statusPayload.items;
      if (view === "scope") {
        const excluded = items.filter((item) => item.scope === "excluded");
        root.innerHTML = excluded.length
          ? renderStatusTable(excluded)
          : '<p class="research-empty">No pages are excluded from the current scope.</p>';
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
        root.innerHTML = renderStatusTable(items);
        return;
      }

      const config = await request("/api/config");
      const counts = statusCounts(items);
      root.innerHTML = `
        <div class="research-stats">
          ${card("Official pages", config.documents)}
          ${card("Unreviewed", counts.unreviewed)}
          ${card("In progress", counts.in_progress)}
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
      decorateNavigation();
    } catch (error) {
      console.warn("Research API unavailable", error);
    }
  }

  async function refreshCurrentPage(force = false) {
    const currentPath = canonicalPath();
    if (!force && state.activePath === currentPath) return;
    state.activePath = currentPath;
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
    } catch (error) {
      if (!String(error.message).includes("Unknown official document")) {
        console.warn("Unable to render research summary", error);
      }
    }
  }

  function scheduleRefresh() {
    window.clearTimeout(state.refreshTimer);
    state.refreshTimer = window.setTimeout(() => {
      decorateNavigation();
      refreshCurrentPage();
    }, 120);
  }

  async function boot() {
    document.documentElement.dataset.researchWorkspace = "ready";
    await loadStatuses();
    await refreshCurrentPage(true);
    new MutationObserver(scheduleRefresh).observe(document.body, { childList: true, subtree: true });
    window.addEventListener("popstate", () => refreshCurrentPage(true));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();
