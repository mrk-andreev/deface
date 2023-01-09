import os

try:
    import unzip_requirements
except ImportError:
    pass

import json
import logging

import boto3

TOKEN = os.environ.get('TOKEN')
QUEUE_NAME = os.environ.get('QUEUE_NAME')
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)


def parse_media_message(data):
    if not data or 'message' not in data:
        return None
    message = data['message']
    message_id = message.get('message_id')
    chat_id = message.get('chat', {}).get('id')
    photos = message.get('photo', [])
    file_id = None
    if photos:
        file_id = photos[-1]['file_id']

    if not message_id or not chat_id or not file_id:
        return None

    return {
        'message_id': message_id,
        'chat_id': chat_id,
        'file_id': file_id,
    }


def handle(event, context):
    try:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
        data = json.loads(event["body"])

        message = parse_media_message(data)
        if message:
            queue.send_message(MessageBody=json.dumps(message))

        logger.info(data)
    except Exception as e:
        logging.exception(e)

    return {
        "statusCode": 200
    }
