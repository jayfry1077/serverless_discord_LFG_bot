##############################################
# Run this script locally to add bot commands
##############################################
import requests
import os
from dotenv import load_dotenv

load_dotenv()

bot_id = os.getenv('bot_id')
bot_key = os.getenv('bot_key')


json = {
    "name": "lfg",
    "description": "Returns a specific group.",
    "options": [
        {
            "name": "create_group",
                    "description": "Create a group.",
                    "type": 1,
                    "options": [
                        {
                            "name": "name",
                            "description": "Name of the group.",
                            "type": 3,
                            "required": True
                        },
                        {
                            "name": "size",
                            "description": "Size of the group.",
                            "type": 3,
                            "required": False
                        },
                        {
                            "name": "description",
                            "description": "Description for the group.",
                            "type": 3,
                            "required": False
                        }
                    ]
        },
        {
            "name": "join_group",
                    "description": "Join a group.",
                    "type": 1,
                    "options": [
                        {
                            "name": "name",
                            "description": "Name of the group.",
                            "type": 3,
                            "required": True
                        }
                    ]
        },
        {
            "name": "leave_group",
                    "description": "Leave a group.",
                    "type": 1,
                    "options": [
                        {
                            "name": "name",
                            "description": "Name of the group.",
                            "type": 3,
                            "required": True
                        }
                    ]
        },
        {
            "name": "get_groups",
                    "description": "Get All groups",
                    "type": 1,
                    "options": [
                        {
                            "name": "avaliable",
                            "value": True,
                            "description": "If you want to only display groups wtih open spots.",
                            "type": 3,
                            "required": False
                        }
                    ]
        },
        {
            "name": "get_group",
                    "description": "Get a group",
                    "type": 1,
                    "options": [
                        {
                            "name": "name",
                            "description": "Name of the group.",
                            "type": 3,
                            "required": True
                        }
                    ]
        }
    ]
}


headers = {
    "Authorization": f"Bot {bot_key}"
}


def update_commands(url):
    r = requests.post(url, headers=headers, json=json)

    print(r.content)


def get_commands(url):
    r = requests.get(url, headers=headers)

    print(r.content)


def delete_commands(url):
    r = requests.delete(url, headers=headers)

    print(r.content)


update_commands(f"https://discord.com/api/v8/applications/{bot_id}/commands")
# get_commands(f"https://discord.com/api/v8/applications/{bot_id}/commands")
# delete_commands(
#     f"https://discord.com/api/v8/applications/{bot_id}/commands/795912485793431583")
