/* Veridata Compliance Research Group: mobile menu.
   The only script on the site. No tracking, no cookies. */
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;

  // Tells the page the menu script loaded; without it the page falls back to plain links.
  window.vcrgMenu = true;

  function setOpen(open) {
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    nav.classList.toggle("is-open", open);
  }

  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  // Close after choosing a link, on Escape, and when the window grows to desktop width.
  nav.addEventListener("click", function (event) {
    if (event.target.closest("a")) setOpen(false);
  });

  // Close when keyboard focus moves past the menu, so it never covers the focused element.
  nav.addEventListener("focusout", function (event) {
    var next = event.relatedTarget;
    if (toggle.getAttribute("aria-expanded") === "true" && next && !nav.contains(next) && next !== toggle) {
      setOpen(false);
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      setOpen(false);
      toggle.focus();
    }
  });

  var desktop = window.matchMedia("(min-width: 64em)");
  var onChange = function (event) {
    if (event.matches) setOpen(false);
  };
  if (desktop.addEventListener) desktop.addEventListener("change", onChange);
  else if (desktop.addListener) desktop.addListener(onChange);
})();
