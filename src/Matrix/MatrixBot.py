import asyncio

import simplematrixbotlib as botlib
from src.Utils import DBAdapter


def run_bot():
    creds = botlib.Creds("https://matrix-client.matrix.org", "colony.eye.app", "jD7*o193nV%#pW")

    config = botlib.Config()
    config.emoji_verify = True
    config.ignore_unverified_devices = True

    bot = botlib.Bot(creds, config)
    prefix = '!'

    @bot.listener.on_message_event
    async def report_inactive(room, message):
        match = botlib.MessageMatch(room, message, bot, prefix)

        if match.is_not_from_this_bot() and match.prefix() and match.command(
                "subjects"):

            output = DBAdapter.get_report()

            await bot.api.send_text_message(room.room_id, output)

        if match.is_not_from_this_bot() and match.prefix() and match.command(
                "inactive"):

            output = DBAdapter.get_inactive()

            await bot.api.send_text_message(room.room_id, output)

        if match.is_not_from_this_bot() and match.prefix() and match.command(
                "connections"):

            output = DBAdapter.get_connections()

            await bot.api.send_text_message(room.room_id, output)

        if match.is_not_from_this_bot() and match.prefix() and match.command(
                "status"):

            output = 'Bot is operational. Type !help for a list of commands.'

            await bot.api.send_text_message(room.room_id, output)

        if match.is_not_from_this_bot() and match.prefix() and match.command(
                "help"):

            output = '!inactive: get a list of inactive subjects\n'
            output += '!status: see if the bot is operational\n'
            output += '!connections: see each connection\'s utilization\n'
            output += '!help\n'

            await bot.api.send_text_message(room.room_id, output)

    while True:
        try:
            bot.run()
        except:
            pass


