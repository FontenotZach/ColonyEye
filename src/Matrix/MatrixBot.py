import asyncio

import simplematrixbotlib as botlib
from src.Utils import DBAdapter
import os
import yaml
from yaml import CLoader as Loader


yaml_path = os.path.join(os.getcwd(), os.path.pardir, 'config.yaml')

with open(yaml_path, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=Loader)


def run_bot(log):
    # creds = botlib.Creds(str(data.get('matrix')[0].get('home_server')), str(data.get('matrix')[0].get('username')), str(data.get('matrix')[0].get('password')))
    creds = botlib.Creds('https://matrix-client.matrix.org', 'colony.eye.app', 'jD7*o193nV%#pW')

    config = botlib.Config()
    config.encryption_enabled = False
    config.ignore_unverified_devices = True
    config.join_on_invite = True

    bot = botlib.Bot(creds, config)
    prefix = '!'

    db = DBAdapter.db(True)
    db.close_cursor()

    @bot.listener.on_message_event
    async def subjects(room, message):
        match = botlib.MessageMatch(room, message, bot, prefix)

        if match.is_not_from_this_bot() and match.prefix() and match.command(
                "subjects"):

            db.refresh_cursor(True)
            output = db.get_report()
            db.close_cursor()

            await bot.api.send_text_message(room.room_id, output)

            log.push_message('matrix__bot', 'subjects command executed')

    @bot.listener.on_message_event
    async def inactive(room, message):
        match = botlib.MessageMatch(room, message, bot, prefix)
        if match.is_not_from_this_bot() and match.prefix() and match.command(
                "inactive"):

            db.refresh_cursor(True)
            output = db.get_inactive()
            db.close_cursor()

            await bot.api.send_text_message(room.room_id, output)

            log.push_message('matrix__bot', 'inactive command executed')

    @bot.listener.on_message_event
    async def connections(room, message):
        match = botlib.MessageMatch(room, message, bot, prefix)
        if match.is_not_from_this_bot() and match.prefix() and match.command(
                "connections"):

            db.refresh_cursor(True)
            output = db.get_connections()
            db.close_cursor()

            await bot.api.send_text_message(room.room_id, output)

            log.push_message('matrix__bot', 'connections command executed')

    @bot.listener.on_message_event
    async def status(room, message):
        match = botlib.MessageMatch(room, message, bot, prefix)
        if match.is_not_from_this_bot() and match.prefix() and match.command(
                "status"):

            output = 'Bot is operational. Type !help for a list of commands.'

            await bot.api.send_text_message(room.room_id, output)

            log.push_message('matrix__bot', 'status command executed')

    @bot.listener.on_message_event
    async def help(room, message):
        match = botlib.MessageMatch(room, message, bot, prefix)
        if match.is_not_from_this_bot() and match.prefix() and match.command(
                "help"):

            output = '!inactive: get a list of inactive subjects\n'
            output += '!status: see if the bot is operational\n'
            output += '!connections: see each connection\'s utilization\n'
            output += '!help\n'

            await bot.api.send_text_message(room.room_id, output)

            log.push_message('matrix__bot', 'help command executed')

    while True:
        try:
            log.push_message('matrix__bot', 'Spinning up bot instance')
            bot.run()
        except asyncio.TimeoutError:
            pass

