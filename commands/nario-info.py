import discord
from discord.ext import commands

class NarioInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nario-info")
    async def nario_info(self, ctx, member: discord.Member = None):
        """Parodo pasirinkto nario informaciją."""
        if member is None:
            member = ctx.author  # Jei nenurodytas, rodo apie save

        embed = discord.Embed(title=f"Nario informacija: {member.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        embed.add_field(name="🔹 Discord vardas:", value=f"{member}", inline=False)
        embed.add_field(name="🆔 ID:", value=f"{member.id}", inline=False)
        embed.add_field(name="📅 Sukurta paskyra:", value=f"{member.created_at.strftime('%Y-%m-%d %H:%M')}", inline=False)
        embed.add_field(name="📌 Prisijungė į serverį:", value=f"{member.joined_at.strftime('%Y-%m-%d %H:%M')}", inline=False)
        
        # Rolių sąrašas, neįtraukiant @everyone
        roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
        embed.add_field(name="🎭 Rolės:", value=", ".join(roles) if roles else "Nėra papildomų rolių", inline=False)

        # Patikrina, ar narys yra boostinęs serverį
        if member.premium_since:
            boost_status = f"Taip! 🚀 (nuo {member.premium_since.strftime('%Y-%m-%d %H:%M')})"
        else:
            boost_status = "Ne"

        embed.add_field(name="🚀 Ar paboostinęs serverį?", value=boost_status, inline=False)
        
        embed.set_footer(text=f"Informacija pateikta {ctx.author.display_name} prašymu")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NarioInfo(bot))
