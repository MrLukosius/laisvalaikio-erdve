import discord
from discord.ext import commands, tasks
import aiohttp

KICK_USERNAMES = ["batuotaskatinasx", "bradegalt"]  # Kick vartotojai
DISCORD_CHANNEL_ID = 1335557698959441920  # #live kanalo ID
ROLE_ID = 1341145232485646387  # Rolės ID, kurią reikia pažymėti

class LiveNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_status = {user: False for user in KICK_USERNAMES}  # Paskutinė būsena (ar buvo LIVE)
        self.check_kick_live.start()

    async def get_kick_live_status(self, username):
        """Tikrina ar vartotojas šiuo metu transliuoja LIVE Kick platformoje."""
        url = f"https://kick.com/api/v2/channels/{username}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("livestream") is not None
                return False

    @tasks.loop(minutes=1)  # Tikrina kas 1 minutę
    async def check_kick_live(self):
        channel = self.bot.get_channel(DISCORD_CHANNEL_ID)
        for username in KICK_USERNAMES:
            is_live = await self.get_kick_live_status(username)

            if is_live and not self.last_status[username]:  # Jei pradėjo transliaciją
                role_mention = f"<@&{ROLE_ID}>"  # Tagina rolę
                embed = discord.Embed(
                    title=f"🎥 {username} pradėjo LIVE transliaciją!",
                    description=f"{role_mention}, skubėk prisijungti ir dalinkis su draugais!\n🔗 [Žiūrėti LIVE](https://kick.com/{username})",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/3/3f/Kick.com_logo.svg")  # Kick logo
                await channel.send(content=role_mention, embed=embed)

            self.last_status[username] = is_live  # Atnaujiname būseną

    @check_kick_live.before_loop
    async def before_check_kick_live(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(LiveNotifier(bot))
