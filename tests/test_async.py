import asyncio
import websockets


async def fetch_updates():
    url = "ws://localhost:4242/ws"
    async with websockets.connect(url) as websocket:
        print("Connected to WebSocket")
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")
asyncio.run(fetch_updates())
