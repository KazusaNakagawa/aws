# import configparser
import logging

from pathlib import Path
from config import const
# config = configparser.ConfigParser()
# config.read('config/awsS3.ini')
# # CREATE DIR
# LOG_PATH = config['Log']['LogFilePath']
# LOG_FILE = config['Log']['LogFile']

Path(const.LOGFILE_PATH).mkdir(exist_ok=True)

FORMAT = '%(asctime)s %(levelname)s:%(message)s'

logging.basicConfig(format=FORMAT, filename=Path(f"{const.LOGFILE_PATH}{const.LOG_FILE}"), level=logging.INFO)


def error(module, action, status, bucket_name: str, ex, msg=None):
    logging.error({
        'module': module,
        'action': action,
        'status': status,
        'bucket name': bucket_name,
        'except': ex,
        'msg': msg,
    })


def info(module, action=None, status=None, bucket_name=None, data=None):
    logging.info({
        'module': module,
        'action': action,
        'status': status,
        'bucket name': bucket_name,
        'data': data,
    })
