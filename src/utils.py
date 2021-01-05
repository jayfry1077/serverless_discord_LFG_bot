import json
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import boto3
import datetime
import json
import os

dynamodb = boto3.client('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE_NAME', '')

DISCORD_PUBLIC_KEY = os.environ.get('DISCORD_PUBLIC_KEY', '')


# INTERACTION RESPONSE TYPES
# NAME	VALUE	DESCRIPTION
# Pong	1	ACK a Ping
# Acknowledge	2	ACK a command without sending a message, eating the user's input
# ChannelMessage	3	respond with a message, eating the user's input
# ChannelMessageWithSource	4	respond with a message, showing the user's input
# AcknowledgeWithSource	5	ACK a command without sending a message, showing the user's input


def discord_body(status_code, type, message):
    return {
        "statusCode": status_code,
        'body': json.dumps({"type": type,
                            "data": {
                                "tts": False,
                                "content": message}})
    }


def valid_signature(event):
    body = event['body']
    auth_sig = event['headers']['x-signature-ed25519']
    auth_ts = event['headers']['x-signature-timestamp']

    message = auth_ts.encode() + body.encode()

    try:
        verify_key = VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))
        verify_key.verify(message, bytes.fromhex(auth_sig))

        return True
    except BadSignatureError as e:
        print(e)
        return False


def create_group(channel_id, creator, name_of_group, group_size=999, group_description=''):

    created_at = datetime.datetime.now()
    expires_at = created_at + datetime.timedelta(days=1)
    ttl = int(expires_at.timestamp())

    try:
        dynamodb.update_item(
            Key={
                'PK': {'S': str(channel_id)},
                'SK': {'S': str(name_of_group)}
            },
            TableName=table_name,
            UpdateExpression="SET #creator = :creator, #grp_des = :grp_des, #grp_mem = :grp_mem, #ttl= :ttl",
            ExpressionAttributeNames={
                '#creator': 'creator',
                '#grp_des': 'group_description',
                '#grp_mem': 'group_members',
                '#ttl': 'TTL'
            },
            ExpressionAttributeValues={
                ':creator': {'S': creator},
                ':grp_des': {'S': group_description},
                ':grp_mem': {'S': json.dumps({'members': [], 'group_size': group_size})},
                ':ttl': {'N': str(ttl)}
            }
        )
        return True
    except Exception as e:
        print(f'Exception occured: {e}')
        return False
