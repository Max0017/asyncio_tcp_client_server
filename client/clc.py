import asyncio
import random
import datetime
from server.log_file import Log_file

async def handle_client(reader, writer):
    global log
    log = Log_file()
    addr = writer.get_extra_info('peername')
    client_num = len(clients) + 1
    clients.append(client_num)
    print('address connected', addr, 'Client', client_num, '----------------------', datetime.datetime.now())
    global seq_num
    seq_num = 0
    global seq_num_get
    seq_num_get = 0
    clients_count[client_num] = (0, 0)  # Инициализируем количество запросов и ответов для нового клиента
    while True:
        get_message = await reader.readline()
        log.set_data(datetime.date.today())
        log.set_get_text(get_message)
        log.set_time((datetime.datetime.now().time()))
        print('get message adrress ', addr, get_message)
        await asyncio.sleep(random.uniform(0.1, 1))  # Случайный интервал от 100 до 1000 мс
        response = f"[{seq_num}/{seq_num_get}] PONG ({client_num})"
        writer.write((response + '\n').encode())
        await writer.drain()
        log.set_send_data(datetime.date.today())
        log.set_send_time(datetime.datetime.now().time())
        log.set_send_text(response)
        print(f"Sent response to {addr}: {response}")
        print(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,, ', addr, '........................................................',
              datetime.datetime.now())
        message = get_message.decode().strip()
        log.write()

        if random.random() < 0.1:  # 10% вероятность игнорировать запрос
            print(f"Ignoring message from {addr}: {message}")
            log.set_send_time('проигнорировано')
            log.set_send_text('проигнорировано')
            log.write()
        if get_message.strip():  # Если пришло сообщение от клиента
            seq_num_get += 1
            # Увеличиваем количество полученных запросов для текущего клиента
            clients_count[client_num] = (clients_count[client_num][0], clients_count[client_num][1] + 1)
        seq_num += 1
        await KeepLive(writer, seq_num, client_num)  # Передаем идентификатор клиента

    print(f"Connection from {addr} closed")
    writer.close()

async def start_server(host, port, ):
    global clients
    clients = []
    server = await asyncio.start_server(lambda r, w: handle_client(r, w), host, port)
    print(f"Server listening on {host}:{port}")
    await server.serve_forever()

async def KeepLive(writer, seq_num, client_num):
    await asyncio.sleep(5)
    print("KeepLive")
    response1 = f"[{seq_num}] (KeepLive) ({client_num})\n]"  # Включаем идентификатор клиента в сообщение KeepLive
    writer.write(response1.encode())
    log.set_send_time(datetime.datetime.now().time())
    log.set_send_text('KeepLive')
    await writer.drain()
    log.write()
    seq_num += 1

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345
    clients_count = {}  # Словарь для отслеживания количества запросов и ответов для каждого клиента
    asyncio.run(start_server(HOST, PORT))
