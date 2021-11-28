import discord
from typing import Any, Union
from discord.ext import commands

class CantRun(commands.CommandError):
    def __init__(self, message: str, *arg: Any):
        super().__init__(message=message, *arg)