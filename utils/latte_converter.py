import discord

class LatteVerifyView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label='Click for verify!', emoji='<:latte_:902674566655139881>', style=discord.ButtonStyle.primary, custom_id='lattebot_view_verifyv2x')
    async def latte_view_buttons(self, button: discord.ui.Button, interaction: discord.Interaction):
        latte_role = discord.utils.get(interaction.user.roles, id=842309176104976387)
        # bar_role = discord.utils.get(interaction.user.roles, id=854503426977038338)
        if not latte_role:
            embed = discord.Embed(color=0xffffff)
            embed.description = "Let's check out . . .\n\n﹒<#861883647070437386> \n﹒<#840380566862823425>"
            role = self.bot.latte.get_role(842309176104976387)
            lvl = self.bot.latte.get_role(854503041775566879)
            spacial = self.bot.latte.get_role(926471814757113946)
            # bar = self.bot.latte.get_role(854503426977038338)
            await interaction.user.add_roles(role, lvl, spacial)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            chat_channel = self.bot.latte.get_channel(861883647070437386)
            await chat_channel.send(f'୨୧・━━⋄✩ ₊ ˚・\nwelcome to our latte . .\n⸝⸝・{interaction.user.mention}', allowed_mentions=discord.AllowedMentions.none())

class LatteSupportVerifyView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label='Click for verify!', emoji='<:latte_:902674566655139881>', style=discord.ButtonStyle.primary, custom_id='lattebot_support_view_verifyv2x')
    async def latte_support_view_buttons(self, button: discord.ui.Button, interaction: discord.Interaction):
        member_role = discord.utils.get(interaction.user.roles, id=892907635467235399)
        if not member_role:
            guild = self.bot.get_guild(887274968012955679)
            role = guild.get_role(892907635467235399)
            embed = discord.Embed(color=0xffffff)
            embed.description = "Let's check out . . .\n\n﹒<#929815225434267749> \n﹒<#892906578334851103>"
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
fancy_text = {
    '0':'𝟶',
    '1':'𝟷',
    '2':'𝟸',
    '3':'𝟹',
    '4':'𝟺',
    '5':'𝟻',
    '6':'𝟼',
    '7':'𝟽',
    '8':'𝟾',
    '9':'𝟿',
    'a':'ᴀ',
    'b':'ʙ',
    'c':'ᴄ',
    'd':'ᴅ',
    'e':'ᴇ',
    'f':'ꜰ',
    'g':'ɢ',
    'h':'ʜ',
    'i':'ɪ',
    'j':'ᴊ',
    'k':'ᴋ',
    'l':'ʟ',
    'm':'ᴍ',
    'n':'ɴ',
    'o':'ᴏ',
    'p':'ᴘ',
    'q':'ǫ',
    'r':'ʀ',
    's':'ꜱ',
    't':'ᴛ',
    'u':'ᴜ',
    'v':'ᴠ',
    'w':'ᴡ',
    'x':'x',
    'y':'ʏ',
    'z':'ᴢ',
    ' ': ' '
}