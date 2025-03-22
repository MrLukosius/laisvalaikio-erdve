import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput, Select

class EmbedBuilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="embed")
    async def embed_command(self, ctx):
        """Pradeda embed kūrimo procesą"""
        modal = EmbedModal()
        await ctx.send("🛠️ Įveskite informaciją apie embed:", view=modal)

class EmbedModal(Modal):
    def __init__(self):
        super().__init__(title="Sukurti Embed")
        self.title_input = TextInput(label="Pavadinimas", required=True)
        self.description_input = TextInput(label="Aprašymas", style=discord.TextStyle.long, required=True)
        self.color_input = TextInput(label="Spalva (hex, pvz., #ff0000)", required=False)
        self.image_input = TextInput(label="Paveikslėlio URL", required=False)
        self.add_item(self.title_input)
        self.add_item(self.description_input)
        self.add_item(self.color_input)
        self.add_item(self.image_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Kai vartotojas pateikia informaciją"""
        embed = discord.Embed(
            title=self.title_input.value,
            description=self.description_input.value,
            color=discord.Color.from_str(self.color_input.value) if self.color_input.value else discord.Color.blue()
        )
        if self.image_input.value:
            embed.set_image(url=self.image_input.value)
        
        view = EmbedView(embed)
        await interaction.response.send_message("🔍 Peržiūrėkite savo embed:", embed=embed, view=view)

class EmbedView(View):
    def __init__(self, embed):
        super().__init__()
        self.embed = embed

        self.add_item(Button(label="Išsiųsti", style=discord.ButtonStyle.green, custom_id="send"))
        self.add_item(Button(label="Atšaukti", style=discord.ButtonStyle.red, custom_id="cancel"))

    async def interaction_check(self, interaction: discord.Interaction):
        """Tvarko mygtukų paspaudimus"""
        if interaction.data["custom_id"] == "send":
            await interaction.response.send_message("📩 Į kurį kanalą norite siųsti?", view=ChannelSelectView(self.embed), ephemeral=True)
        elif interaction.data["custom_id"] == "cancel":
            await interaction.response.send_message("❌ Embed kūrimas atšauktas.", ephemeral=True)
            self.stop()

class ChannelSelectView(View):
    def __init__(self, embed):
        super().__init__()
        self.embed = embed
        self.add_item(Select(placeholder="Pasirinkite kanalą", options=[]))

    async def interaction_check(self, interaction: discord.Interaction):
        """Kai vartotojas pasirenka kanalą"""
        channel_id = int(interaction.data["values"][0])
        channel = interaction.guild.get_channel(channel_id)
        if channel:
            await channel.send(embed=self.embed)
            await interaction.response.send_message("✅ Embed sėkmingai išsiųstas!", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ Nepavyko rasti kanalo.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(EmbedBuilder(bot))
