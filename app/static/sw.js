const CACHE_NAME = 'app-cache-v0';

const URLS_TO_CACHE = [
    '/',
    '/about',
    '/static/css/style.css',
    '/static/js/script.js',
    '/static/manifest.json',
    '/static/img/me.jpg',
    '/static/img/theme-toggle-light.png',
    '/static/img/theme-toggle-dark.png',
    '/static/img/app-icon-192.png',
    '/static/img/app-icon-512.png'
];

self.addEventListener('install', event => {
    const cachePromise = caches.open(CACHE_NAME)
        .then(cache => cache.addAll(URLS_TO_CACHE));
    event.waitUntil(cachePromise.then(() => self.skipWaiting()));
});

self.addEventListener('activate', event => {
    const cachePromise = caches.keys()
        .then(cacheNames => {
            const oldCaches = cacheNames.filter(cacheName =>
                cacheName.startsWith('app-cache-') && cacheName !== CACHE_NAME);
            return Promise.all(oldCaches.map(cacheName => caches.delete(cacheName)));
        });
    event.waitUntil(cachePromise);
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.open(CACHE_NAME)
            .then(cache => cache.match(event.request))
            .then(cachedResponse => cachedResponse
                ? cachedResponse
                : fetch(event.request))
    );
});
