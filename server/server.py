import asyncio
import random
import datetime
from _csv import Writer
from asyncio import StreamReader, StreamWriter

from log_file import Log_file

# Функция обработки клиента
async def client_writer(client_num, writer, reader, req_num, res_num):
    addr = writer.get_extra_info('peername')  # Получаем адрес клиента
    get_message = await reader.readline()  # Получаем сообщение от клиента
    #print('get_message_client ', get_message)
    req_num = req_num  # Счетчик запросов
    res_num = res_num  # Счетчик полученных ответов
    # Устанавливаем данные лога
    log.set_data(datetime.date.today())
    log.set_get_text(get_message)
    log.set_time((datetime.datetime.now().time()))
    response = f"[{res_num}/{req_num}] PONG ({client_num})"
    # Отправляем ответ клиенту
    writer.write((response + '\n').encode())
    await writer.drain()
    # Устанавливаем данные лога для отправленного сообщения
    log.set_send_data(datetime.date.today())
    log.set_send_time(datetime.datetime.now().time())
    log.set_send_text(response)
    #print('Sent response to', addr, ':', response)
    log.write()
    res_num += 1
    if get_message.strip():  # Если пришло сообщение от клиента
        req_num += 1


async def handle_client(reader, writer):
    # Инициализация лога
    global log
    log = Log_file()
    req_num1 = 0
    global req_num2
    req_num2 = 0
    res_num1 = 0
    res_num2 = 0
    client_num = len(clients)
    addr = writer.get_extra_info('peername')  # Получаем адрес клиента
    print('Connected:', addr, 'Client', client_num, 'Time:', datetime.datetime.now())
    while True:
        # Задержка перед ответом
        clients.append(client_num)
        await asyncio.sleep(random.uniform(0.1, 1))
        if client_num == 0:
            await client_writer(client_num, writer, reader, req_num1, res_num1)
            res_num1 += 1
            if req_num2 is not None:  # Если пришло сообщение от клиента
                req_num1 += 1
        else:
            await client_writer(client_num, writer, reader, req_num2, res_num2)
            res_num2 += 1
            if req_num2 is not None:  # Если пришло сообщение от клиента
                req_num2 += 1
        # Если сообщение игнорируется
        if random.random() < 0.1:
            #print('Ignoring message from', addr)
            log.set_send_time('ignored')
            log.set_send_text('ignored')
            log.write()
        # Отправляем KeepAlive
        await KeepLive(writer, req_num2)




async def start_server(host, port):
    global clients
    clients = []
    print(f"Server listening on {host}:{port}")
    server = await asyncio.start_server(lambda r, w: handle_client(r,w), host, port)
    await server.serve_forever()
    if server_should_stop:
        server.close()
        server.wait_closed()
        print("Server closed")
    return server

async def stop_server():
    await asyncio.sleep(300)
    global server_should_stop
    server_should_stop = True
    print("Server stopped")




# Функция отправки KeepAlive
async def KeepLive(writer, seq_num):
    await asyncio.sleep(5)  # Задержка на 5 секунд
    #print('KeepAlive')
    req_num2 = seq_num
    response1 = f"[{req_num2}] (keepalive)\n"
    writer.write(response1.encode())
    await writer.drain()
    req_num2 += 1

    # Устанавливаем данные лога
    log.set_send_time(datetime.datetime.now().time())
    log.set_send_text('KeepAlive')
    log.write()  # Записываем в лог

async def main():
    HOST = "127.0.0.1"
    PORT = 12345
    loop.create_task(start_server(HOST,PORT))
    loop.create_task(stop_server())




if __name__ == "__main__":
    server_should_stop = False
    clients = []
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
    asyncio.run(main())  # Запускаем сервер
