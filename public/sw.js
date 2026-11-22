// Service Worker: legt die ganze App inkl. Sprachmodell auf dem Gerät ab, damit sie offline läuft.
// Nach Änderungen an der App die Versionsnummer erhöhen, dann holen sich Geräte die neue Fassung.
const CACHE = 'lesen-v9';
const FILES = [
  './', 'index.html', 'blaetter.html', 'manifest.webmanifest', 'icon.svg', 'icon-192.png', 'icon-512.png',
  'vosk/vosk.js', 'vosk/model-de.tar.gz'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
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
  // Seite selbst: erst Netz (für Updates), sonst gespeicherte Fassung. Alles andere: erst Speicher.
  if (e.request.mode === 'navigate') {
    e.respondWith(fetch(e.request).catch(() =>
      caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match('index.html'))));
    return;
  }
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request)));
});
