##############################################
# Run this script locally to add bot commands
##############################################
import requests
import os
from dotenv import load_dotenv

load_dotenv()

bot_id = os.getenv('bot_id')
bot_key = os.getenv('bot_key')

url = f"https://discord.com/api/v8/applications/{bot_id}/commands"

json = {
    "name": "lfg_create_group",
    "description": "Create a group",
    "options": [
        {
            "name": "group_name",
            "description": "Group Name, Must be Unique",
            "type": 3,
            "required": True,
        },
        {
            "name": "group_size",
            "description": "Specify a group size.",
            "type": 3,
            "required": False,
        },
        {
            "name": "group_description",
            "description": "Specify a group description",
            "type": 3,
            "required": False,
        },
    ]
}


headers = {
    "Authorization": f"Bot {bot_key}"
}


def update_commands():
    r = requests.post(url, headers=headers, json=json)

    print(r.content)


def get_commands():
    r = requests.get(url, headers=headers)

    print(r.content)


# update_commands()
# get_commands()
