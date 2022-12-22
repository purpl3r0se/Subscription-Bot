import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal
import time
import secrets
import io
import math

import misc.database as database
import misc.utils as utils


class generateCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.command(name="generate",
						  description="Generate the specified amount of licenses and the type of them.")
	@app_commands.describe(ltype="The type of licenses to generate.",
						   amount="How many of these licenses should be generated.")
	async def generate(self, interaction: discord.Interaction, ltype: Literal["Daily", "Weekly", "Monthly", "Lifetime"],
					   amount: int = 1):
		if not utils.owner_check(interaction.user.id):
			await interaction.response.send_message("You are not an owner.", ephemeral=True)
			return

		if ltype == "Daily":
			ltype = 1
		elif ltype == "Weekly":
			ltype = 2
		elif ltype == "Monthly":
			ltype = 3
		elif ltype == "Lifetime":
			ltype = 4

		db_s = time.time()
		db = database.connect()
		connection_time = time.time() - db_s
		if db == "err":
			await interaction.response.send_message("Failed to connect to database", ephemeral=True)
			return

		cursor = db.cursor()
		generated = ""
		execute_s = time.time()

		for _ in range(amount):
			lic = secrets.token_hex(24)
			cursor.execute(
				f"INSERT INTO licenses(\"license\", \"created_at\", \"created_by\", \"type\") VALUES ('{lic}', '{math.floor(time.time())}', {interaction.user.id}, {ltype})")
			generated += f"{lic}\n"

		db.commit()
		execution_time = time.time() - execute_s

		embed = discord.Embed(title="Generated License Keys",
							  description=f"Connection time: {connection_time}s\nExecution time: {execution_time}s\n\nGenerated {amount} licenses of type {ltype}.",
							  color=discord.Color.random())
		file = discord.File(fp=io.StringIO(generated), filename='licenses.txt')
		await interaction.response.send_message(embed=embed, file=file, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(generateCommand(bot))
