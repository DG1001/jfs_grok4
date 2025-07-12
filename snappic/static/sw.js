self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('snappic-cache-v1').then((cache) => {
            return cache.addAll([
                '/',
                '/gallery',
                '/static/style.css',
                '/static/script.js',
                '/static/manifest.json',
                '/static/icon-192.png'
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
