import discord
from discord.ext import commands
from bot import bot

class Labas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def labas(self, ctx):
        await ctx.send("Labas! :)")

def setup(bot):
    bot.add_cog(Labas(bot))  # Čia nėra await, nes add_cog() nėra asinchroninis
