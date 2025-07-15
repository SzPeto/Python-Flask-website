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
    import Main
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if Main.is_first_log:
        with open(self.log_file, "a", encoding = "UTF-8") as log_file:
            log_file.write(f"\n\n{timestamp} - {text}")
    else:
        with open(self.log_file, "a", encoding = "UTF-8") as log_file:
            log_file.write(f"{timestamp} - {text}")

# === Reading the entire file as a single string ===
with open("example.txt", "r") as file:
    content = file.read()
    print("READ ENTIRE FILE:\n", content)

# === Reading line by line into a list ===
with open("example.txt", "r") as file:
    lines = file.readlines()
    print("READ LINES AS LIST:")
    for line in lines:
        print(line.strip())  # strip() removes \n

# Mode strings :
#    "r"   → Read (default mode). File must exist.
#    "w"   → Write. Overwrites file if it exists, creates if not.
#    "a"   → Append. Writes at the end of the file. Creates if not exists.
#    "x"   → Create. Fails if the file already exists.
#    "b"   → Binary mode. Combine with "r", "w", "a", or "x" (e.g. "rb").
#    "t"   → Text mode. Default. Combine with others (e.g. "rt").
#    "r+"  → Read and write. File must exist.
#    "w+"  → Write and read. Overwrites if exists, creates if not.
#    "a+"  → Append and read. Creates if not exists. Reads + writes at end.
#    "x+"  → Create and read/write. Fails if file exists.