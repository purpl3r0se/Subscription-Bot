import discord
from discord import app_commands
from discord.ext import commands
import time
import io

import misc.database as database
import misc.utils as utils


class sqlCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.command(name="sql", description="Run the specified SQL command on the database.")
	@app_commands.describe(sql="The SQL command to run.")
	async def sql(self, interaction: discord.Interaction, sql: str):
		if not utils.owner_check(interaction.user.id):
			await interaction.response.send_message("You are not an owner.", ephemeral=True)
			return

		db_s = time.time()
		db = database.connect()
		connection_time = time.time() - db_s
		if db == "err":
			await interaction.response.send_message("Failed to connect to database", ephemeral=True)
			return

		cursor = db.cursor()
		execute_s = time.time()
		try:
			cursor.execute(sql)
			db.commit()
		except Exception as e:
			execution_time = time.time() - execute_s
			embed = discord.Embed(title="SQL Command Error.",
								  description=f"Connection time: {connection_time}s\nExecution time: {execution_time}s",
								  color=discord.Color.random())

			embed.add_field(name="Command", value=f"```sql\n{sql}```")
			embed.add_field(name="Error", value=f"```{e}```")
			await interaction.response.send_message(embed=embed, ephemeral=True)
			return

		try:
			out = cursor.fetchall()
		except Exception:
			out = "Failed to fetch any output, probably none."
		execution_time = time.time() - execute_s
		embed = discord.Embed(title="SQL Command Ran.",
								description=f"Connection time: {connection_time}s\nExecution time: {execution_time}s",
								color=discord.Color.random())

		embed.add_field(name="Command", value=f"```sql\n{sql}```")
		file = discord.File(fp=io.StringIO(str(out)), filename='output.txt')
		await interaction.response.send_message(embed=embed, file=file, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(sqlCommand(bot))
