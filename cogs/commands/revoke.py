import discord
from discord import app_commands
from discord.ext import commands
import time
import math

import misc.database as database
import misc.config as config
import misc.utils as utils


class revokeCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.command(name="revoke", description="Revoke someone's license.")
	@app_commands.describe(user="The user's license which you want to revoke.")
	async def redeem(self, interaction: discord.Interaction, user: discord.Member):
		if not utils.owner_check(interaction.user.id):
			await interaction.response.send_message("You are not an owner.", ephemeral=True)
			return

		db = database.connect()
		if db == "err":
			await interaction.response.send_message("Failed to connect to database", ephemeral=True)
			return

		cursor = db.cursor()
		cursor.execute(f"SELECT * FROM licenses WHERE \"claimed_by\" = {user.id} AND \"expired\" = false")
		result = cursor.fetchone()
		if result is None:
			await interaction.response.send_message("User doesn't have a subscription...", ephemeral=True)
			return

		license_id = result[0]
		license_code = result[1]
		license_claimed_by = result[2]
		license_expires_at = result[3]
		license_created_at = result[4]
		license_created_by = result[5]
		license_type = result[6]
		license_expired = result[7]

		if license_type == 1:
			role_id = config.daily_role
		elif license_type == 2:
			role_id = config.weekly_role
		elif license_type == 3:
			role_id = config.monthly_role
		elif license_type == 4:
			role_id = config.lifetime_role

		cursor.execute(
			f"UPDATE licenses SET \"expires_at\" = {math.floor(time.time())} , \"expired\" = true WHERE \"license\" LIKE '{license_code}'")
		db.commit()

		await interaction.user.remove_roles(discord.Object(id=int(role_id)), reason="Subscription revoked.")

		embed = discord.Embed(title="Revoked license", description=f"Revoked license from {user.mention}",
							  color=discord.Color.random())
		await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(revokeCommand(bot))
