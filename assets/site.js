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

// 99 for the 1: refresh the partner count from Planning Center (via /api/n99).
// The number baked into the page is the fallback if the API isn't configured.
(function(){
  var els=document.querySelectorAll('[data-n99-count]');
  if(!els.length)return;
  fetch('/api/n99').then(function(r){return r.ok?r.json():null}).then(function(j){
    if(!j||typeof j.count!=='number')return;
    var n=Math.max(0,Math.min(99,j.count));
    els.forEach(function(e){e.textContent=n});
    document.querySelectorAll('[data-n99-fill]').forEach(function(f){f.style.width=(n/99*100).toFixed(1)+'%'});
  }).catch(function(){});
})();
