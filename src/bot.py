#!/usr/bin/env python3

import configparser
import discord
import logging
import re

# Setup for logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class DiscordBot(discord.Client):
    """ Base template of a discord bot. """

    def __init__(self, **options):
        """ Initialization. """
        super().__init__(**options)
        self.prefix = None
        self.admins = None
        self.textChannelId = None


    async def on_connect(self):
        """ Called when bot successfully connected to Discord. """
        print("Bot successfully connected to Discord.")


    async def on_disconnect(self):
        """ Called when bot successfully disconnected from Discord. """
        print("Bot successfully disconnected from Discord.")


    async def on_ready(self):
        """ Called when bot is done preparing the data received from Discord. """
        print("Bot is done preparing the data received from Discord.")
        print(f"Bot logged on as: '{self.user}'")


    async def on_typing(self, channel, user, when):
        """ Called when someone begins typing a message. """
        print(f"'{user}' started typing at '{when}' in channel '{channel}'.")


    async def on_message(self, message):
        """ Called when a message is created and sent. """
        print(f"'{message.author}' just sent the message: >>>\n{message.content}\n<<<")

        # Don't respond to ourselves
        if message.author == self.user:
            return


    async def on_message_delete(self, message):
        """ Called when a message is deleted. """
        print(f"Message was deleted: >>>\n{message}\n<<<")


    async def on_bulk_message_delete(self, messages):
        """ Called when messages are bulk deleted. """
        print(f"Messages were deleted: >>>")
        for message in messages:
            print(message)
        print("<<<")


    async def on_message_edit(self, before, after):
        """ Called when a message receives an update event. """
        print(f"Message: >>>\n{before}\nWas changed to:\n{after}\n<<<")


    async def on_reaction_add(self, reaction, user):
        """ Called when a message has a reaction added to it. """
        print(f"'{user}' added a reaction '{reaction}' to the message: >>>\n{reaction.message.content}\n<<<.")


    async def on_reaction_remove(self, reaction, user):
        """ Called when a message has a reaction removed from it. """
        print(f"'{user}' removed a reaction '{reaction}' from the message: >>>\n{reaction.message.content}\n<<<.")


    async def on_member_join(self, member):
        """ Called when a member joins the server. """
        print(f"'{member}' just joined the server.")


    async def on_member_remove(self, member):
        """ Called when a member leaves the server. """
        print(f"'{member}' just left the server.")



def check_config(config):
    """ Verify that config is set. """
    cfg = config["General"]["prefix"]
    if cfg == "None":
        raise Exception("Command prefix is not set.")

    cfg = config["Discord"]["admins"]
    if cfg == "None":
        raise Exception("There are no admins set to control the discord bot.")

    cfg = config["Discord"]["textChannelId"]
    if cfg == "None":
        raise Exception("Discord text channel id is not set.")

    cfg = config["Discord"]["token"]
    if cfg == "None":
        raise Exception("Discord token is not set.")



if __name__ == "__main__":
    bot = DiscordBot()

    config = configparser.ConfigParser()
    config.read("config.ini")

    check_config(config)

    bot.prefix = config["General"]["prefix"]
    bot.admins = config["Discord"]["admins"].replace(" ", "").split(",")
    bot.textChannelId = int(config["Discord"]["textChannelId"])
    token = config["Discord"]["token"]

    bot.run(token)
