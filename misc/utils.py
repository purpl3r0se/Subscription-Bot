import misc.config as config


def owner_check(id: int) -> bool:
	return id in config.owner_ids
