from re import escape
import boto3
from botocore.exceptions import ClientError
import datetime
import os

dynamodb = boto3.client('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'lfg-serverless-bot-dev')

DISCORD_PUBLIC_KEY = os.environ.get('DISCORD_PUBLIC_KEY', '')


def create_group(guild_id, creator, name_of_group, group_size, group_description):

    created_at = datetime.datetime.now()
    expires_at = created_at + datetime.timedelta(days=1)
    ttl = int(expires_at.timestamp())

    try:
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'PK': {'S': str(guild_id)},
                'SK': {'S': str(name_of_group)},
                'creator': {'S': creator},
                'group_description': {'S': group_description},
                'group_members': {'L': [{'S': creator}]},
                'group_size': {'N': str(group_size)},
                'TTL': {'N': str(ttl)},
                'availiable': {'S': 'True'},
                'guild_id': {'S': f'{str(guild_id)}#{name_of_group}'}
            },
            ConditionExpression='PK <> :PK AND SK <> :SK',
            ExpressionAttributeValues={
                ':PK': {'S': str(guild_id)},
                ':SK': {'S': str(name_of_group)}
            }
        )
        return
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise Exception('Group Already Exists.')

        else:
            raise Exception(f'Error while creating group: {e}')


def availiable_space(guild_id, name_of_group):
    try:
        response = dynamodb.get_item(
            Key={
                'PK': {'S': str(guild_id)},
                'SK': {'S': str(name_of_group)}
            },
            TableName=table_name,
        )

        if 'Item' not in response:
            raise Exception('Group Not Found')

        current_size = len(response['Item']['group_members']['L'])
        set_limit = int(response['Item']['group_size']['N'])

        if current_size >= set_limit:
            raise Exception('No space left in group.')

        return response
    except ClientError as e:
        raise Exception(f'Error checking group availibility: {e}')


def update_availiability(guild_id, name_of_group, availiability):
    try:
        dynamodb.update_item(
            Key={
                'PK': {'S': str(guild_id)},
                'SK': {'S': str(name_of_group)}
            },
            TableName=table_name,
            UpdateExpression="SET #avail = :avail",
            ExpressionAttributeNames={
                '#avail': 'availiability'
            },
            ExpressionAttributeValues={
                ':avail': {'S': availiability},
            },
            ReturnValues='ALL_NEW'
        )

        return
    except ClientError as e:
        raise Exception(e)


def join_group(guild_id, name_of_group, user):

    # Raises exception if there is no space left in group
    user_list = availiable_space(guild_id, name_of_group)

    if {'S': user} in user_list['Item']['group_members']['L']:
        raise Exception("You're already in this group")

    created_at = datetime.datetime.now()
    expires_at = created_at + datetime.timedelta(days=1)
    ttl = int(expires_at.timestamp())

    try:
        response = dynamodb.update_item(
            Key={
                'PK': {'S': str(guild_id)},
                'SK': {'S': str(name_of_group)}
            },
            TableName=table_name,
            UpdateExpression="SET #grp_mem = list_append(#grp_mem, :grp_mem) , #ttl= :ttl",
            ExpressionAttributeNames={
                '#grp_mem': 'group_members',
                '#ttl': 'TTL'
            },
            ExpressionAttributeValues={
                ':grp_mem': {'L': [{'S': user}]},
                ':ttl': {'N': str(ttl)}
            },
            ReturnValues='ALL_NEW'
        )

        current_size = len(response['Attributes']['group_members']['L'])
        set_limit = int(response['Attributes']['group_size']['N'])

        if current_size == set_limit:
            user_list = [user['S']
                         for user in response['Attributes']['group_members']['L']]
            users_ping = '@' + " @".join(user_list) + ' your group is full!'

            update_availiability(guild_id, name_of_group, 'False')

            return users_ping

        return
    except ClientError as e:
        raise Exception(f'Error While Joining Group {e}')


def get_group(guild_id, name_of_group):
    try:
        response = dynamodb.get_item(
            Key={
                'PK': {'S': str(guild_id)},
                'SK': {'S': str(name_of_group)}
            },
            TableName=table_name,
        )

        if 'Item' not in response:
            raise Exception('Group Not Found')

        return response['Item']['group_members']['L'], response['Item']['group_description']['S'], response['Item']['group_size']['N']

    except ClientError as e:
        raise Exception(f'Error finding group: {e}')


def leave_group(guild_id, name_of_group, user):

    group_list, _, _ = get_group(guild_id, name_of_group)

    user_index = group_list.index({'S': user})

    try:
        dynamodb.update_item(
            Key={
                'PK': {'S': str(guild_id)},
                'SK': {'S': str(name_of_group)}
            },
            TableName=table_name,
            UpdateExpression=f"REMOVE group_members[{user_index}]"
        )
        update_availiability(guild_id, name_of_group, True)
        return
    except ClientError as e:
        raise Exception(f'Error while leaving group {e}')


def get_groups(guild_id, only_available):
    try:
        response = dynamodb.query(
            TableName=table_name,
            IndexName='full_group_index',
            KeyConditionExpression='#availiable = :availiable and begins_with(#guild_id,:guild_id)',
            ExpressionAttributeNames={
                '#availiable': 'availiable',
                '#guild_id': 'guild_id'
            },
            ExpressionAttributeValues={
                ':availiable': {'S': only_available},
                ':guild_id': {'S': str(guild_id)}
            }
        )

        if 'Items' not in response:
            raise Exception('No Groups Found')

        discord_response = '```\n'

        if len(response['Items']) > 0:
            for group in response['Items']:
                total_members = len(group['group_members']['L'])
                group_size = int(group['group_size']['N'])
                space = group_size - total_members
                discord_response += f"Group Name:{group['SK']['S']}, Group Description: {group['group_description']['S']}, Space Left: {space}\n"

        else:
            discord_response += 'No full groups found.'

        discord_response += '```'

        return discord_response

    except ClientError as e:
        raise Exception(f'Error finding group: {e}')
