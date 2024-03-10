import asyncio
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
