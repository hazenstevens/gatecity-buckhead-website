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
  var fb=sec.dataset.lmFallback?{videoId:sec.dataset.lmFallback,title:sec.dataset.lmFallbackTitle||'Latest message',url:'https://www.youtube.com/watch?v='+sec.dataset.lmFallback,messageTitle:sec.dataset.lmFallbackMsg,series:sec.dataset.lmFallbackSeries,part:sec.dataset.lmFallbackPart,embedOnly:true}:null;
  fetch('/api/latest-message').then(function(r){return r.ok?r.json():null}).catch(function(){return null}).then(function(j){
    if(!j||!j.videoId)j=fb;
    if(!j)return;
    var img=j.embedOnly?null:sec.querySelector('[data-lm-thumb]');
    if(img){
      var probe=new Image();
      probe.onload=function(){ if(probe.naturalWidth>400){img.src=j.thumbnail;} else {img.src=j.thumbnailFallback;} };
      probe.onerror=function(){img.src=j.thumbnailFallback};
      probe.src=j.thumbnail;
      img.alt=j.title;
    }
    sec.querySelectorAll('[data-lm-link]').forEach(function(a){a.href=j.url});
    var th=sec.querySelector('.msg-thumb');
    if(th){
      var pi=th.querySelector('img');
      if(pi && sec.dataset.lmFallback!==j.videoId){
        var pr=new Image(); pr.onload=function(){ if(pr.naturalWidth>400) pi.src=pr.src; };
        pr.src='https://i.ytimg.com/vi/'+encodeURIComponent(j.videoId)+'/maxres1.jpg';
      }
      th.addEventListener('click',function(ev){
        ev.preventDefault();
        var f=document.createElement('div'); f.className='msg-thumb msg-embed';
        var ifr=document.createElement('iframe');
        ifr.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(j.videoId)+'?rel=0&modestbranding=1&autoplay=1';
        ifr.title=j.title||'Latest message';
        ifr.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
        ifr.setAttribute('allowfullscreen','');
        f.appendChild(ifr); th.parentNode.replaceChild(f,th);
      });
    }
    var nw=sec.querySelector('[data-lm-now]'); if(nw&&j.messageTitle){nw.textContent='This week: '+(j.part?'Part '+j.part+', ':'')+j.messageTitle;}
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

window.__gcbLoad=Date.now();
// Newsletter signup: subscribe to Mailchimp in place (JSONP) and land on /thanks,
// so a real signup ends on our own page, where the Google Ads conversion fires.
// On any failure (or a Mailchimp captcha) it falls back to the normal Mailchimp post.
(function(){
  document.querySelectorAll('form.nl-form').forEach(function(form){
    var action=form.getAttribute('action')||'';
    if(action.indexOf('list-manage.com/subscribe/post')<0)return;
    var msg=document.createElement('p');
    msg.className='nl-msg';msg.setAttribute('role','status');msg.setAttribute('aria-live','polite');
    form.parentNode.insertBefore(msg,form.nextSibling);
    form.addEventListener('submit',function(ev){
      if(form.dataset.fallback==='1')return;
      ev.preventDefault();
      var btn=form.querySelector('button[type=submit]');
      if(btn)btn.disabled=true;
      msg.textContent='Signing you up...';
      var em0=(form.querySelector('[name=EMAIL]')||{}).value||'';
      var fn0=(form.querySelector('[name=FNAME]')||{}).value||'';
      var hp0=(form.querySelector('input[name^="b_"]')||{}).value||'';
      // First choice: our own /api/subscribe (Mailchimp API, no captcha page). If that
      // is unavailable, fall through to the JSONP path below.
      fetch('/api/subscribe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:em0,fname:fn0,hp:hp0,t:Date.now()-(window.__gcbLoad||0)})})
        .then(function(r){return r.json().then(function(j){return {ok:r.ok,status:r.status,j:j};});})
        .then(function(res){
          if(res.ok&&res.j&&res.j.ok){try{sessionStorage.setItem('gcb-ec',JSON.stringify({email:em0,first:fn0}));}catch(_){}window.location.href='/thanks';return;}
          if(res.status===400){msg.textContent=(res.j&&res.j.error)||'Please enter a valid email address.';if(btn)btn.disabled=false;return;}
          jsonp();
        }).catch(jsonp);
      function jsonp(){
      var cb='gcbNl'+Date.now();
      var params=new URLSearchParams(new FormData(form)).toString();
      var url=action.replace('/subscribe/post?','/subscribe/post-json?')+'&'+params+'&c='+cb;
      var script=document.createElement('script');
      var done=false;
      function fallback(){
        if(done)return;done=true;
        try{delete window[cb];}catch(e){}
        form.dataset.fallback='1';form.removeAttribute('target');msg.textContent='';
        if(btn)btn.disabled=false;
        form.submit();
      }
      var timer=setTimeout(fallback,8000);
      window[cb]=function(r){
        if(done)return;
        if(r&&/captcha/i.test(String(r.msg||''))){clearTimeout(timer);fallback();return;}
        done=true;clearTimeout(timer);
        try{delete window[cb];}catch(e){}
        script.remove();
        if(r&&r.result==='success'){try{var em=(form.querySelector('[name=EMAIL]')||{}).value;var fn=(form.querySelector('[name=FNAME]')||{}).value;sessionStorage.setItem('gcb-ec',JSON.stringify({email:em,first:fn||''}));}catch(_){}window.location.href='/thanks';return;}
        var text=(r&&r.msg?String(r.msg):'').replace(/<[^>]*>/g,'').replace(/^\d+\s*-\s*/,'');
        if(/already subscribed/i.test(text)){text="You're already on the list. Thanks!";}
        msg.textContent=text||'Something went wrong. Please try again.';
        if(btn)btn.disabled=false;
      };
      script.onerror=fallback;
      script.src=url;
      document.body.appendChild(script);
      }
    });
  });
})();

// Click-to-play for any poster marked data-yt-embed="VIDEO_ID" (used on the Bible plan pages).
(function(){
  document.querySelectorAll('[data-yt-embed]').forEach(function(th){
    th.addEventListener('click',function(ev){
      ev.preventDefault();
      var id=th.getAttribute('data-yt-embed');
      var f=document.createElement('div'); f.className='msg-thumb msg-embed';
      var ifr=document.createElement('iframe');
      ifr.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'?rel=0&modestbranding=1&autoplay=1';
      ifr.title=(th.querySelector('img')||{}).alt||'Message';
      ifr.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      ifr.setAttribute('allowfullscreen','');
      f.appendChild(ifr); th.parentNode.replaceChild(f,th);
    });
  });
})();

// Prayer request modal: any [data-pray-open] opens it; submits to the Netlify form "prayer-request".
(function(){
  var m=document.getElementById('pray-modal'); if(!m) return;
  var form=document.getElementById('pray-form'), done=m.querySelector('.pray-done'), msg=m.querySelector('.pray-msg'), last=null;
  function open(e){ if(e) e.preventDefault(); last=document.activeElement; m.hidden=false; document.body.classList.add('pray-open'); form.hidden=false; done.hidden=true; msg.textContent=''; setTimeout(function(){ form.querySelector('[name=first]').focus(); },30); }
  function close(){ m.hidden=true; document.body.classList.remove('pray-open'); if(last&&last.focus) last.focus(); }
  document.addEventListener('click',function(e){ var t=e.target.closest&&e.target.closest('[data-pray-open],a[href="#pray"]'); if(t){ open(e); return; } if(e.target.closest&&e.target.closest('[data-pray-close]')) close(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!m.hidden) close(); });
  if(location.hash==='#pray') open();
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var f=new FormData(form);
    if(!String(f.get('first')||'').trim()||!String(f.get('request')||'').trim()){ msg.textContent='Please add your first name and your prayer request.'; return; }
    var em=String(f.get('email')||'').trim(); if(em&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)){ msg.textContent='That email doesn\'t look quite right.'; return; }
    var body=new URLSearchParams({'form-name':'prayer-request',first:f.get('first'),email:em,request:f.get('request'),share:f.get('share')?'yes':'no',page:location.pathname,'bot-field':f.get('bot-field')||''});
    var btn=form.querySelector('button[type=submit]'); btn.disabled=true; msg.textContent='';
    fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:body.toString()})
      .then(function(r){ if(!r.ok) throw 0; form.reset(); form.hidden=true; done.hidden=false; if(window.gtag) gtag('event','prayer_request',{page_path:location.pathname}); })
      .catch(function(){ msg.textContent='Something went wrong. Please try again, or email hazen.stevens@gatecitybuckhead.com.'; })
      .then(function(){ btn.disabled=false; });
  });
})();

