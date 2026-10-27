// 1. Open / close the sidebar on phones.
document.querySelectorAll("[data-toggle-nav]").forEach(function (el) {
  el.addEventListener("click", function () {
    document.body.classList.toggle("nav-open");
  });
});

// 2. Toast messages: close on click, and fade out after 4 seconds.
document.querySelectorAll(".toast").forEach(function (toast) {
  function hide() {
    toast.classList.add("hide");
    setTimeout(function () { toast.remove(); }, 300);
  }
  toast.querySelector("button").addEventListener("click", hide);
  setTimeout(hide, 4000);
});

// 3. Filter dropdowns submit themselves when changed.
document.querySelectorAll("[data-autosubmit]").forEach(function (select) {
  select.addEventListener("change", function () { select.form.submit(); });
});

// 4. Ask before running buttons that have data-confirm="message".
document.querySelectorAll("[data-confirm]").forEach(function (btn) {
  btn.addEventListener("click", function (e) {
    if (!confirm(btn.dataset.confirm)) e.preventDefault();
  });
});