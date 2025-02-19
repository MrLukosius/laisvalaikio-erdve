import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Nenurodyta priežastis"):
        """Išspiria narį iš serverio"""
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member.mention} buvo išmestas iš serverio. 📌 Priežastis: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Nenurodyta priežastis"):
        """Užblokuoja narį serveryje"""
        await member.ban(reason=reason)
        await ctx.send(f"⛔ {member.mention} buvo užblokuotas serveryje. 📌 Priežastis: {reason}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="Nenurodyta priežastis"):
        """Nutildo narį, priskiriant jam nutildymo rolę"""
        mute_role_id = 1333038923387113565  # Čia įrašome nutildymo rolės ID
        mute_role = ctx.guild.get_role(mute_role_id)

        if not mute_role:
            await ctx.send("⚠️ Nutildymo rolė nerasta! Patikrinkite ID.")
            return

        if mute_role in member.roles:
            await ctx.send(f"⚠️ {member.mention} jau turi nutildymo rolę!")
            return

        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f"🔇 {member.mention} buvo nutildytas. 📌 Priežastis: {reason}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Nuima nutildymo rolę nuo nario"""
        mute_role_id = 1333038923387113565  # Čia įrašome nutildymo rolės ID
        mute_role = ctx.guild.get_role(mute_role_id)

        if not mute_role:
            await ctx.send("⚠️ Nutildymo rolė nerasta! Patikrinkite ID.")
            return

        if mute_role not in member.roles:
            await ctx.send(f"⚠️ {member.mention} neturi nutildymo rolės!")
            return

        await member.remove_roles(mute_role)
        await ctx.send(f"🔊 {member.mention} buvo atmutintas!")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
