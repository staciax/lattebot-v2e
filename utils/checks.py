from discord.ext import commands

# The permission system of the bot is based on a "just works" basis
# You have permissions and the bot has permissions. If you meet the permissions
# required to execute the command (and the bot does as well) then it goes through
# and you can execute the command.
# Certain permissions signify if the person is a moderator (Manage Server) or an
# admin (Administrator). Having these signify certain bypasses.
# Of course, the owner will always be able to execute commands.
#@checks.admin_or_permissions(manage_roles=True)

async def check_permissions(ctx, perms, *, check=all):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())

def has_permissions(*, check=all, **perms):
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)
    return commands.check(pred)

async def check_guild_permissions(ctx, perms, *, check=all):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    if ctx.guild is None:
        return False

    resolved = ctx.author.guild_permissions
    return check(getattr(resolved, name, None) == value for name, value in perms.items())

def has_guild_permissions(*, check=all, **perms):
    async def pred(ctx):
        return await check_guild_permissions(ctx, perms, check=check)
    return commands.check(pred)

# These do not take channel overrides into account

def is_mod():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'manage_guild': True})
    return commands.check(pred)

def is_admin():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'administrator': True})
    return commands.check(pred)

def mod_or_permissions(**perms):
    perms['manage_guild'] = True
    async def predicate(ctx):
        return await check_guild_permissions(ctx, perms, check=any)
    return commands.check(predicate)

def admin_or_permissions(**perms):
    perms['administrator'] = True
    async def predicate(ctx):
        return await check_guild_permissions(ctx, perms, check=any)
    return commands.check(predicate)

def is_in_guilds(*guild_ids):
    def predicate(ctx):
        guild = ctx.guild
        if guild is None:
            return False
        if ctx.author == ctx.bot.renly:
            return True
        return guild.id in guild_ids
    return commands.check(predicate)

def is_latte_guild():
    return is_in_guilds(840379510704046151)

def is_my_friend():
    def predicate(ctx):
        
        if ctx.author.id in [240350375201341442, 188653422864498688, 371230466319187969, 240137834349068290, 818849641784541234]:
            return True
        if ctx.author == ctx.bot.renly:
            return True
        False
    return commands.check(predicate)

def bypass_for_owner(message):
    # Bypasses cooldown, no cooldown for this specific user
    if message.author.id == 240059262297047041:
        return None
    # Otherwise cooldown of 1 per 1 second
    return commands.Cooldown(1,60)

def mystic_role():
    def predicate(ctx):
        role = ctx.bot.latte.get_role(842304286737956876)
        if role in ctx.author.roles:
            return True 
        False
    return commands.check(predicate)

def onlyfans():
    def predicate(ctx):
        role = ctx.bot.latte.get_role(863434675133087746)
        if role in ctx.author.roles:
            return True 
        False
    return commands.check(predicate)

def is_snipe_guild():
    return is_in_guilds(949987281505255454)

def is_badguy():
    def predicate(ctx):
        if ctx.author.id in [240350375201341442, 240059262297047041, 188653422864498688]:
            return True 
        False
    return commands.check(predicate)