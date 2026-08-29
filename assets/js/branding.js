/* HALO & GRAIN — branding.js (V1)
   Multi-tenant branding for a single static repo. Add ?c=<slug> to any URL and
   the page rebrands to that customer using config/customers.json — business
   name, contact, socials, colours and fonts. Missing fields fall back to the
   defaults, so nothing ever goes blank. No API, no backend. */
(function () {
  'use strict';

  // Original strings baked into the pages (used for global find/replace).
  var ORIG = { name: 'Halo & Grain', city: 'Chennai' };

  var ROOT = (document.body && document.body.getAttribute('data-root')) || '';
  function reveal() { document.documentElement.classList.remove('pre-brand'); }

  var params = new URLSearchParams(location.search);
  var slug = params.get('c');
  if (!slug) { reveal(); return; }

  fetch(ROOT + 'config/customers.json', { cache: 'no-cache' })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (cfg) {
      if (!cfg) { reveal(); return; }
      var def = cfg._default || {};
      var cust = (cfg.customers || {})[slug];
      if (!cust) { reveal(); return; }           // unknown slug -> default look
      var c = Object.assign({}, def, cust);      // customer wins; gaps -> default
      try { applyTheme(c); applyText(c, def); applyLinks(c); applyMeta(c); } catch (e) {}
      reveal();
    })
    .catch(reveal);

  /* ---------- colour helpers ---------- */
  function clamp(n) { return Math.max(0, Math.min(255, n)); }
  function parseHex(h) {
    if (!h) return null;
    h = h.replace('#', '');
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    if (h.length !== 6) return null;
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
  }
  function toHex(rgb) {
    return '#' + rgb.map(function (v) { return clamp(Math.round(v)).toString(16).padStart(2, '0'); }).join('');
  }
  function shift(hex, amt) { // amt in [-1,1]; + lighten, - darken
    var rgb = parseHex(hex); if (!rgb) return hex;
    return toHex(rgb.map(function (v) { return amt >= 0 ? v + (255 - v) * amt : v * (1 + amt); }));
  }

  function setVar(k, v) { if (v) document.documentElement.style.setProperty(k, v); }

  function applyTheme(c) {
    if (c.colorPrimary) {
      setVar('--gold', c.colorPrimary);
      setVar('--gold-bright', c.colorPrimaryBright || shift(c.colorPrimary, 0.22));
      setVar('--gold-deep', c.colorPrimaryDeep || shift(c.colorPrimary, -0.20));
    }
    setVar('--ink', c.colorInk);
    setVar('--ink-2', c.colorInk2 || (c.colorInk ? shift(c.colorInk, 0.05) : ''));
    setVar('--ink-3', c.colorInk3 || (c.colorInk ? shift(c.colorInk, 0.10) : ''));
    setVar('--cream', c.colorText);
    setVar('--cream-dim', c.colorTextDim);

    var stack = c.font;
    if (c.googleFont) {
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://fonts.googleapis.com/css2?family=' +
        encodeURIComponent(c.googleFont).replace(/%20/g, '+') + ':wght@400;500;600;700&display=swap';
      document.head.appendChild(link);
      stack = "'" + c.googleFont + "', " + (c.font || 'Helvetica, Arial, sans-serif');
    }
    if (stack) { setVar('--font-body', stack); setVar('--font-display', stack); setVar('--font-mono', stack); }
  }

  /* ---------- text ---------- */
  function applyText(c, def) {
    document.querySelectorAll('[data-b]').forEach(function (el) {
      var key = el.getAttribute('data-b');
      var val = c[key];
      if (key === 'name' && c.name) el.textContent = c.name;
      else if (val && (key === 'phone' || key === 'email' || key === 'address' || key === 'city')) el.textContent = val;
    });
    // global swaps for any in-copy mentions (skip tagged nodes, scripts, styles)
    if (c.name && c.name !== ORIG.name) replaceText(ORIG.name, c.name);
    if (c.city && c.city !== ORIG.city) replaceText(ORIG.city, c.city);
  }

  function replaceText(find, repl) {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue || n.nodeValue.indexOf(find) === -1) return NodeFilter.FILTER_REJECT;
        var p = n.parentElement;
        if (!p) return NodeFilter.FILTER_REJECT;
        var tag = p.tagName;
        if (tag === 'SCRIPT' || tag === 'STYLE') return NodeFilter.FILTER_REJECT;
        if (p.closest('[data-b]')) return NodeFilter.FILTER_REJECT; // already handled precisely
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var nodes = [], n;
    while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(function (node) { node.nodeValue = node.nodeValue.split(find).join(repl); });
  }

  /* ---------- links ---------- */
  function applyLinks(c) {
    var digits = (c.phone || '').replace(/[^\d+]/g, '');
    document.querySelectorAll('[data-href]').forEach(function (a) {
      var key = a.getAttribute('data-href');
      if (key === 'tel' && digits) a.setAttribute('href', 'tel:' + digits);
      else if (key === 'mail' && c.email) a.setAttribute('href', 'mailto:' + c.email);
      else if (key === 'instagram') toggleLink(a, c.instagram);
      else if (key === 'youtube') toggleLink(a, c.youtube);
      else if (key === 'facebook') toggleLink(a, c.facebook);
    });
    // WhatsApp links: swap the number and the pre-filled business name
    if (c.whatsapp) {
      var encOrig = encodeURIComponent(ORIG.name);
      var encNew = encodeURIComponent(c.name || ORIG.name);
      document.querySelectorAll('a[href*="wa.me/"]').forEach(function (a) {
        var href = a.getAttribute('href')
          .replace(/wa\.me\/\d+/, 'wa.me/' + c.whatsapp)
          .split(encOrig).join(encNew)
          .split(ORIG.name).join(c.name || ORIG.name);
        a.setAttribute('href', href);
      });
    }
    // form-compose button carries the number in data-wa
    var send = document.getElementById('sendWa');
    if (send && c.whatsapp) send.setAttribute('data-wa', c.whatsapp);
  }
  function toggleLink(a, url) {
    if (url) { a.setAttribute('href', url); a.style.display = ''; }
    else { a.style.display = 'none'; }   // hide socials the customer doesn't have
  }

  /* ---------- title / meta ---------- */
  function applyMeta(c) {
    if (c.name) document.title = document.title.split(ORIG.name).join(c.name);
    if (c.city) document.title = document.title.split(ORIG.city).join(c.city);
    var md = document.querySelector('meta[name="description"]');
    if (md) {
      var v = md.getAttribute('content') || '';
      if (c.name) v = v.split(ORIG.name).join(c.name);
      if (c.city) v = v.split(ORIG.city).join(c.city);
      md.setAttribute('content', v);
    }
  }
})();
