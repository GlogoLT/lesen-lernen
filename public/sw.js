// Service Worker: legt die ganze App inkl. Sprachmodell auf dem Gerät ab, damit sie offline läuft.
// Nach Änderungen an der App die Versionsnummer erhöhen (auch APP_VERSION in blaetter.html).
const CACHE = 'lesen-v10';
const FILES = [
  './', 'index.html', 'blaetter.html', 'manifest.webmanifest', 'icon.svg', 'icon-192.png', 'icon-512.png',
  'vosk/vosk.js', 'vosk/model-de.tar.gz'
];
const BIG = ['vosk/model-de.tar.gz'];   // großes Sprachmodell: aus altem Speicher übernehmen statt neu laden

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    for (const f of FILES) {
      const old = BIG.includes(f) && await caches.match(f);
      // cache: 'reload' = am Browser-Zwischenspeicher vorbei immer die neueste Fassung holen
      await c.put(f, old || await fetch(new Request(f, { cache: 'reload' })));
    }
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  // Seiten: mit Internet immer frisch vom Server (ohne Zwischenspeicher) und gleich für offline merken,
  // ohne Internet die gespeicherte Fassung. Alles andere: erst Speicher.
  if (e.request.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        const r = await fetch(e.request.url, { cache: 'no-store' });
        if (r.ok) {
          const path = new URL(e.request.url).pathname.endsWith('blaetter.html') ? 'blaetter.html' : 'index.html';
          const copy = r.clone();
          caches.open(CACHE).then(c => c.put(path, copy));
        }
        return r;
      } catch {
        return (await caches.match(e.request, { ignoreSearch: true })) || caches.match('index.html');
      }
    })());
    return;
  }
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request)));
});
