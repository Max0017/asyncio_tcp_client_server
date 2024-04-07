import asyncio
import datetime
import random
from log_file_client import Log_File_Client

async def send_message(host, port, log_file):
    global index_i
    index_i = 0
    reader, writer = await asyncio.open_connection(host, port)
    addr = writer.get_extra_info('peername')
    print(f'[{datetime.datetime.now()}], Connected [{addr}] client')
    log = Log_File_Client()
    log.file_name = log_file  # Устанавливаем имя файла лога
    seq_num = 0
    while True:
        try:
            data = None
            await asyncio.sleep(random.uniform(0.3, 3))  # Случайная задержка от 300 до 3000 мс
            message = f"[{seq_num}] PING"
            writer.write((message + '\n').encode())
            await writer.drain()

            log.set_send_date(datetime.date.today())
            log.set_send_time(datetime.datetime.now().time())
            log.set_send_text('PING')
            # print(f"request sent to server: {message}")
            data = await reader.readline()
            response = data.decode().strip()
            #print("get_message_server ",response)
            log.set_get_time(datetime.datetime.now().time())
            log.set_get_text(response)

            if "PONG" in str(data):
                i = str(data).find('[') + 1
                i1 = str(data).find('/')
                i3 = str(data).find(']')
                server_seq = int(str(data)[i:i1])
                client_req = int(str(data)[i1 + 1:i3])
                #print("___________________PONG________________")
                #print(server_seq, '/', client_req)
                if server_seq != client_req - index_i:
                    #print("======================TimeOut=======================")
                    index_i = client_req - server_seq
                    log.set_get_time("Timeout")
                    log.set_get_text("Timeout")


        except ConnectionError  as e:
            print(f"Connection error: {e}")
        seq_num += 1
        log.write()



async def main():
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 12345
    log_file = "client_1_log.txt"
    await send_message(SERVER_HOST, SERVER_PORT, log_file)

if __name__ == "__main__":
    asyncio.run(main())
