import os
import pytest
from api.models.storage import Storage
from config import const

from botocore.exceptions import ClientError

from dotenv import load_dotenv

# call .env
load_dotenv()
region = os.environ.get('AWS_REGION')


class TestStorage(object):
    storage = None

    @classmethod
    def setup_class(cls):
        print('start')

    @classmethod
    def teardown_class(cls):
        print('end')

    def setup_method(self, method):
        print(f"method {method.__name__}")

    def teardown_method(self, method):
        print(f"method {method.__name__}")

    @pytest.fixture
    def _storage(self):
        return Storage(client=const.CLIENT, bucket_name='testbucket-yyyymmdd', region=region)

    def test_create_bucket(self, _storage):
        """ Tests that can create buckets """

        # clean bucket
        # bucket name duplication avoidance process
        _storage.delete_all_buckets()

        response = _storage.create_bucket()
        assert len(response['ResponseMetadata']['RequestId']) == 16
        assert len(response['ResponseMetadata']['HostId']) == 76
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    def test_create_bucket_raise_bucket_already_exists(self, _storage, bucket_name='testbucket'):
        """ If it is already created globally, an exception will be thrown. """

        _storage.bucket_name = bucket_name

        with pytest.raises(_storage.client.exceptions.BucketAlreadyExists) as err:
            raise _storage.client.exceptions.BucketAlreadyExists(
                _storage.create_bucket()
            )
        assert str(
            err.value) == 'An error occurred (BucketAlreadyExists) when calling the CreateBucket operation: ' \
                          'The requested bucket name is not available. The bucket namespace is shared by all users ' \
                          'of the system. Please select a different name and try again.'

    def test_create_bucket_raise_bucket_already_owned_by_you(self, _storage):
        """ Raising  when you try to create it using a bucket that already exists. """

        with pytest.raises(_storage.client.exceptions.BucketAlreadyOwnedByYou) as err:
            raise _storage.client.exceptions.BucketAlreadyOwnedByYou(
                _storage.create_bucket()
            )
        assert str(
            err.value) == 'An error occurred (BucketAlreadyOwnedByYou) when calling the CreateBucket operation: ' \
                          'Your previous request to create the named bucket succeeded and you already own it.'

    def test_delete_all_buckets(self, _storage):
        """ Test to delete all buckets. """

        response = _storage.delete_all_buckets()

        assert len(response[0]['ResponseMetadata']['RequestId']) == 16
        assert len(response[0]['ResponseMetadata']['HostId']) == 76
        assert response[0]['ResponseMetadata']['HTTPStatusCode'] == 204
