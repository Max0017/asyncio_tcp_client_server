import asyncio
<<<<<<< HEAD
import click
from aioconsole import ainput
import json


class Client:
    def __init__(self, host, port, default_username: str = None):
        self.host = host
        self.port = port
        self.default_username = default_username
        self.reader = None
        self.writer = None

    async def _connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    async def _send(self, message: str):
        self.writer.write(message.encode() + b'\n')
        await self.writer.drain()

    async def _receive(self):
        data = await self.reader.readline()
        if data:
            raw_message = data.decode().strip()
            try:
                return json.loads(raw_message)
            except json.JSONDecodeError:
                return {"raw_message": raw_message} if raw_message else None
        return None

    async def run(self):
        await self._connect()
        if self.default_username:
            await self._process_command("/setname", self.default_username)

        user_input_task = asyncio.create_task(self._user_input_loop())

        await self._server_output_loop()

        user_input_task.cancel()
        self.close()

    async def _server_output_loop(self):
        while True:
            try:
                message = await self._receive()
            except ConnectionError:
                print('Disconnected from server')
                break

            if not message:
                print('Disconnected from server')
                break

            await self._process_server_output(message)

    async def _user_input_loop(self):
        while True:
            _input = await ainput()

            await self._process_input(_input)

    async def _process_server_output(self, message: dict):
        if message.get("type") == "message":
            sender = message.get("data", None)["source"]
            content = message["data"]["message"]
            print(f"{sender}: {content}")
        else:
            print(f'Raw message: {message["raw_message"]}')

    async def _process_input(self, _input: str):
        if _input[0] == '/':
            split_str = _input.split(" ", 1)
            command, rest = split_str if len(split_str) > 1 else (split_str[0], "")
            await self._process_command(command, rest)

        else:
            await self._send(f'{{"type": "message", "data": "{_input}"}}')

    async def _process_command(self, command: str, rest: str):
        match command:
            case "/setname":
                username = rest.strip(" ")
                await self._send(f'{{"type": "set-name", "data": "{username}"}}')
            case "/history":
                await self._send(f'{{"type": "history", "data": ""}}')
            case "/users":
                await self._send(f'{{"type": "users", "data": ""}}')
            case _:
                print("INVALID COMMAND!")

    def close(self):
        if self.writer:
            self.writer.close()

def main(host_address, host_port):
    client = Client(host_address, host_port)
    asyncio.run(client.run())


if __name__ == "__main__":
    host_port = 5555
    host_address = "localhost"
    main(host_address,host_port)
=======
import datetime
import random
from log_file_client import Log_File_Client
import multiprocessing

async def send_message(host, port, log_file, seq_num, client_num):
    reader, writer = await asyncio.open_connection(host, port)
    addr = writer.get_extra_info('peername')
    print(f'[{datetime.datetime.now()}],Coonected [{addr} ] client [{client_num}]')
    log = Log_File_Client()
    log.file_name = log_file  # Устанавливаем имя файла лога
    while True:
        await asyncio.sleep(random.uniform(0.3, 3))  # Случайная задержка от 300 до 3000 мс
        message = f"[{seq_num}] PING"  # Используем seq_num как переменную
        writer.write((message + '\n').encode())
        await writer.drain()
        log.set_send_date(datetime.date.today())
        log.set_send_time(datetime.datetime.now().time())
        log.set_send_text('PING')
        #print(f"request sent to server {client_num}: {message}")
        data = await reader.readline()
        response = data.decode().strip()
        log.set_get_time(datetime.datetime.now().time())
        log.set_get_text(response)

        """if response:
            print(f"received messages from the server {client_num}: {response}")
        else:
            print(f"No response received from the server")"""

        log.write()
        seq_num += 1  # Увеличиваем значение seq_num на 1

def run_clients(host, port, log_file, seq_num, client_num):
    # Создаем event loop для каждого процесса
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Запускаем корутину send_message
    try:
        loop.run_until_complete(asyncio.gather(send_message(host, port,  log_file, seq_num, client_num), stop_clients()))
    finally:
        loop.close()
async def stop_clients():
    await asyncio.sleep(300)  # Ждем 5 минут
    print("Stopping clients...")
    for task in asyncio.all_tasks():
        task.cancel()  # Отменяем все асинхронные задачи


if __name__ == "__main__":
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 12345
    # Задаем имена лог-файлов для каждого клиента
    log_files = ["client_0_log.txt", "client_1_log.txt"]
    global client_num
    client_num = 0
    # Запускаем процессы для отправки сообщений
    processes = []
    for log_file in log_files:
        # Создаем переменную-счетчик для каждого процесса
        seq_num = 0
        process = multiprocessing.Process(target=run_clients, args=(SERVER_HOST, SERVER_PORT, log_file, seq_num, client_num))
        processes.append(process)
        process.start()
        client_num += 1


        # Ждем завершения всех процессов
    for process in processes:
        process.join()
>>>>>>> e28647b (first)
