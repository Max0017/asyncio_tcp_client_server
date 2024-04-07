import asyncio
import time
import random
from threading import Thread
from dataclasses import dataclass
from collections import deque


@dataclass
class ClientConnectionContext:
    client_name: str
    writer: asyncio.StreamWriter


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client_contexts: list[ClientConnectionContext] = []
        self.output_history: deque[str] = deque(maxlen=20)

    async def KeepLive(self, writer: asyncio.StreamWriter):
        await asyncio.sleep(5)
        writer.write('KeepLive\n')
        print ("KeepLive")
        await writer.drain()

    async def new_thread(self):
        t1 = Thread(target=self.KeepLive)
        t1.start()
    async def run(self):
        server = await asyncio.start_server(self._handle_client, self.host, self.port)
        print(f'Server listening on {self.host}:{self.port}')

        async with server:
            await server.serve_forever()

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer_name = writer.get_extra_info("peername")
        context = ClientConnectionContext(f"{peer_name[0]}:{peer_name[1]}", writer)
        self.client_contexts.append(context)
        print(f"Client connected: {context.client_name}")
        while True:
            delay = random.uniform(0.1, 1)  # Случайный интервал от 100 до 1000 мс
            await asyncio.sleep(delay)
            writer.write("PING\n".encode())
            await writer.drain()
        writer.close()



async def main(host_address: str, host_port: int):
    server = Server(host_address, host_port)
    await asyncio.gather(server.run(),server.KeepLive())
host_port = 5555
host_address = "localhost"
asyncio.run(main(host_address,host_port))

if __name__ == "__main__":
    main(host_address,host_port)
