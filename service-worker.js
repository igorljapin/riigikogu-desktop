// riigikogu-desktop has retired behind a redirect to riigikogu-mobile's
// desktop surface. This worker's only job now is to make sure it does not
// keep serving the old cached app forever: it wipes every cache it (or an
// earlier version of itself) created, unregisters itself, and sends any
// open window — including an already-installed standalone PWA, where the
// redirect stub's meta-refresh may not fire — to the new home.
const NEW_URL = 'https://igorljapin.github.io/riigikogu-mobile/desktop/';

self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const names = await caches.keys();
      await Promise.all(names.map((name) => caches.delete(name)));
      await self.registration.unregister();

      const windows = await self.clients.matchAll({ type: 'window' });
      await Promise.all(windows.map((client) => client.navigate(NEW_URL)));
    })()
  );
});
