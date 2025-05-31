const CACHE_NAME = 'stokapp-cache-v1';
const urlsToCache = [
  '/',
  '/static/img/pwa-icon-192.png',
  '/static/img/pwa-icon-512.png',
  // Gerekirse diğer statik dosyalar eklenebilir
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        return response || fetch(event.request);
      })
  );
}); 