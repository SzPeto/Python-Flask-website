import datetime
import os.path

# TODO - refactor with os.path.join
class Functions:
    def __init__(self):
        self.log_file = self.create_path("Log\\log.txt")

    def create_path(self, path):
        try:
            dir_name = os.path.dirname(path)
            if dir_name and not os.path.exists(path):
                os.makedirs(dir_name)
                if os.path.exists("Log\\log.txt"):
                    self.write_log(f"Directory {dir_name} succesfully created")
        except Exception as e:
            if os.path.exists("Log\\log.txt"):
                self.write_log(f"def create_path : {e}")
            else:
                print(f"def create_path : {e}")

        return path

    def write_log(self, text):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding = "UTF-8") as log_file:
            log_file.write(f"{timestamp} - {text}\n")