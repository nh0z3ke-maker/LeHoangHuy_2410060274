# Bai 4.6.4 - Le Hoang Huy - 2410060274 - 24TXTHG1
# WebSocket client: nhan du lieu va tu dong ket noi lai.

import asyncio
from datetime import datetime

from tornado.httpclient import HTTPClientError
from tornado.websocket import WebSocketClosedError, websocket_connect


SERVER_URL = "ws://127.0.0.1:8888/websocket/"
RECONNECT_DELAY = 3


async def main():
    print("BAI 4.6.4 - WEBSOCKET CLIENT VOI TORNADO", flush=True)
    print("LE HOANG HUY | 2410060274 | 24TXTHG1", flush=True)
    print("Nhan Ctrl+C de dung client.", flush=True)

    while True:
        connection = None

        try:
            print(f"[DANG KET NOI] {SERVER_URL}", flush=True)

            connection = await websocket_connect(
                SERVER_URL,
                connect_timeout=10,
                ping_interval=10,
                ping_timeout=10,
            )

            print("[KET NOI] Thanh cong. Dang nhan du lieu...", flush=True)

            while True:
                message = await connection.read_message()

                if message is None:
                    print("[MAT KET NOI] Server da dong ket noi.", flush=True)
                    break

                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] [NHAN] {message}", flush=True)

        except (OSError, HTTPClientError, WebSocketClosedError) as error:
            print(f"[LOI KET NOI] {error}", flush=True)

        finally:
            if connection is not None:
                connection.close()

        print(
            f"[THU LAI] Ket noi lai sau {RECONNECT_DELAY} giay...",
            flush=True,
        )
        await asyncio.sleep(RECONNECT_DELAY)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient da dung.", flush=True)