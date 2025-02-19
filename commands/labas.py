import discord
from discord.ext import commands

class Labas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignoruojame botų žinutes

        lower_message = message.content.lower()  # Mažosios raidės, kad būtų jautrus tikrinimas

        if lower_message == "labas":
            await message.channel.send(f"Labas, {message.author.mention}!")
        elif lower_message in ["sveikas", "sveiki"]:
            await message.channel.send(f"Sveikas/-a, {message.author.mention}!")

async def setup(bot):
    await bot.add_cog(Labas(bot))
