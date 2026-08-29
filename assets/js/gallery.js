/* HALO & GRAIN — gallery.js (V1)
   Renders every gallery, hero and thumbnail from the site's own image folder.
   Source of truth at runtime is manifest.json (rebuilt automatically by the
   GitHub Action on any change to images/). Falls back to the baked
   window.IMAGES_DATA if the fetch fails (e.g. opened via file://).
   Every <img> has an error guard, so a deleted / renamed file never shows a
   blank or broken image. */
(function () {
  'use strict';

  var ROOT = document.body.getAttribute('data-root') || '';
  var IMG_RE = /\.(?:jpe?g|png|webp|gif|avif)$/i;

  function natSort(a, b) {
    return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' });
  }

  // Accept several shapes: {categories:[...]}, {images:{slug:[...]}}, or a flat {slug:[...]}
  function toMap(data) {
    var map = {};
    if (!data) return map;
    var cats = Array.isArray(data) ? data : (data.categories || null);
    if (cats) {
      cats.forEach(function (c) {
        if (c && c.slug) map[c.slug] = (c.files || []).filter(function (f) { return IMG_RE.test(f); }).slice().sort(natSort);
      });
    } else if (data.images && typeof data.images === 'object') {
      Object.keys(data.images).forEach(function (s) {
        map[s] = (data.images[s] || []).filter(function (f) { return IMG_RE.test(f); }).slice().sort(natSort);
      });
    } else {
      Object.keys(data).forEach(function (s) {
        if (Array.isArray(data[s])) map[s] = data[s].filter(function (f) { return IMG_RE.test(f); }).slice().sort(natSort);
      });
    }
    return map;
  }

  function urlFor(slug, file) { return ROOT + 'images/' + slug + '/' + file; }

  function guard(img) {
    img.addEventListener('error', function () {
      var fr = img.closest('.frame');
      if (fr && fr.parentNode) { fr.parentNode.removeChild(fr); return; }
      img.style.display = 'none';
      if (img.parentElement) img.parentElement.classList.add('img-missing');
    });
  }

  function newImg(src, alt) {
    var im = document.createElement('img');
    im.loading = 'lazy';
    im.decoding = 'async';
    im.alt = alt || '';
    guard(im);
    im.src = src;
    return im;
  }

  // Single-image slots: hero, feature, related thumbnails, avatars, reel cover.
  function fillSingles(map) {
    document.querySelectorAll('[data-img]').forEach(function (el) {
      var slug = el.getAttribute('data-img');
      var i = parseInt(el.getAttribute('data-i') || '0', 10);
      var alt = el.getAttribute('data-alt') || el.alt || '';
      var files = map[slug] || [];
      if (!files.length) { el.classList.add('img-missing'); return; }
      var file = files[i % files.length];
      var src = urlFor(slug, file);
      if (el.tagName === 'IMG') {
        guard(el);
        el.src = src;
        if (alt) el.alt = alt;
      } else {
        el.insertBefore(newImg(src, alt), el.firstChild);
      }
    });
  }

  // Full galleries: build one <figure class="frame"> per file.
  function fillGalleries(map) {
    document.querySelectorAll('[data-gallery]').forEach(function (box) {
      var slug = box.getAttribute('data-gallery');
      var label = box.getAttribute('data-label') || '';
      var files = map[slug] || [];
      var section = box.closest('section');
      box.textContent = '';
      if (!files.length) { if (section) section.style.display = 'none'; return; }
      var frag = document.createDocumentFragment();
      files.forEach(function (file, idx) {
        var fig = document.createElement('figure');
        fig.className = 'frame';
        var a = document.createElement('a');
        a.href = urlFor(slug, file); a.target = '_blank'; a.rel = 'noopener';
        a.appendChild(newImg(urlFor(slug, file), label + ' — photo ' + (idx + 1)));
        var cap = document.createElement('figcaption');
        var c1 = document.createElement('span'); c1.className = 'cat'; c1.textContent = label;
        var c2 = document.createElement('span'); c2.className = 'num';
        c2.textContent = 'FR ' + String(idx + 1).padStart(2, '0');
        cap.appendChild(c1); cap.appendChild(c2);
        fig.appendChild(a); fig.appendChild(cap);
        frag.appendChild(fig);
      });
      box.appendChild(frag);
      if (section) {
        var cnt = section.querySelector('[data-count-images]');
        if (cnt) cnt.textContent = files.length + ' image' + (files.length === 1 ? '' : 's');
      }
    });
  }

  function render(map) { fillSingles(map); fillGalleries(map); }

  function fromFallback() { return toMap(window.IMAGES_DATA); }

  fetch(ROOT + 'manifest.json', { cache: 'no-cache' })
    .then(function (r) { if (!r.ok) throw new Error('manifest ' + r.status); return r.json(); })
    .then(function (j) {
      var m = toMap(j);
      render(Object.keys(m).length ? m : fromFallback());
    })
    .catch(function () { render(fromFallback()); });
})();
