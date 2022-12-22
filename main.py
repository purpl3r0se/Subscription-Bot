import os

import misc.config as config
import misc.logger as logger
import misc.tasks as tasks
from misc.variables import bot


@bot.event
async def on_ready():
	for filename in os.listdir("./cogs/commands"):
		if filename.endswith(".py"):
			await bot.load_extension(f"cogs.commands.{filename[:-3]}")
			logger.info(f"Loaded command cog: {filename[:-3]}", __name__)

	logger.info(f"Logged in as {bot.user} in {len(bot.guilds)} guild(s).", __name__)

	tasks.expiry_check.start()
	tasks.status_loop.start()


bot.run(config.token)
