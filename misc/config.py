import os
from dotenv import load_dotenv

load_dotenv("env/.env")
load_dotenv("env/database.env")
load_dotenv("env/subscriptions.env")

# .env

token = os.getenv("token")
prefix = os.getenv("prefix")
main_guild = int(os.getenv("main_guild"))

application_id = os.getenv("application_id")
__owner_ids = os.getenv("owner_ids").split(",")
owner_ids = []
owner_ids.extend(int(owner_id) for owner_id in __owner_ids)
store_url = os.getenv("store_url")

# database.env

database_user = os.getenv("database_user")
database_name = os.getenv("database_name")
database_password = os.getenv("database_password")
database_hostname = os.getenv("database_hostname")
database_port = os.getenv("database_port")

# subscriptions.env

daily_role = os.getenv("daily_role")
weekly_role = os.getenv("weekly_role")
monthly_role = os.getenv("monthly_role")
lifetime_role = os.getenv("lifetime_role")
