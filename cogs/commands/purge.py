import discord
from discord import app_commands
from discord.ext import commands


class purgeCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.command(name="purge", description="Purge the specified amount of messages.")
	@app_commands.describe(amount="The amount of messages to purge.")
	@commands.has_permissions(manage_messages=True)
	async def purge(self, interaction: discord.Interaction, amount: int):
		await interaction.response.send_message(f"Purged {amount} messages.", ephemeral=True)
		await interaction.channel.purge(limit=amount + 1)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(purgeCommand(bot))
