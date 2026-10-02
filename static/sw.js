const CACHE_NAME = "freechat-v1";

// キャッシュする静的アセット（軽量に保つ）
const STATIC_ASSETS = [
  "/static/css/style.css",
  "/static/js/main.js",
  "/static/manifest.json",
];

// インストール時に静的アセットをキャッシュ
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// 古いキャッシュを削除
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// フェッチ戦略:
//   静的アセット → Cache First
//   API・HTML    → Network First（リアルタイム性優先）
self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);

  // Socket.IO は SW を通さない
  if (url.pathname.startsWith("/socket.io")) return;

  // API は常にネットワーク優先
  if (url.pathname.startsWith("/api")) {
    event.respondWith(fetch(event.request));
    return;
  }

  // 静的アセットはキャッシュ優先
  if (url.pathname.startsWith("/static")) {
    event.respondWith(
      caches.match(event.request).then(cached => cached || fetch(event.request))
    );
    return;
  }

  // HTML ページはネットワーク優先、失敗時はキャッシュ
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});

// ── Web Push通知受信 ──────────────────────────────
self.addEventListener("push", event => {
  // iOS: event.data が null でも showNotification を必ず呼ぶ（呼ばないとエラー）
  let title = "FreeChat";
  let body  = "新しいメッセージがあります";
  let url   = "/";

  if (event.data) {
    try {
      const d = event.data.json();
      title = d.title || title;
      body  = d.body  || body;
      url   = d.url   || url;
    } catch(_) {
      body = event.data.text() || body;
    }
  }

  event.waitUntil(
    self.registration.showNotification(title, {
      body,
      icon:  "/static/icons/icon-192.png",
      badge: "/static/icons/icon-192.png",
      data:  { url },
    })
  );
});

// 通知タップでチャット画面を開く
self.addEventListener("notificationclick", event => {
  event.notification.close();
  const url = event.notification.data.url;
  event.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true }).then(list => {
      for (const client of list) {
        if (client.url.includes(url) && "focus" in client) return client.focus();
      }
      return clients.openWindow(url);
    })
  );
});
