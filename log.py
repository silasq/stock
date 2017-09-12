from datetime import datetime


def write(log_file, log_str):
    message = datetime.today().strftime("%Y-%m-%d %H:%M:%S") + " : " + log_str + "\n"
    print message,
    log_file.write(message)