# serverless_discord_LFG_bot

Looking for group serverless discord bot

# Setup

The goal for me was to make this so anyone with an AWS account can deploy the stack and get a bot working. The serverless.yml file attaches will build all the infrastructure you need. It also injects the variable names you need into the lambda env variables.

My inspiration was this post on mendium. https://oozio.medium.com/serverless-discord-bot-55f95f26f743

They give really good examples to get set up with discord bots. Please check out that article if you get a chance its a great read and really help me.

There are some variables that you will have to provide yourself.

1. DISCORD_PUBLIC_KEY
2. DEV_ACCOUNT_ID

Place these into an env.json file in the same diretory as the serverless file. They will be read into the lambda environment variables.

These can be gotten from the Discord developer portal when you create your application and bot.

The other big thing you have to set up is the nacl lambda layer. Here is a guide you can follow for that.
https://medium.com/@geoff.ford_33546/creating-a-pynacl-lambda-layer-c3f2e1b6ff11

In there serverless YML there is an <ENTER YOUR LAYER ARN HERE> section that you should all your layer ARN. Otherwise the lambda will not be able to verfy the signature of the Discord POST request.

# Registering Commands

I included a script that you can use to register commands. If you want the commands that work out of the box you should run the update_commands function in the register_commands.py file. Run this locally.

For this to work you need 2 env variables you will need to get from the discord developer portal. Create a .env file in the same directory as the script to and put the following into it.

1. bot_id='YOUR BOT ID'
2. bot_key='YOUR BOT KEY'

# Bot commands

## /lfg create_group

/lfg create_group has 1 required parameter which is group name. You can optionally provide a group description and group size.

## /lfg join_group

/lfg join_group has 1 required parameter which is group name.

## /lfg leave_group

/lfg leave_group has 1 required parameter which is group name.

## /lfg get_group

/lfg get_group has 1 required parameter which is group name.

This will return inforamtion about the group.

1. Users in group
1. Group Description
1. Group Size

## /lfg get_groups

/lfg get_groups has 1 optional parameter which is avaliable.

1. Blank = True
1. True = True
1. False = False

If you provide True you will return all groups with avaliable space.
If you provide False you will provide all groups that are full.

Information returned is.

1. Group Name
1. Group Description
1. Avaliable space in group.
