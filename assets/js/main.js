/* HALO & GRAIN — main.js (V1) — shared across all pages */
(function () {
  'use strict';

  /* nav: scrolled state + floating WhatsApp reveal */
  var nav = document.getElementById('nav');
  var waFloat = document.getElementById('waFloat');
  function onScroll() {
    var y = window.scrollY;
    if (nav && !nav.classList.contains('solid')) nav.classList.toggle('scrolled', y > 40);
    if (waFloat) waFloat.classList.toggle('show', y > 500);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* mobile menu */
  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      links.classList.toggle('open', !open);
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* portfolio filter (home) */
  var filterBtns = document.querySelectorAll('.filters button');
  var frames = document.querySelectorAll('.frame[data-cat]');
  if (filterBtns.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        filterBtns.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        btn.setAttribute('aria-pressed', 'true');
        var f = btn.dataset.filter;
        frames.forEach(function (fr) {
          fr.classList.toggle('hide', !(f === 'all' || fr.dataset.cat === f));
        });
      });
    });
  }

  /* stat count-up */
  var prefersReduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var counters = document.querySelectorAll('[data-count]');
  function runCount(el) {
    var target = +el.dataset.count, suffix = el.dataset.suffix || '';
    if (prefersReduce) { el.textContent = target + suffix; return; }
    var cur = 0, step = Math.max(1, Math.ceil(target / 60));
    (function tick() {
      cur = Math.min(target, cur + step);
      el.textContent = cur + suffix;
      if (cur < target) requestAnimationFrame(tick);
    })();
  }
  if (counters.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { runCount(en.target); obs.unobserve(en.target); }
        });
      }, { threshold: 0.6 });
      counters.forEach(function (c) { io.observe(c); });
    } else {
      counters.forEach(runCount);
    }
  }

  /* showreel lite-embed */
  var reelPlay = document.getElementById('reelPlay');
  var reelFrame = document.getElementById('reel-frame');
  if (reelPlay && reelFrame) {
    reelPlay.addEventListener('click', function () {
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1&rel=0';
      iframe.title = 'Halo & Grain showreel';
      iframe.allow = 'autoplay; encrypted-media; fullscreen';
      iframe.allowFullscreen = true;
      reelFrame.innerHTML = '';
      reelFrame.appendChild(iframe);
    });
  }

  /* enquiry form -> WhatsApp compose (no backend) */
  var sendWa = document.getElementById('sendWa');
  if (sendWa) {
    sendWa.addEventListener('click', function () {
      var wa = sendWa.dataset.wa || '919876543210';
      var svc = sendWa.dataset.service ? (' (' + sendWa.dataset.service + ')') : '';
      var g = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; };
      var text =
        'Hi Halo & Grain! I\'d like to enquire' + svc + '.%0A' +
        'Name: ' + encodeURIComponent(g('f-name') || '-') + '%0A' +
        'Event: ' + encodeURIComponent(g('f-type') || '-') + '%0A' +
        'Date: ' + encodeURIComponent(g('f-date') || 'to be decided') + '%0A' +
        'Details: ' + encodeURIComponent(g('f-msg') || '-');
      window.open('https://wa.me/' + wa + '?text=' + text, '_blank', 'noopener');
    });
  }
})();

/* mega menu (Services) — added V2 */
(function () {
  'use strict';
  var btn = document.getElementById('megaBtn');
  if (!btn) return;
  var host = btn.closest('.has-mega');
  if (!host) return;
  function close() { host.classList.remove('mega-open'); btn.setAttribute('aria-expanded', 'false'); }
  function open() { host.classList.add('mega-open'); btn.setAttribute('aria-expanded', 'true'); }
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    if (host.classList.contains('mega-open')) close(); else open();
  });
  document.addEventListener('click', function (e) {
    if (!host.contains(e.target)) close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && host.classList.contains('mega-open')) { close(); btn.focus(); }
  });
  // close after choosing a service
  host.querySelectorAll('.mega a').forEach(function (a) {
    a.addEventListener('click', close);
  });
})();
