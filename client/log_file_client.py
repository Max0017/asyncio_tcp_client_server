class Log_File_Client:
    def __init__(self):
        self.file_name = None
        self.send_date = None
        self.send_time = None
        self.send_text = None
        self.get_time = None
        self.get_text = None

    def set_send_date(self, send_date):
        self.send_date = send_date

    def set_get_time(self, get_time):
        self.get_time = get_time

    def set_get_text(self, get_text):
        self.get_text = get_text

    def set_send_time(self, send_time):
        self.send_time = send_time

    def set_send_text(self, send_text):
        self.send_text = send_text

    def write(self):
        with open(str(self.file_name), 'a',encoding='utf-8') as file:
            if 'keepalive' in self.get_text:
                file.write(str(self.get_time) + "; " + str(self.get_text) + "; \n")
            else:
                file.write(str(self.send_date) + "; " + str(self.send_time) + "; " + str(self.send_text) + "; " + str(self.get_time) + "; " +
                           str(self.get_text) + "; \n")
