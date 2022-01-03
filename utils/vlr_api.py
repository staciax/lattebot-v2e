# Standard
import requests
import urllib3
from discord.ext import commands

# Local
from .auth import Auth
from .vlr_pillow import generate_image

# disable urllib3 warnings that might arise from making requests to 127.0.0.1
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class UserInputErrors(commands.UserInputError):
    pass

class ValorantAPI:
    def __init__(self, ctx, username, password, country='tha', region='ap'):
        self.ctx = ctx
        self.auth = {
            "username": username,
            "password": password,
            "country": country
        }
        self.region = region
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

    async def start(self):
        try:
            self.user_id, self.headers, self.local_headers = Auth(self.auth).authenticate()
            file = generate_image(self.my_daily_offter())
        except RuntimeError as e:
            raise UserInputErrors(f'{e}')
        
        await self.ctx.send(file=file)