// GateCity Buckhead — shared nav behavior
(function () {
  var hdr = document.getElementById('hdr');
  if (hdr) {
    var onScroll = function () { hdr.classList.toggle('stuck', window.scrollY > 80); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  var burger = document.getElementById('burger');
  function setMenu(open) {
    document.body.classList.toggle('nav-open', open);
    if (!burger) return;
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  if (burger) {
    burger.addEventListener('click', function () {
      setMenu(!document.body.classList.contains('nav-open'));
    });
  }
  Array.prototype.forEach.call(document.querySelectorAll('#mobilenav a'), function (a) {
    a.addEventListener('click', function () { setMenu(false); });
  });

  var groups = Array.prototype.slice.call(document.querySelectorAll('.has-menu'));
  function closeAll(except) {
    groups.forEach(function (g) {
      if (g === except) return;
      g.dataset.open = 'false';
      var t = g.querySelector('.navtrig');
      if (t) t.setAttribute('aria-expanded', 'false');
    });
  }
  groups.forEach(function (g) {
    var trig = g.querySelector('.navtrig');
    if (!trig) return;
    trig.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = g.dataset.open !== 'true';
      closeAll(g);
      g.dataset.open = String(open);
      trig.setAttribute('aria-expanded', String(open));
    });
  });
  document.addEventListener('click', function () { closeAll(); });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    closeAll();
    if (document.body.classList.contains('nav-open')) setMenu(false);
  });
})();
