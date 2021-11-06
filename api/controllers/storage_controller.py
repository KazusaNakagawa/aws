import os

from dotenv import load_dotenv

from api.models import storage
from config import const


def s3_storage_management():
    """ aws s3 management """

    # call .env
    load_dotenv()
    region = os.environ.get('AWS_REGION')

    management_storage = storage.Storage(client=const.CLIENT,
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

    file_dict = management_storage.get_timestamp_file1()
    filter_files = management_storage.get_files_up_specified_timestamp(file_dict)
    sqs_format_list = management_storage.create_sqs_message_format(filter_files)
    print(sqs_format_list)

    if const.GET_TIMESTAMP_FILE:
        file_ = management_storage.get_timestamp_file2(data_list=data_list)
        print(file_)

    # 最終的に存在している Bucketを確認する
    management_storage.print_bucket_name()


if __name__ == '__main__':
    pass
