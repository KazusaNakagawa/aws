from api.controllers import storage_controller


def management():
    """ aws processing run """
    storage_controller.s3_storage_management()
