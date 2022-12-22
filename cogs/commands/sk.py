import discord
from discord import app_commands
from discord.ext import commands
import httpx


class skCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.command(name="sk", description="Check a SK Key, to see if its valid.")
	@app_commands.describe(sk="The SK Key to check.")
	async def sk(self, interaction: discord.Interaction, sk: str):
		data = {
			"card[number]": "5142006885834320",
			"card[exp_month]": "9",
			"card[exp_year]": "2023",
			"card[cvc]": "432",
		}

		headers = {
			"Authorization": f"Bearer {sk}",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
		}

		response = httpx.post("https://api.stripe.com/v1/tokens", headers=headers, data=data).json()
		formatted_response = ""

		if "error" in str(response):
			for key, data in response["error"].items():
				if key == "client_ip":
					continue
				formatted_response += f"{key} -> {data}\n"
		else:
			for key, data in response.items():
				if key == "client_ip":
					continue
				formatted_response += f"{key} -> {data}\n"

		embed = discord.Embed(title="SK Checker", color=0xF00FFF)
		embed.add_field(name="Data", value=f"```{formatted_response.strip()}```")

		await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(skCommand(bot))
