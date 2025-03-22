import discord
from discord import app_commands, ui
from discord.ext import commands

class EmbedBuilderModal(ui.Modal, title="🔧 Embed kūrimas"):
    title_input = ui.TextInput(label="Pavadinimas", required=False)
    description_input = ui.TextInput(label="Aprašymas", style=discord.TextStyle.paragraph, required=False)
    color_input = ui.TextInput(label="Spalva (hex, pvz.: #3498db)", required=False)
    image_url_input = ui.TextInput(label="Paveikslėlio URL", required=False)
    thumbnail_url_input = ui.TextInput(label="Thumbnail URL", required=False)

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    async def on_submit(self, interaction: discord.Interaction):
        color = discord.Color.default()
        if self.color_input.value:
            try:
                color = discord.Color(int(self.color_input.value.lstrip('#'), 16))
            except ValueError:
                await interaction.response.send_message("⚠️ Netinkama spalvos reikšmė! Naudokite hex formatą (pvz.: #3498db)", ephemeral=True)
                return
        
        embed = discord.Embed(
            title=self.title_input.value or "",
            description=self.description_input.value or "",
            color=color
        )
        if self.image_url_input.value:
            embed.set_image(url=self.image_url_input.value)
        if self.thumbnail_url_input.value:
            embed.set_thumbnail(url=self.thumbnail_url_input.value)
        
        view = ConfirmEmbedView(embed, self.ctx)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class ConfirmEmbedView(ui.View):
    def __init__(self, embed, ctx):
        super().__init__()
        self.embed = embed
        self.ctx = ctx

    @ui.button(label="✅ Išsiųsti", style=discord.ButtonStyle.green)
    async def send_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("Kur norite išsiųsti pranešimą?", ephemeral=True, view=ChannelSelectView(self.embed, self.ctx))

    @ui.button(label="❌ Atšaukti", style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.edit_message(content="🚫 Embed kūrimas atšauktas!", view=None, embed=None)

class ChannelSelectView(ui.View):
    def __init__(self, embed, ctx):
        super().__init__()
        self.embed = embed
        self.ctx = ctx
        
        self.add_item(ChannelDropdown(embed, ctx))

class ChannelDropdown(ui.Select):
    def __init__(self, embed, ctx):
        self.embed = embed
        self.ctx = ctx
        options = [
            discord.SelectOption(label=channel.name, value=str(channel.id))
            for channel in ctx.guild.text_channels
        ]
        super().__init__(placeholder="Pasirinkite kanalą...", options=options)

    async def callback(self, interaction: discord.Interaction):
        channel = self.ctx.guild.get_channel(int(self.values[0]))
        await channel.send(embed=self.embed)
        await interaction.response.edit_message(content=f"✅ Embed išsiųstas į {channel.mention}!", view=None, embed=None)

class EmbedBuilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="embed", description="Sukuria embed pranešimą")
    async def embed_command(self, interaction: discord.Interaction):
        modal = EmbedBuilderModal(interaction)
        await interaction.response.send_modal(modal)

async def setup(bot):
    await bot.add_cog(EmbedBuilder(bot))
