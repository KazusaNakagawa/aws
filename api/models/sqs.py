import boto3


class SqsQueue(object):

    def __init__(self, region: str, client='sqs'):
        """ initialization parameter

        params
        ------
          client(str): sqs
          region(str): Region code
        """
        self.sqs = boto3.resource(client)
        self.region = region

    def send(self, msg_list: list, queue_name='test-queue') -> bool:
        """ send sqs message

        params
        ------
          msg_list(list): send message list
          queue_name(str): queue name
        return
        ------
          Response send sqs message (dict)
        """

        queue = self.sqs.get_queue_by_name(QueueName=queue_name)

        # send queue message
        msg_list = [{'Id': f'{i}', 'MessageBody': f"{msg}"} for i, msg in enumerate(msg_list)]

        if not msg_list:
            return False

        """
        1. 全要素数を表示
        2. 10件単位で loop 処理できるようにロジック組む
        3. 全数送信できるように調整する
        """
        for idx in range(0, len(msg_list), 10):
            queue.send_messages(Entries=msg_list[idx:idx + 10])

    def receive(self, queue_name, max_num_msg=10) -> None:
        """ receive sqs message

        params
        ------
          queue_name(str): queue name
          max_num_msg(int): The maximum number of messages to return.
        """

        queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        # >> sqs.Queue(url='https://{region}.queue.amazonaws.com/{my account}/{queue_name}')

        while True:
            # get queue message
            msg_list = queue.receive_messages(MaxNumberOfMessages=max_num_msg)
            if msg_list:
                for i, msg in enumerate(msg_list):
                    print(f"index: {i}, {msg.body}")
                    msg.delete()

            if not msg_list:
                break
