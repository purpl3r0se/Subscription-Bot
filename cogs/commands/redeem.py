import discord
from discord import app_commands
from discord.ext import commands
import time
import math

import misc.database as database
import misc.config as config


class redeemCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.command(name="redeem", description="Generate the specified amount of licenses and the type of them.")
	@app_commands.describe(license="The license you want to redeem.")
	async def redeem(self, interaction: discord.Interaction, license: str):
		if interaction.guild is None:
			await interaction.response.send_message("This command can only be ran in a server.", ephemeral=True)
			return

		db = database.connect()
		if db == "err":
			await interaction.response.send_message("Failed to connect to database", ephemeral=True)
			return

		if len(license) != 48:
			await interaction.response.send_message("Invalid license code.", ephemeral=True)
			return

		if license.lower() in {"delete", "select", "or", "and", "=", "drop", "*", "where", "like", "which"}:
			await interaction.response.send_message("Invalid license code.", ephemeral=True)
			return

		cursor = db.cursor()
		cursor.execute(f"SELECT * FROM licenses WHERE \"claimed_by\" = {interaction.user.id} AND \"expired\" = false")
		result = cursor.fetchone()
		if result != None:
			await interaction.response.send_message("You already have an ongoing subscription...", ephemeral=True)
			return

		cursor.execute(f"SELECT * FROM licenses WHERE \"license\" LIKE '{license}'")
		result = cursor.fetchone()
		if result is None:
			await interaction.response.send_message("Invalid license code.", ephemeral=True)
			return

		license_id = result[0]
		license_code = result[1]
		license_claimed_by = result[2]
		license_expires_at = result[3]
		license_created_at = result[4]
		license_created_by = result[5]
		license_type = result[6]
		license_expired = result[7]

		if license_expired == True:
			await interaction.response.send_message("This license is expired.", ephemeral=True)
			return

		if license_claimed_by == interaction.user.id:
			await interaction.response.send_message("You've already claimed this license.", ephemeral=True)
			return
		elif license_claimed_by != None:
			await interaction.response.send_message("This license is already redeemed by someone else.", ephemeral=True)
			return

		if license_type == 1:
			role_id = config.daily_role
			to_add = 86400
		elif license_type == 2:
			role_id = config.weekly_role
			to_add = 604800
		elif license_type == 3:
			role_id = config.monthly_role
			to_add = 2629800
		elif license_type == 4:
			role_id = config.lifetime_role
			to_add = 3155760000

		expires_at = math.floor(time.time()) + to_add
		cursor.execute(
			f"UPDATE licenses SET \"claimed_by\" = {interaction.user.id} , \"expires_at\" = {int(expires_at)} WHERE \"license\" LIKE '{license}'")
		db.commit()

		await interaction.user.add_roles(discord.Object(id=int(role_id)), reason="Redeemed Subscription")

		embed = discord.Embed(title="Activated license",
							  description=f"Activated license of <@&{role_id}> until <t:{expires_at}:f>",
							  color=discord.Color.random())
		await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(redeemCommand(bot))
