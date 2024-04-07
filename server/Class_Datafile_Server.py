


class Log_file:
    def __init__(self, data, time, get_text, send_data, send_time, send_text):
        self.data = data
        self.time = time
        self.get_text = get_text
        self.send_data = send_data
        self.send_time = send_time
        self.send_text = send_text
        self.get_message = self.data + self.time + self.get_text
        self.send_message = self.data + self.time + self.send_text
    def write(self):
        with open('data.txt', 'w') as file:
            if self.send_text == 'KeepLive':
                file.write(self.data, self.time, self.get_text, self.send_data, 'проигнорировано')
            file.write('\t',self.get_message, self.send_message, '\n')
        file.close(

        )
