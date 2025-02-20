import discord
import asyncio
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.admin_roles = [1333731772285980703, 1333030957610963022, 1338599511324360704, 1335641678031097997, 1334093147982008424, 1334093306669432833, 1334535150310264953]

    def is_admin():
        async def predicate(ctx):
            return any(role.id in ctx.author.roles for role in ctx.author.roles)
        return commands.check(predicate)

    @commands.has_permissions(kick_members=True)
    @commands.command()
    @is_admin()
    async def kick(self, ctx, member: discord.Member, *, reason="Priežastis nenurodyta"):
        if any(role.id in self.admin_roles for role in member.roles):
            await ctx.send("⛔ Administracijos narių negalima išmesti!")
            return
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member.mention} buvo išmestas. Priežastis: **{reason}**")


    @kick.error
    async def kick_error(self, ctx, error):
        await ctx.send(f"⚠️ Klaida: {error}")

    @commands.has_permissions(ban_members=True)
    @commands.command()
    @is_admin()
    async def ban(self, ctx, member: discord.Member, *, reason="Nepateikta"):
        if any(role.id in self.admin_roles for role in member.roles):
            await ctx.send("⛔ Administracijos narių negalima užblokuoti!")
            return
        await member.ban(reason=reason)
        await ctx.send(f"✅ {member.mention} buvo užblokuotas. Priežastis: **{reason}**")


    @ban.error
    async def ban_error(self, ctx, error):
        await ctx.send(f"⚠️ Klaida: {error}")

    @commands.has_permissions(mute_members=True)
    @commands.command()
    @is_admin()
    async def mute(self, ctx, member: discord.Member, mute_time: int, *, reason="Nepateikta"):
        mute_role = discord.utils.get(ctx.guild.roles, id=1333038923387113565)
        if any(role.id in self.admin_roles for role in member.roles):
            await ctx.send("⛔ Administracijos narių negalima nutildyti!")
            return
        await member.add_roles(mute_role)
        await ctx.send(f"🔇 {member.mention} buvo nutildytas **{mute_time} min**! Priežastis: **{reason}**")
        
        await asyncio.sleep(mute_time * 60)
        await member.remove_roles(mute_role)
        await ctx.send(f"✅ {member.mention}, tavo mute baigėsi.")

    
    @mute.error
    async def mute_error(self, ctx, error):
        await ctx.send(f"⚠️ Klaida: {error}")

        

async def setup(bot):
    await bot.add_cog(Moderation(bot))
