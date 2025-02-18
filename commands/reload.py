import discord
from discord.ext import commands

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)  # Tik administratoriams
    async def reload(self, ctx, extension):
        """Perkrauna komandų modulį"""
        try:
            await self.bot.unload_extension(f"commands.{extension}")
            await self.bot.load_extension(f"commands.{extension}")
            await ctx.send(f"✅ Modulis `{extension}` sėkmingai perkrautas!")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"⚠️ Modulis `{extension}` nebuvo užkrautas!")
        except commands.ExtensionNotFound:
            await ctx.send(f"❌ Modulis `{extension}` nerastas!")
        except Exception as e:
            await ctx.send(f"🚨 Klaida perkraunant `{extension}`: `{e}`")

async def setup(bot):
    await bot.add_cog(Reload(bot))  # Prideda komandą kaip Cog
