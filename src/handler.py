import json
import logging
from re import sub
from src.utils import dynamo_bot_funcs, discord_funcs
from src.bot_funcs import bot

DISCORD_PING_PONG = {'statusCode': 200, 'body': json.dumps({"type": 1})}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

commands = {'lfg': {'create_group': bot.create_group, 'join_group': bot.join_group,
                    'leave_group': bot.leave_group, 'get_group': bot.get_group, 'get_groups': bot.get_groups}}


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

    try:
        bot_func = commands.get(command).get(sub_command)
        message = bot_func(guild_id, body)
        return discord_funcs.discord_body(200, 3, message)
    except Exception as e:
        return discord_funcs.discord_body(200, 4, f'Unable to {sub_command}, {e}')
