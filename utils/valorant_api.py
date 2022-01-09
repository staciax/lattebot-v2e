# Standard
import asyncio
import requests
import urllib3
import discord
from discord.ext import commands
from typing import Any

# Local
from .auth import Auth
from .vlr_pillow import generate_image
from .errors import UserInputErrors

# disable urllib3 warnings that might arise from making requests to 127.0.0.1
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ValorantAPI:
    def __init__(self, ctx=None, username=None, password=None, region=None, channel=None):
        self.ctx = ctx
        self.username = username
        self.password = password
        self.region = region
        self.channel:discord.TextChannel = channel
        self.session = requests.session()
        
    def fetch(self, endpoint="/") -> dict:
        response = self.session.get("https://pd.{region}.a.pvp.net{endpoint}".format(region=self.region, endpoint=endpoint), headers=self.headers, verify=False)
        return response.json()

    def store_fetch_offers(self) -> dict:
        data = self.fetch("/store/v2/storefront/{user_id}".format(user_id=self.user_id))
        return data["SkinsPanelLayout"]["SingleItemOffers"]
    
    def store_fetch_price(self) -> dict:
        data = self.fetch('/store/v1/offers/')
        return data['Offers']

    def my_daily_offter(self) -> None:
        skinid = self.store_fetch_offers()
        get_price = self.store_fetch_price()
        skin = []
        icon = []
        price = []
        for i in skinid:
            response = self.session.get(
                f"https://valorant-api.com/v1/weapons/skinlevels/{i}")
            api = response.json()
            skin.append(api['data']['displayName'])
            icon.append(api['data']['displayIcon'])
            for x in get_price:
                if x['OfferID'] == i:
                    price.append(str(*x['Cost'].values()))

        return skin, icon, price

    def build_embed(self) -> discord.Embed:
        user = self.interaction.user
        embed = discord.Embed(title=f'Valorant Store', color=0xfe676e, timestamp=discord.utils.utcnow()) #0x2F3136
        embed.set_image(url='attachment://store-offers.png')        
        embed.set_footer(text=f'Requested by {user.display_name}')
        if user.avatar is not None:
            embed.set_footer(text=f'Requested by {user.display_name}', icon_url=user.avatar)
        return embed

    async def start(self):
        ctx = self.ctx
        try:
            # defers the interaction response.
            if ctx.interaction is not None:
                await ctx.interaction.response.defer(ephemeral=True)

            # authenticate
            self.user_id, self.headers = Auth(self.username, self.password).authenticate()   

            # generate image
            file = generate_image(self.my_daily_offter())

            # build embed 
            embed = self.build_embed()
            
            await ctx.reply('\u200B', mention_author=False)
            await ctx.channel.send(embed=embed, file=file)

        except RuntimeError as e:
            raise UserInputErrors(f'{e}')
        except discord.Forbidden:
            raise UserInputErrors(f"**I don't have enough permission to send message**")
        except discord.HTTPException:
            raise UserInputErrors(f"**Sending the message failed.**")
        
        # Remind me to remove this..
        # GET name, tagline, mmr by puuid
        # r = self.session.get("https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr-history/{region}/{user_id}".format(region=self.region, user_id=self.user_id))
        # userinfo = r.json()
        # print(userinfo['name'], userinfo['tag'])
    
    # async def for_loop_send(self):        
    #     # authenticate
    #     self.user_id, self.headers = Auth(self.username, self.password).authenticate()   

    #     # generate image
    #     file = generate_image(self.my_daily_offter())

    #     # build embed 
    #     embed = discord.Embed(title="Valorant Store",color=0xfe676e, timestamp=discord.utils.utcnow())
    #     embed.set_image(url='attachment://store-offers.png')
    #     embed.set_footer(text=f"ID : {self.username}")

    #     # loop send
    #     await self.channel.send(embed=embed, file=file)
