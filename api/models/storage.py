import datetime

import boto3
import glob

from botocore.exceptions import ClientError
from pathlib import Path
from typing import List

from config import const
from config import logger_tool


class Storage(object):
    """
    AWS S3 Bucket 操作する model
    """

    def __init__(self, client: str, bucket_name: str, region: str):
        """ initialization parameter

        params
        ------
            client(str): s3
            bucket_name(str): choice bucket name
            region(str): Region code
        """
        self.client = boto3.client(client)
        self.resource_bucket = boto3.resource(client)
        self.bucket_name = bucket_name
        self.region = region

    @staticmethod
    def get_file_data(base_path='data', sub_path=None) -> List:
        """ dataが格納されているファイルを取得する

        ExSample
        ---------
        # only base_path
        data_list = management_storage.get_file_data(base_path='data')

        # test sub_path
        data_list = management_storage.get_file_data(base_path='data', sub_path='test1')

        params
        ------
            base_path(str): base directory
            sub_path(str): sub directory

        return
        ------
            取得したファイルを list で返す
        """
        if sub_path:
            return glob.glob(f"{base_path}/{sub_path}/*.*")

        return glob.glob(f"{base_path}/*.*")

    def create_bucket(self):
        """ Bucket を作成する処理

        params
        -------
            max_key(int): default: 2
                is_bucket_check fuc args
        """
        logger_tool.info(
            module=__name__,
            action='create',
            status='run',
            bucket_name=self.bucket_name
        )

        try:
            response = self.client.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.region}
            )

            logger_tool.info(
                module=__name__,
                action='create',
                status=200,
                bucket_name=self.bucket_name
            )
            return response

        except self.client.exceptions.BucketAlreadyExists as err:
            logger_tool.error(
                module=__name__,
                action='create',
                status=409,
                bucket_name=self.bucket_name,
                ex=err,
                msg="Bucket {} already exists!".format(err.response['Error']['BucketName']),
            )
            raise err

        except self.client.exceptions.BucketAlreadyOwnedByYou as err:
            logger_tool.error(
                module=__name__,
                action='create',
                status=409,
                bucket_name=self.bucket_name,
                ex=err,
                msg="Bucket {} already Owned By You!".format(err.response['Error']['BucketName']),
            )
            raise err

    def upload_data(self, bucket_name: str, upload_data: str):
        """
        params
        ------
            upload_data: ex) sample.png
        """
        key = upload_data.split('/')[-1]

        logger_tool.info(
            module=__name__,
            action='upload',
            status='run',
            bucket_name=bucket_name,
            data=key,
        )

        with open(upload_data, 'rb') as upload_data_file:
            self.resource_bucket.Bucket(bucket_name).put_object(Key=key, Body=upload_data_file)

        logger_tool.info(
            module=__name__,
            action='upload',
            status=200,
            bucket_name=bucket_name,
            data=key,
        )

    def download_data(self, download_data: str, base_dir='tmp') -> None:
        """
        Bucket にあるファイルをダウンロードする

        params
        ------
            download_data(str): S3にある指定データを download する
        """
        # download 用に作成
        Path(const.TMP_PATH).mkdir(exist_ok=True)

        key = download_data.split('/')[-1]

        logger_tool.info(
            module=__name__,
            action='download',
            status='run',
            bucket_name=self.bucket_name,
            data=key,
        )
        try:
            self.resource_bucket.meta.client.download_file(
                self.bucket_name, key, f"{base_dir}/{key}"
            )
            logger_tool.info(
                module=__name__,
                action='download',
                status=204,
                bucket_name=self.bucket_name,
                data=key,
            )
        except ClientError as ex:
            logger_tool.error(
                module=__name__,
                action='download',
                status=404,
                bucket_name=self.bucket_name,
                ex=ex
            )

    def delete_data(self, bucket_name: str, delete_data: str):
        """
        bucketにあるデータを削除

        params
        ------
            bucket_name(str):  Bucket name
            delete_data(data): 削除するファイル名

        return
        ------
            response: 削除が成功した結果を返すレスポンス parameter
        """

        key = delete_data.split('/')[-1]

        logger_tool.info(
            module=__name__,
            action='delete',
            status='run',
            bucket_name=bucket_name,
            data=key,
        )
        try:
            response = self.client.delete_object(
                Bucket=bucket_name,
                Key=key,
            )
            return response

        except ClientError as ex:
            logger_tool.error(
                module=__name__,
                action='delete data',
                status=404,
                bucket_name=bucket_name,
                ex=ex
            )

        logger_tool.info(
            module=__name__,
            action='delete',
            status=204,
            bucket_name=bucket_name,
            data=key,
        )

    def print_bucket_name(self):
        """
        is select buckets
        """
        buckets = [bucket.name for bucket in self.resource_bucket.buckets.all()]

        if not buckets:
            return print('No Buckets')

        if buckets:
            print('Bucket list', buckets)

    def delete_all_buckets(self):
        """
        全ての bucketを削除する

        return
        ------
            response: bucket を削除した結果を返す response parameter
        """

        buckets = list(self.resource_bucket.buckets.all())

        if buckets:
            logger_tool.info(
                module=__name__,
                action='delete',
                status='run',
                bucket_name=self.bucket_name
            )

            response = [key.delete() for key in self.resource_bucket.buckets.all()]

            logger_tool.info(
                module=__name__,
                action='delete',
                status=204,
                bucket_name=self.bucket_name
            )
            return response

    def get_timestamp_file1(self) -> dict:
        """
        Retrieve all the data in the specified bucket and return it in a dictionary with the value of last modified.

        return
        ------
        dict: {'file name': 'LastModified'}
          ex) {'data_211021.json': '2021-11-06 09:35:53'}
        """

        file_last_modified_dict = {}

        my_bucket = self.resource_bucket.Bucket(self.bucket_name)
        for obj in my_bucket.objects.all():
            obj_last_modified = str(obj.get()['LastModified'] + datetime.timedelta(hours=9))[0:-6]
            file_last_modified_dict[obj.key] = obj_last_modified

        return file_last_modified_dict

    def get_timestamp_file2(self, data_list):
        """
        Return the timestamp of the specified file stored in s3 as a dictionary.

        params
        ------
            data_list(list): s3に格納されているファイルリストと合わす
            ex) data/data_211021.json

        $ aws s3 ls s3://bucketid001
        2021-11-06 09:35:53       7613 data_211021.json

        # last_modified
        9時間前にズレてる
        data_211021.json 2021-11-06 00:35:53+00:00

        日本時間に調整する
        >> datetime.timedelta(hours=9)
        data_211021.json 2021-11-06 09:35:53+00:00

        return
        ------
            ex) {'data_211021.json': '2021-11-06 09:35:53'}
        """

        file_last_modified_dict = {}

        for key in data_list:
            # Extract the file name.
            file_name = key.split('/')[-1]
            object_summery = self.resource_bucket.ObjectSummary(self.bucket_name, key=file_name)
            # Adjust to Japan time.
            object_summery_last_modified = object_summery.last_modified + datetime.timedelta(hours=9)

            file_last_modified_dict[file_name] = str(object_summery_last_modified)[0:-6]

        return file_last_modified_dict

    def get_files_up_specified_timestamp(self, file_dict, filter_time='2021-11-06 14:00:00'):
        """ Get files up to the specified timestamp.
        """
        print(f"*** since: {filter_time} ***")

        filter_files = []
        for file_name, timestamp in file_dict.items():
            if timestamp >= filter_time:
                print(f"file: {file_name:20} timestamp: {timestamp}")
                filter_files.append(file_name)
        print('-' * 20)

        return filter_files

    def create_sqs_message_format(self, filter_files):
        """ Create file data to send SQS messages """

        return [f"s3://{self.bucket_name}/{file}" for file in filter_files]
