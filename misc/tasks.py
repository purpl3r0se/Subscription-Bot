import discord
from discord.ext import tasks
import time
import math

import misc.database as database
import misc.logger as logger
import misc.config as config
from misc.variables import bot


@tasks.loop(minutes=5)
async def status_loop():
	members = [member for member in bot.get_all_members() if not member.bot]

	activity = discord.Activity(
		type=discord.ActivityType.competing,
		name=f"with {len(members)} users")
	await bot.change_presence(activity=activity)


@tasks.loop(minutes=1)
async def expiry_check():
	db = database.connect()
	if db == "err":
		logger.critical("Failed to connect database", __name__)

	cursor = db.cursor()
	cursor.execute("SELECT * FROM licenses")
	results = cursor.fetchall()

	for result in results:
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

		if not license_expired and license_expires_at != None and int(license_expires_at) < math.floor(time.time()):
			logger.info(f"Subscription expired for {license_claimed_by}, type: {license_type}", __name__)
			cursor.execute(f"UPDATE licenses SET \"expired\" = true WHERE \"license\" LIKE '{license_code}'")
			db.commit()
			guild = bot.get_guild(config.main_guild)
			for member in guild.members:
				if member.id == license_claimed_by:
					for role in member.roles:
						if role.id == int(role_id):
							await member.remove_roles(discord.Object(id=int(role_id)), reason="Subscription expired.")
							await member.send(
								f"Your license has expired, if you want to extend your subscription head over to {config.store_url}")
