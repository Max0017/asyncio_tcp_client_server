import asyncio
import random
import datetime
from _csv import Writer
from asyncio import StreamReader, StreamWriter

from log_file import Log_file

# Функция обработки клиента
async def client_writer(client_num, get_message, writer, res_num, ignor ):
    addr = writer.get_extra_info('peername')  # Получаем адрес клиента
    res_num = res_num  # Счетчик  ответов
    if "PING" in str(get_message):
        i = str(get_message).find('[') + 1
        i1 = str(get_message).find(']')
        message = str(get_message)[i:i1]
        req_num = int(message)
        """print("--------------")
        print(req_num, " / ", res_num )"""

    # print('get_message_client ', get_message)
    await KeepLive(writer, res_num, ignor)
    # Устанавливаем данные лога
    log.set_data(datetime.date.today())
    log.set_get_text(get_message)
    log.set_time((datetime.datetime.now().time()))
    if ignor:
        response = f"[{res_num}/{req_num}] PONG ({client_num})"
        writer.write((response + '\n').encode())
        await writer.drain()
        # Устанавливаем данные лога для отправленного сообщения
        log.set_send_data(datetime.date.today())
        log.set_send_time(datetime.datetime.now().time())
        log.set_send_text(response)
        #print('Sent response to', addr, ':', response)
    log.write()



async def handle_client(reader, writer):
    # Инициализация лога
    global log
    global ignor
    res_num1 = 0
    res_num2 = 0
    ignor = True
    log = Log_file()
    client_num = len(clients)
    addr = writer.get_extra_info('peername')  # Получаем адрес клиента
    print('Connected:', addr, 'Client', client_num, 'Time:', datetime.datetime.now())
    try:
        while True:
            # Задержка перед ответом
            ignor = True
            clients.append(client_num)
            addr = writer.get_extra_info('peername')  # Получаем адрес клиента
            data = await reader.readline()  # Получаем сообщение от клиента
            if random.random() < 0.1:
                ignor = False
                #print('Ignoring message from', addr)
                log.set_send_time('проигнорировано')
                log.set_send_text('проигнорировано')
                log.write()
            await asyncio.sleep(random.uniform(0.1, 1))
            if client_num == 0:
                    await client_writer(client_num, data, writer, res_num1, ignor)
                    if ignor:
                        res_num1 += 1

            else:
                    await client_writer(client_num, data,  writer, res_num2,ignor)
                    if ignor:
                        res_num2 += 1


    except ConnectionResetError:
        print("ConnectionResetError occurred. Ignoring.")




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
async def KeepLive(writer, seq_num, ignor):
    await asyncio.sleep(5)  # Задержка на 5 секунд
    #print('KeepAlive')
    # Устанавливаем данные лога
    if ignor:
        log.set_send_time(datetime.datetime.now().time())
        log.set_send_text('KeepAlive')
        log.write()  # Записываем в лог
        response1 = f"[{seq_num}] (keepalive)\n"
        writer.write(response1.encode())
        await writer.drain()
        seq_num += 1



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
