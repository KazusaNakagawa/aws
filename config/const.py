import configparser
import sys
import re

"""
任意の設定ファイルを読み込んで、定数として格納するファイル
設定ファイルから読み込む事で、プロクラムを変更しないようにする。

params:
  sys.argv[1]: sample.ini
  
>> sample.ini
;AWS
[Storage]
Client = s3
BucketName = testbucket-yyyymmdd

[Bucket]
Create = 1
Delete = 1

[Management]
Upload = 1
Download = 0
Delete = 1
TmpPath = tmp/

# Log file
[Log]
FilePath = log/
File = bucket.log
"""


class NotReadNinFileError(Exception):
    """ Error handling when an ini file cannot be read. """


try:
    arg1 = sys.argv[1]
except IndexError as _:
    msg = ' The ini file has not been read !!! Processing stopped.\n'
    msg += 'ExSample CMD:\n'
    msg += '---------\n'
    msg += '$ python main.py sample.ini # python run\n'
    msg += '$ pytest test # test run'
    raise NotReadNinFileError(msg)

config = configparser.ConfigParser()
if re.search('.ini', arg1[-4:]):
    config.read(arg1)

# Isolating test execution. Because the ini file could not be read in the argument.
if arg1.split('/')[0] == 'test':
    ini_file_name = 'config/test.ini'
    ini_file = config.read(ini_file_name)

    # Support for docker test execution
    if not ini_file:
        config.read(f"test/{ini_file_name}")

# AWS --------------
CLIENT = config['Storage']['Client']
BUCKET_NAME = config['Storage']['BucketName']

BUCKET_CREATE = config['Bucket'].getboolean('Create')
BUCKET_DELETE = config['Bucket'].getboolean('Delete')

# Management
UPLOAD_BASE_PATH = config['Management']['UploadBasePath']
TMP_PATH = config['Management']['TmpPath']
DATA_UPLOAD = config['Management'].getboolean('Upload')
DATA_DOWNLOAD = config['Management'].getboolean('Download')
DATA_DELETE = config['Management'].getboolean('Delete')
GET_TIMESTAMP_FILE = config['Management'].getboolean('GetTimestamp_File')

# Logfile
LOGFILE_PATH = config['Log']['FilePath']
LOG_FILE = config['Log']['File']
