from api.controllers import sqs_controller
from api.controllers import storage_controller


def management():
    """ aws processing run """
    sqs_format_list = storage_controller.s3_storage_management()
    sqs_controller.sqs_management(sqs_format_list, queue_name='test-queue-name')
