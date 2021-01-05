from re import escape
import boto3
from botocore.exceptions import ClientError
import datetime
import os

dynamodb = boto3.client('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'lfg-bot-dev')

DISCORD_PUBLIC_KEY = os.environ.get('DISCORD_PUBLIC_KEY', '')


def create_group(channel_id, creator, name_of_group, group_size, group_description):

    created_at = datetime.datetime.now()
    expires_at = created_at + datetime.timedelta(days=1)
    ttl = int(expires_at.timestamp())

    try:
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'PK': {'S': str(channel_id)},
                'SK': {'S': str(name_of_group)},
                'creator': {'S': creator},
                'group_description': {'S': group_description},
                'group_members': {'L': [{'S': creator}]},
                'group_size': {'N': str(group_size)},
                'TTL': {'N': str(ttl)}
            },
            ConditionExpression='PK <> :PK AND SK <> :SK',
            ExpressionAttributeValues={
                ':PK': {'S': str(channel_id)},
                ':SK': {'S': str(name_of_group)}
            }
        )
        return
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise Exception('Group Already Exists.')

        else:
            raise Exception(f'Error while creating group: {e}')


def availiable_space(channel_id, name_of_group):
    try:
        response = dynamodb.get_item(
            Key={
                'PK': {'S': str(channel_id)},
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

        return
    except ClientError as e:
        raise Exception(f'Error checking group availibility: {e}')


def join_group(channel_id, name_of_group, user):

    # Raises exception if there is no space left in group
    availiable_space(channel_id, name_of_group)

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
            UpdateExpression="SET #grp_mem = list_append(#grp_mem, :grp_mem) , #ttl= :ttl",
            ExpressionAttributeNames={
                '#grp_mem': 'group_members',
                '#ttl': 'TTL'
            },
            ExpressionAttributeValues={
                ':grp_mem': {'L': [{'S': user}]},
                ':ttl': {'N': str(ttl)}
            }
        )
        return
    except ClientError as e:
        raise Exception(f'Error While Joining Group {e}')


def get_group(channel_id, name_of_group):
    pass
