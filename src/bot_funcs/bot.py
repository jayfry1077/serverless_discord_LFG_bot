from src.utils import dynamo_bot_funcs, discord_funcs
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def create_group(guild_id, body):

    group_creator = f"{body['member']['user']['username']}#{body['member']['user']['discriminator']}"
    options = body['data']['options'][0]['options']
    group_name = ''
    group_size = 999
    group_des = ''

    for op in options:
        if op['name'] == 'name':
            group_name = op['value']
        elif op['name'] == 'size':
            group_size = op['value']
            if type(group_size) != int:
                input_type = type(group_size)
                raise Exception(
                    f'Group size must be an integer, not {input_type}.')
        elif op['name'] == 'description':
            group_des = op['value']
        else:
            raise Exception(
                f'{op["value"]} is not a valid option for create_group.')

    try:
        dynamo_bot_funcs.create_group(
            guild_id, group_creator, group_name, group_size, group_des)
        return f'Group {group_name} was created!'
    except Exception as e:
        logger.error(e)
        raise Exception(e)


def join_group(guild_id, body):

    user = f"{body['member']['user']['username']}#{body['member']['user']['discriminator']}"
    options = body['data']['options'][0]['options']
    group_name = ''

    for op in options:
        if op['name'] == 'name':
            group_name = op['value']
        else:
            raise Exception(
                f'{op["value"]} is not a valid option for join_group.')

    try:
        message = dynamo_bot_funcs.join_group(guild_id, group_name, user)

        if message is None:
            return f'{user} joined group {group_name}!'
        else:
            return message
    except Exception as e:
        logger.error(e)
        raise Exception(e)


def leave_group(guild_id, body):

    user = f"{body['member']['user']['username']}#{body['member']['user']['discriminator']}"
    options = body['data']['options'][0]['options']
    group_name = ''

    for op in options:
        if op['name'] == 'name':
            group_name = op['value']
        else:
            raise Exception(
                f'{op["value"]} is not a valid option for leave_group.')

    try:
        dynamo_bot_funcs.leave_group(guild_id, group_name, user)
        return f'{user} left group {group_name}.'
    except Exception as e:
        logger.error(e)
        raise Exception(e)


def get_group(guild_id, body):

    options = body['data']['options'][0]['options']
    group_name = ''

    for op in options:
        if op['name'] == 'name':
            group_name = op['value']
        else:
            raise Exception(
                f'{op["value"]} is not a valid option for get_group.')

    try:
        group, description, size = dynamo_bot_funcs.get_group(
            guild_id, group_name)
        user_list = [user['S'] for user in group]
        user_list = ", ".join(user_list)

        return f'```Users in group {group_name}: {user_list}\nGroup Description: {description}\nGroup Size: {size}```'

    except Exception as e:
        logger.error(e)
        raise Exception(e)


def get_groups(guild_id, body):

    avaliable = 'True'
    if 'options' in body['data']['options'][0].keys():

        options = body['data']['options'][0]['options']

        for op in options:
            if op['name'] == 'avaliable':
                avaliable = op['value']

                if avaliable in ('False', 'false'):
                    avaliable == False
            else:
                raise Exception(
                    f'{op["value"]} is not a valid option for get_group.')

    try:
        message = dynamo_bot_funcs.get_groups(
            guild_id, avaliable)

        return message

    except Exception as e:
        logger.error(e)
        raise Exception(e)
