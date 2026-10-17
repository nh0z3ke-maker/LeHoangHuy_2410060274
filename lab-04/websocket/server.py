# Bai 4.6.4 - Le Hoang Huy - 2410060274 - 24TXTHG1
# WebSocket server: phat trai cay ngau nhien moi 3 giay.

import asyncio
import random
from datetime import datetime

from tornado.ioloop import PeriodicCallback
from tornado.iostream import StreamClosedError
from tornado.web import Application
from tornado.websocket import WebSocketClosedError, WebSocketHandler


HOST = "127.0.0.1"
PORT = 8888
FRUITS = ["apple", "banana", "orange", "grape", "melon"]
clients = set()


class FruitWebSocket(WebSocketHandler):
    def open(self):
        clients.add(self)
        print(
            f"[KET NOI] {self.request.remote_ip} | Tong client: {len(clients)}",
            flush=True,
        )

    def on_message(self, message):
        print(f"[CLIENT GUI] {message}", flush=True)

    def on_close(self):
        clients.discard(self)
        print(f"[NGAT KET NOI] Con {len(clients)} client.", flush=True)


async def broadcast_fruit():
    if not clients:
        return

    # Chon mot gia tri chung cho tat ca client trong moi lan phat.
    fruit = random.choice(FRUITS)
    sent_count = 0

    for client in list(clients):
        try:
            await client.write_message(fruit)
            sent_count += 1
        except (WebSocketClosedError, StreamClosedError):
            clients.discard(client)

    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"[{current_time}] [PHAT] {fruit} | {sent_count} client", flush=True)


def make_app():
    return Application(
        [(r"/websocket/", FruitWebSocket)],
        # Tornado 6.5: ping timeout khong lon hon ping interval.
        websocket_ping_interval=10,
        websocket_ping_timeout=10,
    )


async def main():
    app = make_app()
    server = app.listen(PORT, address=HOST)

    # PeriodicCallback nhan chu ky theo mili giay: 3000 ms = 3 giay.
    broadcaster = PeriodicCallback(broadcast_fruit, 3000)
    broadcaster.start()

    print("BAI 4.6.4 - WEBSOCKET VOI TORNADO", flush=True)
    print("LE HOANG HUY | 2410060274 | 24TXTHG1", flush=True)
    print(f"[SAN SANG] ws://{HOST}:{PORT}/websocket/", flush=True)
    print("Phat trai cay ngau nhien moi 3 giay khi co client.", flush=True)
    print("Nhan Ctrl+C de dung server.", flush=True)

    try:
        await asyncio.Event().wait()
    finally:
        broadcaster.stop()
        server.stop()
        for client in list(clients):
            client.close(code=1001, reason="Server stopping")
        await server.close_all_connections()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer da dung.", flush=True)
    except OSError as error:
        print(f"[LOI] {error}", flush=True)
        raise SystemExit(1)
    