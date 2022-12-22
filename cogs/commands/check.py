import discord
from discord import app_commands
from discord.ext import commands
import httpx


class checkCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.command(name="check", description="Check to see whether a cc is valid.")
	@app_commands.describe(cc="The CC to check. (format: cc|mm|yy|cvv)")
	@commands.has_permissions(manage_messages=True)
	async def check(self, interaction: discord.Interaction, cc: str):
		await interaction.response.send_message("command disabled.", ephemeral=True)
		return

		a = httpx.get(f"http://znc-pro.fun/z/api/nonsk.php?lista={cc}&amt=0.8&curr=usd&tg_id=")
		text = a.text.replace("</span>", "").replace("#vnonsk", "").replace("Risk:", " Risk:").replace("Country:", "").replace("@ZNCLOOT", "").replace("<b>", "").replace("<br >", "").replace("#", "").replace("<br>", "").replace("</br>", "").replace("  ", " ").replace("CC: ", "").replace("Result: ", "").replace(f"{cc} ", "").replace("<span>", "").replace("<span ", "").replace("<span", " ").replace("class=\"\">", "").replace("|", "").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("➜", "").replace("✅", ":white_check_mark:").strip()
		resp = text.split(" ")[0]
		result = text.replace(f"{resp} ", "")
		await interaction.channel.send(f"User {interaction.user} Executed CC Command and got {result} as a response")
		embed = discord.Embed(title="Slash Checker", color=0x03fcec)
		embed.add_field(name="CC", value=cc)
		embed.add_field(name="Response of CC", value=result)
		await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(checkCommand(bot))