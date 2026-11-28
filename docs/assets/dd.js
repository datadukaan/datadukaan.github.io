/* Data Dukaan: reading progress (stored in this browser only) + episode finder. */
(function () {
  var KEY = "dd-read";
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return []; } }
  function save(list) { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {} }

  function paintButtons(day, on) {
    document.querySelectorAll('.dd-done[data-day="' + day + '"]').forEach(function (b) {
      b.setAttribute("aria-pressed", on ? "true" : "false");
      b.querySelector(".dd-done-label").textContent = on ? "Read" : "Mark as read";
    });
  }

  function setupDayPage() {
    var buttons = document.querySelectorAll(".dd-done");
    if (!buttons.length) return;
    var day = Number(buttons[0].dataset.day);
    paintButtons(day, load().indexOf(day) !== -1);
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        var list = load(), i = list.indexOf(day);
        if (i === -1) list.push(day); else list.splice(i, 1);
        save(list); paintButtons(day, i === -1);
      });
    });
  }

  function setupHome() {
    var shelf = document.querySelector(".dd-shelf");
    if (!shelf) return;
    var read = load();
    read.forEach(function (d) {
      var box = shelf.querySelector('a[data-day="' + d + '"]'); if (box) box.classList.add("is-read");
      var row = document.querySelector('.dd-row[data-day="' + d + '"]'); if (row) row.classList.add("is-done");
    });
    var count = document.querySelector(".dd-read-count");
    if (count && read.length) { count.hidden = false; count.textContent = ", and you've read " + read.length; }

    var input = document.querySelector(".dd-search input");
    var chips = document.querySelectorAll(".dd-chip");
    var empty = document.querySelector(".dd-empty");
    var module = "all";
    function apply() {
      var q = (input.value || "").trim().toLowerCase(), shown = 0;
      document.querySelectorAll(".dd-module").forEach(function (sec) {
        var inModule = module === "all" || sec.dataset.module === module, any = false;
        sec.querySelectorAll(".dd-row").forEach(function (row) {
          var ok = inModule && (!q || row.dataset.search.indexOf(q) !== -1);
          row.hidden = !ok; if (ok) { any = true; shown++; }
        });
        sec.hidden = !any;
      });
      empty.hidden = shown !== 0;
    }
    input.addEventListener("input", apply);
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        chips.forEach(function (x) { x.classList.toggle("is-on", x === c); x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
        module = c.dataset.filter; apply();
      });
    });
  }

  function init() { setupDayPage(); setupHome(); }
  if (window.document$ && window.document$.subscribe) window.document$.subscribe(init);
  else document.addEventListener("DOMContentLoaded", init);
})();
