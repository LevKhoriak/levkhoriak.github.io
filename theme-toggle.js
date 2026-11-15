// Theme button, shared by the homepage and the notes. Load it in <head> (not deferred).
//
// Cycles through three states: system -> light -> dark -> system.
// "system" follows the OS setting (nothing stored). Light/dark are stored under the same
// localStorage key Quarto uses ("quarto-color-scheme": "default" = light, "alternate" = dark),
// so the choice carries between the homepage and the notes.
(function () {
  var KEY = "quarto-color-scheme";
  var ORDER = ["system", "light", "dark"];
  var root = document.documentElement;
  var systemDark = window.matchMedia("(prefers-color-scheme: dark)");

  var ICONS = {
    light: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    dark: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>',
    system: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg>'
  };

  function getState() {
    var value = null;
    try { value = localStorage.getItem(KEY); } catch (e) { /* storage blocked */ }
    return value === "alternate" ? "dark" : value === "default" ? "light" : "system";
  }

  function setState(state) {
    try {
      if (state === "system") localStorage.removeItem(KEY);
      else localStorage.setItem(KEY, state === "dark" ? "alternate" : "default");
    } catch (e) { /* storage blocked: the change lasts until the page is left */ }
  }

  function wantsDark(state) {
    return state === "system" ? systemDark.matches : state === "dark";
  }

  // Homepage colors: data-theme on <html> overrides the system preference in shared.css.
  function applyRoot(state) {
    if (state === "system") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", state);
  }

  // Note pages: Quarto swaps its own stylesheets; ask it to switch if it shows the wrong mode.
  function applyQuarto(state) {
    if (typeof window.quartoToggleColorScheme !== "function") return;
    var showingDark = document.body.classList.contains("quarto-dark");
    if (showingDark !== wantsDark(state)) window.quartoToggleColorScheme(); // also writes the key; the caller overwrites it
  }

  function updateButton(button, state) {
    var next = ORDER[(ORDER.indexOf(state) + 1) % ORDER.length];
    button.innerHTML = ICONS[state];
    button.setAttribute("aria-label", "Theme: " + state + " (click for " + next + ")");
    button.title = button.getAttribute("aria-label");
  }

  applyRoot(getState()); // before first paint, so there is no flash of the wrong theme

  document.addEventListener("DOMContentLoaded", function () {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "theme-toggle";
    updateButton(button, getState());

    button.addEventListener("click", function () {
      var state = ORDER[(ORDER.indexOf(getState()) + 1) % ORDER.length];
      applyQuarto(state); // first: Quarto decides which way to flip from the *old* stored value
      setState(state);
      applyRoot(state);
      updateButton(button, state);
    });

    document.body.appendChild(button);
  });
})();
