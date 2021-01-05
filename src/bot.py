import json
import src.utils as utils

DISCORD_PING_PONG = {'statusCode': 200, 'body': json.dumps({"type": 1})}


def main(event, context):

    if not utils.valid_signature(event):
        return utils.discord_body(401, 2, 'Error Validating Discord Signature')

    body = json.loads(event['body'])

    if body['type'] == 1:
        return DISCORD_PING_PONG

    channel_id = body['channel_id']

    if body['data']['options'][0]['name'] == 'create_group':
        group_creator = f"{body['member']['user']['username']}#{body['member']['user']['discriminator']}"
        options = body['data']['options']
        group_name = ''

        for op in options:
            if op['name'] == 'group_name':
                group_name = op['value']
            elif op['name'] == 'group_size':
                group_size = op['value']
            elif op['name'] == 'group_description':
                group_des = op['value']
            else:
                return utils.discord_body(200, 4, f'{op["value"]} is not a valid option for create_group.')

        if group_name == '':
            return utils.discord_body(200, 4, 'You cannot create a group with no name.')

        if utils.create_group(channel_id, group_creator, group_name, group_size, group_des):
            return utils.discord_body(200, 3, f'Group {group_name} was created!')

        else:
            return utils.discord_body(200, 4, f'There was some issue with the command you sent.')
