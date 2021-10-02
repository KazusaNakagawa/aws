import configparser
import os

from dotenv import load_dotenv

from api.models import storage

config = configparser.ConfigParser()
config.read('config/awsS3.ini')

BUCKET_NAME = config['Storage']['BucketName']


def s3_storage_management():
    """ aws s3 management """

    # call .env
    load_dotenv()
    region = os.environ.get('AWS_REGION')

    management_storage = storage.Storage(client=config['Storage']['Client'],
                                         bucket_name=config['Storage']['BucketName'],
                                         region=region)

    data_list = management_storage.get_file_data(base_path=const.UPLOAD_BASE_PATH)

    if config['Bucket'].getboolean('Create'):
        management_storage.create_bucket()

    if config['S3'].getboolean('Upload'):
        for data in data_list:
            management_storage.upload_data(bucket_name=BUCKET_NAME, upload_data=data)

    if config['S3'].getboolean('Download'):
        for data in data_list:
            management_storage.download_data(download_data=data)

    if config['S3'].getboolean('Delete'):
        for data in data_list:
            management_storage.delete_data(bucket_name=BUCKET_NAME, delete_data=data)

    if config['Bucket'].getboolean('Delete'):
        management_storage.delete_all_buckets()

    # 最終的に存在している Bucketを確認する
    management_storage.print_bucket_name()
