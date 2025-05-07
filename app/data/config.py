from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = list(map(lambda x: int(x), env.list("ADMINS")))
MAX_SIZE_MB = env.int("MAX_SIZE_MB")
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024