import discord
from discord.ext import commands

import misc.config as config

bot = commands.Bot(intents=discord.Intents.all(), command_prefix=config.prefix, help_command=None, case_insensitive=True, owner_ids=config.owner_ids)