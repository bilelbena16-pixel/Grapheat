const CACHE = 'bookingalger-v3';
const FILES = ['./', 'index.html', 'android.html', 'manifest.webmanifest',   "img/atlas.jpg",  "img/azur.jpg",  "img/celeste.jpg",  "img/cocon.jpg",  "img/dahlia.jpg",  "img/ecrin.jpg",  "img/emeraude.jpg",  "img/escale.jpg",  "img/escapade.jpg",  "img/evasion.jpg",  "img/hibiscus.jpg",  "img/horizon.jpg",  "img/icon-180.png",  "img/icon-192.png",  "img/icon-512.png",  "img/jasmin.jpg",  "img/lilas.jpg",  "img/loft.jpg",  "img/logo.png",  "img/lotus.jpg",  "img/magnolia.jpg",  "img/mark.png",  "img/nid.jpg",  "img/palmeria.jpg",  "img/petunia.jpg",  "img/refuge.jpg",  "img/riadcity.jpg",  "img/rubis.jpg",  "img/suite.jpg",  "img/villa.jpg"];
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(CACHE).then(x => x.put(e.request, c)); return r; }).catch(() => caches.match(e.request).then(r => r || caches.match('index.html'))));
});
