from discord_alert import AlertBot
from db_watcher import DBWatcher

bot = AlertBot()
watcher = None

def start_watching():
    global watcher
    watcher = DBWatcher(on_new_keys_callback=bot.notify_new_keys)
    watcher.start()

bot.set_on_ready(start_watching)
bot.run()