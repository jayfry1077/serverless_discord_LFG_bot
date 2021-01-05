import json
import logging
from src.utils import dynamo_bot_funcs, discord_funcs

DISCORD_PING_PONG = {'statusCode': 200, 'body': json.dumps({"type": 1})}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main(event, context):

    if not discord_funcs.valid_signature(event):
        return discord_funcs.discord_body(200, 2, 'Error Validating Discord Signature')

    body = json.loads(event['body'])

    if body['type'] == 1:
        return DISCORD_PING_PONG

    channel_id = body['channel_id']

    if body['data']['name'] == 'lfg_create_group':
        group_creator = f"{body['member']['user']['username']}#{body['member']['user']['discriminator']}"
        options = body['data']['options']
        group_name = ''
        group_size = 999
        group_des = ''

        for op in options:
            if op['name'] == 'group_name':
                group_name = op['value']
            elif op['name'] == 'group_size':
                group_size = op['value']
            elif op['name'] == 'group_description':
                group_des = op['value']
            else:
                return discord_funcs.discord_body(200, 4, f'{op["value"]} is not a valid option for create_group.')

        try:
            dynamo_bot_funcs.create_group(
                channel_id, group_creator, group_name, group_size, group_des)
            return discord_funcs.discord_body(200, 3, f'Group {group_name} was created!')
        except Exception as e:
            logger.error(e)
            return discord_funcs.discord_body(200, 4, f'Unable to create group. Error: {e}.')
