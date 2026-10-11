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

// Latest message: swap in the newest Sunday message from YouTube (via /api/latest-message).
// The image and copy baked into the page are the fallback if the API is unavailable.
(function(){
  var sec=document.getElementById('latest-message');
  if(!sec)return;
  fetch('/api/latest-message').then(function(r){return r.ok?r.json():null}).then(function(j){
    if(!j||!j.videoId)return;
    var img=sec.querySelector('[data-lm-thumb]');
    if(img){
      var probe=new Image();
      probe.onload=function(){ if(probe.naturalWidth>400){img.src=j.thumbnail;} else {img.src=j.thumbnailFallback;} };
      probe.onerror=function(){img.src=j.thumbnailFallback};
      probe.src=j.thumbnail;
      img.alt=j.title;
    }
    sec.querySelectorAll('[data-lm-link]').forEach(function(a){a.href=j.url});
    var t=sec.querySelector('[data-lm-title]'); if(t)t.textContent=j.messageTitle||j.title;
    var e=sec.querySelector('[data-lm-eyebrow]');
    if(e){
      var d=j.published?new Date(j.published):null;
      var when=d?d.toLocaleDateString('en-US',{month:'long',day:'numeric',year:'numeric'}):'';
      e.textContent='Latest Message'+(when?' \u00b7 '+when:'');
    }
    var l=sec.querySelector('[data-lm-lede]');
    if(l){
      var s=j.series?(j.series+(j.part?', Part '+j.part:'')):'';
      l.textContent=(s?s+'. ':'')+'Missed Sunday? Every message goes up on YouTube. Start there, then join us in the room this week.';
    }
  }).catch(function(){});
})();
