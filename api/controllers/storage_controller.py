import os

from dotenv import load_dotenv

from config import const
from api.models.storage import Storage
from api.controllers import sqs_controller

# s3ファイル取得指定日
_BEFORE_DAY = 7
_REGS = [
    '^s3://[^/]+/dir_first/icon/b',
    '^s3://[^/]+/dir_sec/icon/down'
]


def s3_storage_management():
    """ aws s3 management

    return
    ------
      List for creating sqs messages
    """

    # call .env
    load_dotenv()
    region = os.environ.get('AWS_REGION')

    management_storage = Storage(client=const.CLIENT,
                                 bucket_name=const.BUCKET_NAME,
                                 region=region)

    data_list = management_storage.get_file_data(base_path=const.UPLOAD_BASE_PATH)

    if const.BUCKET_CREATE:
        management_storage.create_bucket()

    if const.DATA_UPLOAD:
        for data in data_list:
            management_storage.upload_data(bucket_name=const.BUCKET_NAME, upload_data=data)

    if const.DATA_DOWNLOAD:
        for data in data_list:
            management_storage.download_data(download_data=data)

    if const.DATA_DELETE:
        for data in data_list:
            management_storage.delete_data(bucket_name=const.BUCKET_NAME, delete_data=data)

    if const.BUCKET_DELETE:
        management_storage.delete_all_buckets()

    for reg in _REGS:
        file_dict = management_storage.get_timestamp_file(reg=reg)

        filter_files = management_storage.get_files_up_specified_timestamp(file_dict=file_dict, before_day=_BEFORE_DAY)

        # sqs management loop 対応
        sqs_controller.sqs_management(filter_files, queue_name='test-queue-name')

    # 最終的に存在している Bucketを確認する
    management_storage.print_bucket_name()


if __name__ == '__main__':
    pass
