import json
import logging
from src.utils import dynamo_bot_funcs, discord_funcs
from src.bot_funcs import bot

DISCORD_PING_PONG = {'statusCode': 200, 'body': json.dumps({"type": 1})}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main(event, context):

    print(event)

    if not discord_funcs.valid_signature(event):
        return discord_funcs.discord_body(200, 2, 'Error Validating Discord Signature')

    body = json.loads(event['body'])

    if body['type'] == 1:
        return DISCORD_PING_PONG

    guild_id = body['guild_id']
    command = body['data']['name']
    sub_command = body['data']['options'][0]['name']

    if command == 'lfg' and sub_command == 'create_group':

        try:
            message = bot.create_group(guild_id, body)
            return discord_funcs.discord_body(200, 3, message)
        except Exception as e:
            return discord_funcs.discord_body(
                200, 4, f'Unable to create group. Error: {e}.')

    elif command == 'lfg' and sub_command == 'join_group':

        try:
            message = bot.join_group(guild_id, body)
            return discord_funcs.discord_body(200, 3, message)
        except Exception as e:
            return discord_funcs.discord_body(
                200, 4, f'Unable to join group. Error: {e}.')

    elif command == 'lfg' and sub_command == 'leave_group':

        try:
            message = bot.leave_group(guild_id, body)
            return discord_funcs.discord_body(200, 3, message)
        except Exception as e:
            return discord_funcs.discord_body(
                200, 4, f'Unable to laeve group. Error: {e}.')

    elif command == 'lfg' and sub_command == 'get_group':

        try:
            message = bot.get_group(guild_id, body)
            return discord_funcs.discord_body(200, 3, message)
        except Exception as e:
            return discord_funcs.discord_body(
                200, 4, f'Unable to get group. Error: {e}.')

    elif command == 'lfg' and sub_command == 'get_groups':

        try:
            message = bot.get_groups(guild_id, body)
            return discord_funcs.discord_body(200, 3, message)
        except Exception as e:
            return discord_funcs.discord_body(
                200, 4, f'Unable to find groups. Error: {e}.')

    else:
        return discord_funcs.discord_body(200, 4, 'Unable to process command.')
