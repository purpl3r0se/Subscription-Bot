import psycopg

import misc.config as config
import misc.logger as logger


def connect(verbose: bool = False):
	try:
		if verbose:
			logger.info("Connecting to database.", __name__)
		db = psycopg.connect(dbname=config.database_name,
							 user=config.database_user,
							 password=config.database_password,
							 host=config.database_hostname,
							 port=config.database_port)
		if verbose:
			logger.info("Connected to database.", __name__)
		return db
	except Exception as e:
		logger.critical(f"Failed to connect to database, error: {e}", __name__)
		return "err"
