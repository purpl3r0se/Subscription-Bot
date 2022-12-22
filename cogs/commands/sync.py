import discord
from discord.ext import commands
from typing import Literal, Optional

import misc.logger as logger
import misc.utils as utils


class syncCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command()
	async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object],
				   spec: Optional[Literal["~", "*", "^"]] = None):
		if not utils.owner_check(ctx.author.id):
			await ctx.reply("You are not an owner.", ephemeral=True)
			return

		logger.info(f"Command executed by {ctx.author} (guilds -> {guilds}) (spec -> {spec})", __name__)
		if not guilds:
			if spec == "~":
				synced = await ctx.bot.tree.sync(guild=ctx.guild)
			elif spec == "*":
				ctx.bot.tree.copy_global_to(guild=ctx.guild)
				synced = await ctx.bot.tree.sync(guild=ctx.guild)
			elif spec == "^":
				ctx.bot.tree.clear_commands(guild=ctx.guild)
				await ctx.bot.tree.sync(guild=ctx.guild)
				synced = []
			else:
				synced = await ctx.bot.tree.sync()

			logger.info(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild'}.",
						__name__)
			await ctx.reply(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild'}.")
			return

		ret = 0
		for guild in guilds:
			try:
				await ctx.bot.tree.sync(guild=guild)
			except discord.HTTPException:
				pass
			else:
				ret += 1

		logger.info(f"Synced the tree to {ret}/{len(guilds)}.", __name__)
		await ctx.reply(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(syncCommand(bot))
