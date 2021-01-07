import json
import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


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
