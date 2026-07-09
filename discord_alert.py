import discord
import asyncio
import config


class AlertBot:
    def __init__(self):
        intents = discord.Intents.default()
        self.client = discord.Client(intents=intents)
        self.loop = None

        @self.client.event
        async def on_ready():
            self.loop = asyncio.get_running_loop()
            print(f"Logged in as {self.client.user}")
            self.on_ready_callback()

    def set_on_ready(self, callback):
        """Lets main.py hook in logic to run once the bot is connected."""
        self.on_ready_callback = callback

    def notify_new_keys(self, keys):
        """Thread-safe entrypoint — safe to call from the watchdog thread."""
        asyncio.run_coroutine_threadsafe(self._alert_users(keys), self.loop)

    async def _alert_users(self, keys):
        for key in keys:
            print(f"ALERT — new record: {key}")
            for user_id in config.RECIPIENT_IDS:
                try:
                    user = await self.client.fetch_user(user_id)
                    await user.send(f"⚠️ Attack detected — key: {key}")
                except discord.Forbidden:
                    print(f"Can't DM {user_id} — DMs disabled or no shared server.")
                except discord.NotFound:
                    print(f"User ID {user_id} not found.")
                except discord.HTTPException as e:
                    print(f"Failed to send to {user_id}: {e}")

    def run(self):
        self.client.run(config.TOKEN)