class Log_file:
    def __init__(self):
        self.data = None
        self.time = None
        self.get_text = None
        self.send_data = None
        self.send_time = None
        self.send_text = None

    def set_data(self, data):
        self.data = data

    def set_time(self, time):
        self.time = time

    def set_get_text(self, get_text):
        self.get_text = get_text

    def set_send_data(self, send_data):
        self.send_data = send_data

    def set_send_time(self, send_time):
        self.send_time = send_time

    def set_send_text(self, send_text):
        self.send_text = send_text

    def write(self):
        with open('server_db.txt', 'a',encoding='utf-8') as file:
            if self.send_text is not None:
                if self.send_text == 'проигнорировано':
                    file.write(str(self.data) + " " + str(self.time) + " " + str(self.get_text) + " " + str(self.send_data) + " " +
                               str(self.send_time) + " " + str(self.send_text) + "\n")
                file.write(str(self.data) + " " + str(self.time) + " " + str(self.get_text) + " " + str(self.send_data) + " " +
                           str(self.send_time) + " " + str(self.send_text) + "\n")