/* Blog library: search, helpfulness rating, private question and story forms (Nov 2026) */
(function () {
  var q = document.getElementById('blog-q');
  if (q) {
    var cards = [].slice.call(document.querySelectorAll('.blog-grid .post-card'));
    var none = document.querySelector('.blog-q-none');
    q.addEventListener('input', function () {
      var words = q.value.toLowerCase().trim().split(/\s+/).filter(Boolean), shown = 0;
      cards.forEach(function (c) {
        var t = c.textContent.toLowerCase();
        var hit = words.every(function (w) { return t.indexOf(w) > -1; });
        c.style.display = hit ? '' : 'none'; if (hit) shown++;
      });
      if (none) none.hidden = shown > 0;
    });
  }
  var SB = 'https://egccpqcdpmvkkgdunpuc.supabase.co', KEY = 'sb_publishable_THG77diuxLtHQ_BpN2SvVw_Z2w9XHda';
  function rpc(fn, body) {
    return fetch(SB + '/rest/v1/rpc/' + fn, { method: 'POST', headers: { apikey: KEY, 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.ok ? r.json().catch(function () { return null; }) : null; }).catch(function () { return null; });
  }
  var card = document.querySelector('.fb-card');
  if (card) {
    var page = card.getAttribute('data-fb-page'), id = null;
    var how = card.querySelector('.fb-how'), thanks = card.querySelector('.fb-thanks');
    [].forEach.call(card.querySelectorAll('.fb-scale button'), function (b) {
      b.addEventListener('click', function () {
        if (card.getAttribute('data-done')) return;
        card.setAttribute('data-done', '1');
        [].forEach.call(card.querySelectorAll('.fb-scale button'), function (x) { x.classList.toggle('on', x === b); x.disabled = true; });
        how.hidden = false; thanks.hidden = false;
        rpc('blog_feedback_rate', { p_page: page, p_rating: +b.getAttribute('data-r') }).then(function (r) { id = r; });
      });
    });
    var send = card.querySelector('.fb-send');
    send.addEventListener('click', function () {
      var note = card.querySelector('#fb-note').value.trim();
      if (!note) return;
      send.disabled = true;
      var go = function () { if (id) rpc('blog_feedback_note', { p_id: id, p_note: note }); how.hidden = true; thanks.textContent = 'Thank you for telling us more.'; };
      id ? go() : setTimeout(go, 1500);
    });
  }
  [].forEach.call(document.querySelectorAll('form.fb-form'), function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = f.querySelector('button[type=submit]'); btn.disabled = true;
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(f)).toString() })
        .then(function (r) {
          if (!r.ok) throw 0;
          [].forEach.call(f.querySelectorAll('label,button,.fb-sub'), function (el) { el.hidden = true; el.style.display = 'none'; });
          f.querySelector('.fb-done').hidden = false;
        })
        .catch(function () { btn.disabled = false; alert('Sorry, that did not send. Please try again.'); });
    });
  });
})();

// Post share: phone share sheet, falling back to copying the link.
(function(){
  var msg='I read this and would love your thoughts: ';
  function copy(btn,url){
    var done=function(){var t=btn.textContent;btn.textContent='Link copied';setTimeout(function(){btn.textContent=t},2000)};
    if(navigator.clipboard){navigator.clipboard.writeText(url).then(done,function(){prompt('Copy this link:',url)})}else{prompt('Copy this link:',url)}
  }
  document.querySelectorAll('.share-native').forEach(function(b){b.addEventListener('click',function(){
    var url=b.dataset.shareUrl;
    if(navigator.share){navigator.share({title:b.dataset.shareTitle,text:msg,url:url}).catch(function(){})}else{copy(b,url)}
  })});
  document.querySelectorAll('.share-copy').forEach(function(b){b.addEventListener('click',function(){copy(b,b.dataset.shareUrl)})});
})();
