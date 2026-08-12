(() => {
  "use strict";

  document.documentElement.dataset.researchWorkspace = "loading";
  window.addEventListener("DOMContentLoaded", () => {
    document.documentElement.dataset.researchWorkspace = "ready";
  });
})();
