import configparser
import sys

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

config = configparser.ConfigParser()
config.read(sys.argv[1])

# AWS --------------
CLIENT = config['Storage']['Client']
BUCKET_NAME = config['Storage']['BucketName']

BUCKET_CREATE = config['Bucket'].getboolean('Create')
BUCKET_DELETE = config['Bucket'].getboolean('Delete')

# Management
TMP_PATH = config['Management']['TmpPath']
UPLOAD = config['Management'].getboolean('Upload')
DOWNLOAD = config['Management'].getboolean('Download')
DELETE = config['Management'].getboolean('Delete')

# Logfile
LOGFILE_PATH = config['Log']['FilePath']
LOG_FILE = config['Log']['File']
