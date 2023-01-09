import random
import uuid

from handler import parse_media_message


def test_parse_media_message():
    message_id = random.randint(1, 255)
    chat_id = random.randint(1, 255)
    file_id = uuid.uuid4()

    assert parse_media_message(
        {
            'message': {
                'message_id': message_id,
                'chat': {
                    'id': chat_id,
                },
                'photo': [
                    {
                        'file_id': ''
                    },
                    {
                        'file_id': file_id
                    }
                ]
            }
        }
    ) == {
               'message_id': message_id,
               'chat_id': chat_id,
               'file_id': file_id,
           }


def test_parse_media_message_without_photo():
    message_id = random.randint(1, 255)
    chat_id = random.randint(1, 255)

    assert parse_media_message(
        {
            'message': {
                'message_id': message_id,
                'chat': {
                    'id': chat_id,
                },
                'photo': []
            }
        }
    ) is None


def test_parse_media_message_empty():
    assert parse_media_message({}) is None


def test_parse_media_message_none():
    assert parse_media_message(None) is None
