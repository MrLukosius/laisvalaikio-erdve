import discord
import asyncio
import random
import string
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

# Kanalas, kuriame nariai turi paspausti reakciją
VERIFY_CHANNEL_ID = 1333458652828536832
VERIFY_EMOJI = "✅"

# Rolės ID
VERIFIED_ROLE_ID = 1344063403668406335
UNVERIFIED_ROLE_ID = 1344063479312814080

# Saugo CAPTCHA kodus
captcha_codes = {}

class ReactionVerification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Kai narys paspaudžia reakciją"""
        if payload.channel_id != VERIFY_CHANNEL_ID or str(payload.emoji) != VERIFY_EMOJI:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        # Sukuriame CAPTCHA kodą
        captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        captcha_codes[member.id] = captcha_code

        # Sukuriame CAPTCHA nuotrauką
        captcha_path = f"captcha_{member.id}.png"
        self.generate_captcha_image(captcha_code, captcha_path)

        # Sukuriame privatų kanalą
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await guild.create_text_channel(f"patvirtinimas-{member.id}", overwrites=overwrites)

        # Įkeliame CAPTCHA į kanalą
        await channel.send(f"{member.mention}, įrašyk šį kodą, kad patvirtintum savo paskyrą:", file=discord.File(captcha_path))

        # Laukiame atsakymo
        def check(msg):
            return msg.channel == channel and msg.author == member
        
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=120)  # 120 sek. laukimo
            if msg.content.upper() == captcha_code:
                # Teisingas atsakymas, suteikiame rolę
                verified_role = guild.get_role(VERIFIED_ROLE_ID)
                unverified_role = guild.get_role(UNVERIFIED_ROLE_ID)

                if verified_role:
                    await member.add_roles(verified_role)

                if unverified_role and unverified_role in member.roles:
                    await member.remove_roles(unverified_role)

                await channel.send(f"✅ {member.mention}, sėkmingai patvirtinai savo paskyrą!", delete_after=5)
                await asyncio.sleep(5)
                await channel.delete()  # Ištriname kanalą

            else:
                await channel.send("❌ Klaidingas kodas! Bandyk iš naujo.", delete_after=10)

        except asyncio.TimeoutError:
            await channel.send("⏳ Laikas baigėsi! Bandyk iš naujo.", delete_after=10)
            await asyncio.sleep(10)
            await channel.delete()

    def generate_captcha_image(self, text, filename):
        """Generuoja CAPTCHA nuotrauką"""
        img = Image.new('RGB', (200, 80), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        draw.text((50, 30), text, fill=(0, 0, 0), font=font)
        img.save(filename)

async def setup(bot):
    await bot.add_cog(ReactionVerification(bot))
