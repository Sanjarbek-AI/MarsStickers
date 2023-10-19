from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("IP")

CHANNELS = [
    {'name': "Test 1", "url": "https://t.me/+0gUAMSM42kYyNGVi", "id": -1001967245677},
    {'name': "Test 2", "url": "https://t.me/+osV0LMTTDU8zNTgy", "id": -1001920548167},
]
