const CACHE_NAME = "horilla-pwa-v1";
const PRECACHE_URLS = ["/"];

self.addEventListener("install", (event) => {
    event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE_URLS)));
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((names) =>
            Promise.all(names.filter((name) => name !== CACHE_NAME).map((name) => caches.delete(name)))
        )
    );
    self.clients.claim();
});

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET" || new URL(event.request.url).origin !== self.location.origin) {
        return;
    }

    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request).then((cached) => cached || caches.match("/")))
    );
});
