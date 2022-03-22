# Standard
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from difflib import get_close_matches
from datetime import time

# Third

# Local
from utils.formats import format_dt
from utils.checks import is_latte_guild
from utils_valorant.auth import Auth
from utils_valorant.api import VALORANT_API
from utils_valorant.useful import *
from utils_valorant.json_loader import data_read, data_save
from utils_valorant.view import Notify, Notify_list

class share_button(discord.ui.Button):
    def __init__(self, embeds, channel: discord.channel):
        self.embeds = embeds
        self.channel = channel
        super().__init__(
            label="Share to friends",
            style=discord.ButtonStyle.primary
        )

    async def callback(self, interaction: discord.Interaction):
        embeds = [embed for embed in list(self.embeds)]
        await self.channel.send(embeds=embeds)
        if self.view.message:
            await self.view.message.edit(view=None)

class Valorant(commands.Cog, command_attrs = dict(slash_command=True)):
    """the bot doesn't store your username/password, it only uses them to get the cookies"""
    def __init__(self, bot):
        self.bot = bot
        self.notifys_skin.start()
    
    def cog_unload(self):
        self.notifys_skin.cancel()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='valorant_icon', id=955743009138429962, animated=False)
    
    @tasks.loop(time=time(hour=0, minute=0, second=15)) #utc 00:00:15
    async def notifys_skin(self):
        try:
            data = data_read('notifys')
            user_access_token = [x['id'] for x in data]
            final_user = list(set(user_access_token))
            
            # refresh access token
            for user in final_user:
                try:
                    Auth(user_id=user).get_users()
                except:
                    pass
    
            for x in data:
                chennel = self.bot.get_channel(x['channel_id'])
                
                skin_data = VALORANT_API(x['id']).get_store_offer()
                duration = skin_data['duration']
                duration = format_dt((datetime.utcnow() + timedelta(seconds=duration)), 'R')
                
                embed = discord.Embed(color=0xfd4554)

                if x['uuid'] == skin_data['skin1']['uuid']:
                    name = skin_data['skin1']['name']
                    user_id = x['id']
                    uuid = x['uuid']
                    icon = skin_data['skin1']['icon']
                    view = Notify(user_id, uuid, name)
                    author = await self.bot.fetch_user(user_id)
                    embed = notify_send(get_tier_emoji(uuid, self.bot), name, duration, icon)
                    view.message = await chennel.send(content=f'||{author.mention}||', embed=embed, view=view)

                if x['uuid'] == skin_data['skin2']['uuid']:
                    name = skin_data['skin2']['name']
                    user_id = x['id']
                    uuid = x['uuid']
                    view = Notify(user_id, uuid, name)
                    icon = skin_data['skin2']['icon']
                    author = await self.bot.fetch_user(user_id)
                    embed = notify_send(get_tier_emoji(uuid, self.bot), name, duration, icon)
                    view.message = await chennel.send(content=f'||{author.mention}||', embed=embed, view=view)

                if x['uuid'] == skin_data['skin3']['uuid']:
                    name = skin_data['skin3']['name']
                    user_id = x['id']
                    uuid = x['uuid']
                    icon = skin_data['skin3']['icon']
                    view = Notify(user_id, uuid, name)
                    author = await self.bot.fetch_user(user_id)
                    embed = notify_send(get_tier_emoji(uuid, self.bot), name, duration, icon)
                    view.message = await chennel.send(content=f'||{author.mention}||', embed=embed, view=view)

                if x['uuid'] == skin_data['skin4']['uuid']:
                    name = skin_data['skin4']['name']
                    user_id = x['id']
                    uuid = x['uuid']
                    icon = skin_data['skin4']['icon']
                    view = Notify(user_id, uuid, name)
                    author = await self.bot.fetch_user(user_id)
                    embed = notify_send(get_tier_emoji(uuid, self.bot), name, duration, icon)
                    view.message = await chennel.send(content=f'||{author.mention}||', embed=embed, view=view)

        except (KeyError, FileNotFoundError):
            pass
        except Exception as e:
            print(f'Notify Spectified error - {e}')
    
    @notifys_skin.before_loop
    async def before_daily_send(self):
        await self.bot.wait_until_ready()
        print('Checking new store skins for notifys...')
    
    @commands.command(help="Shows my daily store")
    # @is_latte_guild()
    async def store(self, ctx, username = commands.Option(None, description="Input username"), password = commands.Option(None, description="Input password")):
        is_private = False
        if username is not None or password is not None:
            is_private = True

        if ctx.interaction is not None:
            await ctx.interaction.response.defer(ephemeral=is_private)
        
        view = discord.ui.View()

        if username and password:
            puuid, headers, region, ign = Auth(username, password).temp_auth()
            skin_list = VALORANT_API().temp_store(puuid, headers, region)
            riot_name = ign
        elif username or password:
            raise commands.CommandError("An unknown error occurred, sorry")
        else:
            data = Auth(user_id=ctx.author.id).get_users()
            
            try:
                skin_data = data_read('skins')
                if skin_data['prices']["version"] != self.bot.game_version:
                    fetch_price(ctx.author.id)
            except KeyError:
                fetch_price(ctx.author.id)
            
            skin_list = VALORANT_API(str(ctx.author.id)).get_store_offer()

            riot_name = data['IGN']
        
        embed = discord.Embed(color=0xfd4554)
        embed.description = f"Daily store for **{riot_name}** | Remaining {format_dt((datetime.utcnow() + timedelta(seconds=skin_list['duration'])), 'R')}"

        skin1 = skin_list['skin1']
        skin2 = skin_list['skin2']
        skin3 = skin_list['skin3']
        skin4 = skin_list['skin4']

        embed1 = embed_design_giorgio(skin1['uuid'], skin1['name'], skin1['price'], skin1['icon'])
        embed2 = embed_design_giorgio(skin2['uuid'], skin2['name'], skin2['price'], skin2['icon'])
        embed3 = embed_design_giorgio(skin3['uuid'], skin3['name'], skin3['price'], skin3['icon'])
        embed4 = embed_design_giorgio(skin4['uuid'], skin4['name'], skin4['price'], skin4['icon'])

        if is_private is True:
            view.add_item(share_button([embed, embed1, embed2, embed3, embed4], ctx.channel))

        view.message = await ctx.send(embeds=[embed, embed1, embed2, embed3, embed4], view=view)

    @commands.command(help="Log in with your Riot acoount")
    async def login(self, ctx, username = commands.Option(description="Input username (temp login)"), password = commands.Option(description="Input password (temp login)")):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer(ephemeral=True)

        auth = Auth(username, password, str(ctx.author.id))
        login = auth.authenticate()

        if login['auth'] == 'response':
            auth.get_entitlements_token()
            auth.get_userinfo()
            auth.get_region()

            data = data_read('users')
            embed = discord.Embed(color=0xfd4554, description='Successfully logged in as **{}**!'.format(data[str(ctx.author.id)]['IGN']))
            await ctx.send(embed=embed)
        else:
            raise commands.UserInputError('Your username or password may be incorrect!')

    @commands.command(name="2fa", help="Enter your 2FA Code")
    async def twofa(self, ctx, code:str = commands.Option(description="Input 2FA Code")):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer(ephemeral=True)
        if len(code) > 6 or len(code) < 6:
            raise commands.UserInputError('You entered the code with more than 6 or less 6.')
    
        try:
            data = data_read('users')
            twoFA_timeout = data[str(ctx.author.id)]['WaitFor2FA'] 
            future = datetime.fromtimestamp(twoFA_timeout) + timedelta(minutes=5)
            if datetime.now() > future:
                remove_user(ctx.author.id)
                raise commands.UserInputError("**2FA Timeout!**, plz `/login` again")
        except (KeyError, FileNotFoundError):
            raise commands.UserInputError("if you're not registered! plz, `/login` to register")
    
        auth = Auth(user_id=str(ctx.author.id)).give2facode(str(code))
        
        if auth:
            data = data_read('users')
            embed = discord.Embed(description='Successfully logged in as **{}**!'.format(data[str(ctx.author.id)]['IGN']), color=0xfd4554)
            return await ctx.send(embed=embed, ephemeral=True)
        raise commands.UserInputError('Invalid 2FA code!')

    @commands.command(name="logout", help="Logout and delete your accounts")
    async def logout(self, ctx):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer(ephemeral=True)
        try:
            data = data_read('users')
            del data[str(ctx.author.id)]
            data_save('users', data)
            embed = discord.Embed(description='You have been logged out bot', color=0xfd4554)
            return await ctx.send(embed=embed, ephemeral=True)
        except KeyError:
            raise commands.UserInputError("I can't logout you if you're not registered!")
        except Exception:
            raise commands.UserInputError("I can't logout you")

    @commands.command(help="Set an notify for when a particular skin is in your store")
    async def notify(self, ctx, skin:str = commands.Option(description="The name of the skin you want to notify")):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()
        
        # get_user

        data = Auth(user_id=ctx.author.id).get_users()

        #setup emoji
        await setup_emoji(ctx)

        skindata = data_read('skins')
        skindata['skins'].pop('version')
        name_list = [skindata['skins'][x]['name'] for x in skindata['skins']]
        
        skin_name = get_close_matches(skin, name_list, 1)

        if skin_name:
            notify_data = data_read('notifys')

            find_skin = [x for x in skindata['skins'] if skindata['skins'][x]['name'] == skin_name[0]]
            skin_uuid = find_skin[0]

            skin_source = skindata['skins'][skin_uuid]

            data_add = {
                "id": str(ctx.author.id),
                "uuid": skin_uuid,
                "channel_id": ctx.channel.id
            }

            notify_data.append(data_add)

            data_save('notifys', notify_data)

            emoji = get_tier_emoji(skin_uuid, self.bot)
            name = skin_source['name']
            icon = skin_source['icon']
            uuid = skin_source['uuid']

            embed = discord.Embed(description=f'Successfully set an notify for the {emoji} **{name}**', color=0xfd4554)
            embed.set_footer(text='NOTE : this is preview command')
            embed.set_thumbnail(url=icon)
            
            view = Notify(ctx.author.id, uuid, name)
            view.message = await ctx.send(embed=embed, view=view)
            return
        
        raise commands.UserInputError("Not found skin")

    @commands.command(help="Shows all your skin notify")
    async def notifys(self, ctx):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer(ephemeral=True)
        
        Auth(user_id=ctx.author.id).get_users()
        
        try:
            skin_data = data_read('skins')
            if skin_data['prices']["version"] != self.bot.game_version:
                fetch_price(ctx.author.id)
        except KeyError:
            fetch_price(ctx.author.id)

        view = Notify_list(ctx)
        await view.start()
    
    @commands.command(help="Shows your valorant point in your accounts")
    async def point(self, ctx):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()
        
        data = Auth(user_id=ctx.author.id).get_users()
        user_id = str(ctx.author.id)

        balances = get_valorant_point(user_id)

        try:
            balances = get_valorant_point(user_id)
            vp = balances["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
            rad = balances["e59aa87c-4cbf-517a-5983-6e81511be9b7"]            
        except:
            raise commands.UserInputError("Can't fetch point")

        embed = discord.Embed(title=f"{data['IGN']} Points:",color=0xfd4554)
        embed.add_field(name='Valorant Points',value=f"<:ValorantPoint:950365917613817856> {vp}", inline=True)
        embed.add_field(name='Radianite points',value=f"<:RadianitePoint:950365909636235324> {rad}", inline=True)

        await ctx.send(embed=embed)

    # @commands.command(name="nightmarket", help="Shows your nightmarket in your account")
    # async def night(self, ctx, username = commands.Option(None, description="Input username (temp login)"), password= commands.Option(None, description="Input password (temp login)")):
        
    #     is_private = False
    #     if username is not None or password is not None:
    #         is_private = True
    #     await ctx.defer(ephemeral=is_private)

    #     if username and password:
    #         puuid, headers, region, ign = Auth(username, password).temp_auth()
    #         nightmarket, duration = VALORANT_API().temp_night(puuid, headers, region)
    #         riot_name = ign
    #     elif username or password:
    #         raise commands.CommandError("An unknown error occurred, sorry")
    #     else:
    #         data = Auth(user_id=ctx.author.id).get_users()
    #         riot_name = data['IGN']
    #         nightmarket, duration = VALORANT_API(str(ctx.author.id)).store_fetch_nightmarket()
        
    #     async def night_embed(uuid, name, price, dpice):
    #         embed = discord.Embed(color=0x0F1923)
    #         embed.description = f"{get_emoji_tier_by_uuid(uuid)} **{name}**\n{get_emoji_point_bot(self.bot, 'vp')} {dpice} ~~{price}~~"
    #         embed.set_thumbnail(url=get_skin_icon(uuid))
    #         return embed
        
    #     try:
    #         embed = discord.Embed(color=0xfd4554)
    #         embed.description = f"**NightMarket for {riot_name}** | Remaining {format_dt((datetime.utcnow() + timedelta(seconds=duration)), 'R')}"

    #         skin1 = nightmarket['skin1']
    #         skin2 = nightmarket['skin2']
    #         skin3 = nightmarket['skin3']
    #         skin4 = nightmarket['skin4']
    #         skin5 = nightmarket['skin5']
    #         skin6 = nightmarket['skin6']
            
    #         embed1 = await night_embed(skin1['uuid'],skin1['name'], skin1['price'], skin1['disprice'])
    #         embed2 = await night_embed(skin2['uuid'],skin2['name'], skin2['price'], skin2['disprice'])
    #         embed3 = await night_embed(skin3['uuid'],skin3['name'], skin3['price'], skin3['disprice'])
    #         embed4 = await night_embed(skin4['uuid'],skin4['name'], skin4['price'], skin4['disprice'])
    #         embed5 = await night_embed(skin5['uuid'],skin5['name'], skin5['price'], skin5['disprice'])
    #         embed6 = await night_embed(skin6['uuid'],skin6['name'], skin6['price'], skin6['disprice'])
            
    #         await ctx.send(embeds=[embed, embed1, embed2, embed3, embed4, embed5, embed6])
    #     except Exception as e:
    #         print(e)
    #         raise commands.CommandError("An unknown error occurred, sorry")

def setup(bot):
    bot.add_cog(Valorant(bot))