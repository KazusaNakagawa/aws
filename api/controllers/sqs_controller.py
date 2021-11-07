import os

from dotenv import load_dotenv

from api.models.sqs import SqsQueue


def sqs_management(sqs_format_list, queue_name='test-queue-name'):
    """ sqs processing run """
    # call .env
    load_dotenv()
    region = os.environ.get('AWS_REGION')

    sqs_ = SqsQueue(region=region)
    sqs_.send(msg_list=sqs_format_list, queue_name=queue_name)
    sqs_.receive(queue_name)
