# Standard
import discord
import datetime
import asyncio
import typing
from discord.ext import commands
from typing import Union , Optional , Tuple
# Third

# Local

class Embed(discord.Embed):
    def __init__(self, color=0xffffff, fields=(), field_inline=False, **kwargs):
        super().__init__(color=color, **kwargs)
        for n, v in fields:
            self.add_field(name=n, value=v, inline=field_inline)

#thank_stella_bot
class RenlyEmbed(discord.Embed):
    """Main purpose is to get the usual setup of Embed for a command or an error embed"""
    def __init__(self, color: Union[discord.Color, int] = 0xffffff, timestamp: datetime.datetime = None,
                 fields: Tuple[Tuple[str, str]] = (), field_inline: Optional[bool] = False, **kwargs):
        super().__init__(color=color, timestamp=timestamp or discord.utils.utcnow(), **kwargs)
        for n, v in fields:
            self.add_field(name=n, value=v, inline=field_inline)

    @classmethod
    def default(cls, ctx: commands.Context, **kwargs) -> "RenlyEmbed":
        instance = cls(**kwargs)
        if ctx.author.display_avatar is not None:
            instance.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar)
        else:
            instance.set_footer(text=f"Requested by {ctx.author}")
        return instance

    @classmethod
    def to_error(cls, color: Union[discord.Color, int] = 0xFF7878, **kwargs) -> "RenlyEmbed":
        return cls(color=color, **kwargs)
    
    @classmethod
    def to_success(cls, color: Union[discord.Color, int] = 0xffffff, **kwargs) -> "RenlyEmbed":
        return cls(color=color, **kwargs)
    
    # @classmethod
    # def to_error(cls, title: Optional[str] = "Error",
    #              color: Union[discord.Color, int] = 0xFF7878, **kwargs) -> "RenlyEmbed":
    #     return cls(title=title, color=color, **kwargs)

