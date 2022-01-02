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

latte_voice = {
    'Totsuki': 861371712153845781,
    'general': 840381453779206166,
    'game': 840406478615085056,
    'music - 1': 840381486485340171,
    'music - 2': 840384917635858444,
    'listen only': 888526894738317323,
    'movie': 859656177067098142,
    'working': 890965104361889793,
    'afk': 840387675008663592,
    "don't know": 886966133176017017,
    'underworld': 873679362082369546,
    'moonlight': 875038018736644166,
    'angel': 883027485455941712,
    'death': 883059509810040884,
    'temp': 879260241286549525,
}

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