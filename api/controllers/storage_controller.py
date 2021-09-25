import os

from dotenv import load_dotenv

from config import const
from api.models import storage


def s3_storage_management():
    """ aws s3 management """

    # call .env
    load_dotenv()
    region = os.environ.get('AWS_REGION')

    management_storage = storage.Storage(client=const.CLIENT, bucket_name=const.BUCKET_NAME, region=region)

    data_list = management_storage.get_file_data(base_path='data')

    if const.BUCKET_CREATE:
        management_storage.create_bucket()

    if const.UPLOAD:
        for data in data_list:
            management_storage.upload_data(bucket_name=const.BUCKET_NAME, upload_data=data)

    if const.DOWNLOAD:
        for data in data_list:
            management_storage.download_data(download_data=data)

    if const.DELETE:
        for data in data_list:
            management_storage.delete_data(bucket_name=const.BUCKET_NAME, delete_data=data)

    if const.BUCKET_DELETE:
        management_storage.delete_all_buckets()

    # 最終的に存在している Bucketを確認する
    management_storage.print_bucket_name()
