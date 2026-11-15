// Light/dark toggle, shared by the homepage and the notes. Load it in <head> (not deferred).
//
// By default the site follows the system setting. Clicking the button stores a choice
// under the same localStorage key Quarto uses ("quarto-color-scheme": "alternate" = dark,
// "default" = light), so a choice made on the homepage carries over to notes and back.
(function () {
  var KEY = "quarto-color-scheme";
  var root = document.documentElement;
  var systemDark = window.matchMedia("(prefers-color-scheme: dark)");

  var MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>';
  var SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function store(dark) {
    try { localStorage.setItem(KEY, dark ? "alternate" : "default"); } catch (e) { /* private mode */ }
  }

  function isDark() {
    var choice = stored();
    return choice ? choice === "alternate" : systemDark.matches;
  }

  // Homepage colors: data-theme on <html> overrides the system preference in shared.css.
  function apply() {
    var choice = stored();
    if (choice) root.setAttribute("data-theme", choice === "alternate" ? "dark" : "light");
    else root.removeAttribute("data-theme");
  }

  function updateButton(button) {
    var dark = isDark();
    button.innerHTML = dark ? SUN : MOON;
    button.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    button.title = button.getAttribute("aria-label");
  }

  apply(); // before first paint, so there is no flash of the wrong theme

  document.addEventListener("DOMContentLoaded", function () {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "theme-toggle";
    updateButton(button);

    button.addEventListener("click", function () {
      if (typeof window.quartoToggleColorScheme === "function") {
        // Note pages: let Quarto swap its stylesheets; it stores the choice under the same key.
        window.quartoToggleColorScheme();
      } else {
        store(!isDark());
      }
      apply();
      updateButton(button);
    });

    // Follow system changes while no choice is stored.
    systemDark.addEventListener("change", function () {
      apply();
      updateButton(button);
    });

    document.body.appendChild(button);
  });
})();
