import logging
from logging.handlers import RotatingFileHandler
# logging.basicConfig(
#             level=logging.DEBUG,
#             format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
#             datefmt="%d/%b/%Y %H:%M:%S",)
#             #filename=log_path + self.name_account+'.log', filemode='a')

default_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] [PID:%(process)d TID:%(thread)d] %(message)s",
        "%d/%m/%Y %H:%M:%S")

file_handler = RotatingFileHandler('debug.log', maxBytes=10485760,backupCount=300, encoding='utf-8')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler.setFormatter(default_formatter)
console_handler.setFormatter(default_formatter)

logging.root.setLevel(logging.DEBUG)
logging.root.addHandler(file_handler)
logging.root.addHandler(console_handler)
