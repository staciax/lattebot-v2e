# Standard
import discord
import asyncio
from discord.ext import commands 
from difflib import get_close_matches
from typing import Optional

# Third

# Local
from utils.paginator import SimplePages
from utils.checks import is_latte_guild

class Cancel_button(discord.ui.View):
    def __init__(self, ctx, content=None):
        super().__init__()
        self.value = True
        self.ctx = ctx
        self.content = content
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.user)
        self.clear_items()
        self.fill_items()
    
    def fill_items(self) -> None:
        if self.content is not None:
            self.add_item(self.content_button)
        self.add_item(self.cancel_button_)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This menus cannot be controlled by you, sorry!', ephemeral=True)
        return False

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        embed_error = discord.Embed(color=0xffffff)
        if interaction.response.is_done():
            embed_error.description='An unknown error occurred, sorry'
            await interaction.followup.send(embed=embed_error, ephemeral=True)
        else:
            embed_error.description='An unknown error occurred, sorry'
            await interaction.response.send_message(embed=embed_error, ephemeral=True)

    @discord.ui.button(label="See old content", style=discord.ButtonStyle.green)
    async def content_button(self, button, interaction):
        data = self.content
        if data:
            await interaction.response.send_message(data, ephemeral=True)

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel_button_(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        await self.message.delete()

    async def on_timeout(self):
        self.value = False
        await self.message.edit(view=None)

class Tags(commands.Cog, command_attrs = dict(slash_command=True)):
    """Commands to fetch something by a tag name"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='createthread', id=903346472509141023, animated=False)

    # @commands.group()
    # async def tag(self, ctx):
    #     pass

    @commands.command(help="Tag command")
    @commands.guild_only()
    @is_latte_guild()
    async def tag(self, ctx, tag=commands.Option(description="Input name or id")):
        isInt = True
        try:
            int(tag)
        except ValueError:
            isInt = False

        #check_int_true_or_false
        if isInt:
            check_data = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag_id": int(tag)})
            if bool(check_data) == False:
                check_data = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": str(tag)})
        else:
            check_data = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": str(tag)})
        
        #found_or_not_found
        if check_data is not None:
            message = check_data['content']
            await ctx.send(f"`{check_data['tag']}`\n{message}")
        else:
            not_found = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})
            names = (r['tag'] for r in not_found)
            matches = get_close_matches(tag , names)
            embed_r = discord.Embed(colour=self.bot.white_color)
            if matches:
                matches = "\n".join(matches)
                embed_r.description = f"Tag not found. Did you mean...\n`{matches}`"
            else:
                embed_r.description = f"Tag not found."
            await ctx.send(embed=embed_r , ephemeral=True)

    @commands.command(aliases=['create'], help="Creates a new tag owned by you.")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_create(self, ctx, name:str = commands.Option(description="Input name")):
        #embed
        embed_error = discord.Embed(color=0xFF7878)
        embed = discord.Embed(color=0xfdfd96)

        #find_data
        data_check = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": name})
        if bool(data_check) == True:
            embed_error.description = "This tag already exists. Please use another tag."
            return await ctx.send(embed=embed_error, ephemeral=True)

        #data_count
        data_count = await self.bot.latte_tags.find_many_by_custom({})
        num_list = []
        for x in data_count:     
            num = x['tag_id']
            num_list.append(num)
        next_num = max(num_list)

        #response
        view = Cancel_button(ctx)
        embed.description = "Please enter the content within your tag (within 5 minutes)"
        view.message = await ctx.send(embed=embed, view=view)
        
        try:
            message_response = await self.bot.wait_for('message', timeout=300, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            embed_error.description = 'Create tag was canceled due to timeout.'
            return await view.message.edit(embed=embed_error, view=None)
        
        content = message_response.content
        #when_content_more_2000
        if len(content) > 2000:
            embed_error.description = 'Tag content is a maximum of 2000 characters.'
            return await ctx.send(embed=embed_error, ephemeral=True)
        
        if not view.value:
            return
        elif view.value:

            #create_data
            data = {
                "user_id": ctx.author.id,
                "guild_id": ctx.guild.id,
                "tag": name,
                "content": content,
                "tag_id": next_num + 1
            }

            #update_data
            await self.bot.latte_tags.update_by_custom(
                {"user_id": ctx.author.id, "guild_id": ctx.guild.id, "tag": name}, data
            )

            #reponse
            embed_edit = discord.Embed(description=f"Tag **{name}** successfully created.", timestamp=discord.utils.utcnow(), color=0x77dd77)
            # await message_response.delete()
            await view.message.edit(embed=embed_edit, view=None)

    @commands.command(help="remove your tag")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_remove(self, ctx, name = commands.Option(description="Input your tag name")):
        #embed
        embed_error = discord.Embed(color=0xFF7878)
        
        isInt = True
        try:
            int(name)
        except ValueError:
            isInt = False

        #check_int_true_or_false
        if isInt:
            data_check = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag_id": int(name)})
            if bool(data_check) == False:
                data_check = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": str(name)})
        else:
            data_check = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": str(name)})
        
        #check_data
        if bool(data_check) == False:
            embed_error.description = "tag not found"
            return await ctx.send(embeb=embed_error, ephemeral=True)

        #check_owner_tag
        if data_check["user_id"] != ctx.author.id:
            embed_error.description = "You are not the owner of the tag"
            return await ctx.send(embed=embed_error , ephemeral=True)
        
        #deletd_data
        if isInt:
            data_deleted = await self.bot.latte_tags.delete_by_custom({"guild_id": ctx.guild.id, "tag_id": int(name)})
            if bool(data_deleted) == False:
                data_deleted = await self.bot.latte_tags.delete_by_custom({"guild_id": ctx.guild.id, "tag": str(name)})
        else:
            data_deleted = await self.bot.latte_tags.delete_by_custom({"guild_id": ctx.guild.id, "tag": str(name)})
        
        #check_data_deleted?
        if bool(data_deleted) == False:
            print("data deleted false")
            return

        embed = discord.Embed(color=0xFF7878)
        #delete_is_true_or_false
        if data_deleted and data_deleted.acknowledged:
            embed.description=f"You have successfully deleted **{data_check['tag']}**."
            embed.timestamp = discord.utils.utcnow()
            return await ctx.send(embed=embed)
        else:
            embed.description = "I could not find tag"
            await ctx.send(embed=embed, ephemeral=True)

    @commands.command(help="rename your tag")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_rename(self, ctx, name_old:str= commands.Option(description="tag old name"), name_new:str=commands.Option(description="tag new name")):
        #find_data
        data_check = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": name_old})
        
        embed_error = discord.Embed(color=0xFF7878)

        #check_data
        if bool(data_check) == False:
            embed_error.description = "tag not found"
            return await ctx.send(embed=embed_error, ephemeral=True)

        #check_owner_tag
        if str(data_check["user_id"]) != str(ctx.author.id):
            embed_error.description = "You are not the owner of the tag"
            return await ctx.send(embed=embed_error, ephemeral=True)

        #find_again
        data = await self.bot.latte_tags.find_by_custom({"user_id": ctx.author.id, "guild_id": ctx.guild.id, "tag": name_old})
        
        #update_data
        data["tag"] = name_new                 
        await self.bot.latte_tags.update_by_custom(
            {"user_id": ctx.author.id, "guild_id": ctx.guild.id, "tag": name_old}, data
        )

        #reponse
        embed = discord.Embed(description=f"You have successfully renamed **{name_old}** to **{data['tag']}**", color=0xFCFFA6)
        embed.timestamp = discord.utils.utcnow()
        if ctx.author.avatar is not None:
            embed.set_footer(text=f"Rename by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        else:
            embed.set_footer(text=f"Rename by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(help="edit your tag")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_edit(self, ctx, tag=commands.Option(description="Input your tag name or id")):
        #embed
        embed_error = discord.Embed(color=0xFF7878)
        embed = discord.Embed(color=0xfdfd96)
        
        #check_name_or_id
        isInt = True
        try:
            int(tag)
        except ValueError:
            isInt = False
        
        if isInt:
            data_check = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag_id": int(tag)})
            type_data = 'int'
            if bool(data_check) == False:
                data_check = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": str(tag)})
                type_data = 'int_but_str'
        else:
            data_check = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": str(tag)})
            type_data = 'str'
        
        #check_data
        if bool(data_check) == False:
            embed_error.description = "Tag not found"
            return await ctx.send(embed=embed_error, ephemeral=True)

        #check_owner_tag
        if data_check["user_id"] != ctx.author.id:
            embed_error.description = "You are not the owner of this tag."
            return await ctx.send(embed=embed_error, ephemeral=True)

        old_content = data_check['content'] or None

        #response
        view = Cancel_button(ctx, content=old_content)
        embed.description = "Please enter the new content (within 5 minutes)"
        view.message = await ctx.send(embed=embed, view=view)

        #waiting_message
        try:
            message_response = await self.bot.wait_for('message', timeout=300, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            embed_error.description = 'Edit tag was canceled due to timeout.'
            return await view.message.edit(embed=embed_error, view=None)

        content = message_response.content
        #when_content_more_2000
        if len(content) > 2000:
            embed_error.description = 'Tag content is a maximum of 2000 characters.'
            return await ctx.send(embed=embed_error, ephemeral=True)

        if not view.value:
            return
        elif view.value:
            
            data_check["content"] = content

            if type_data == 'int':
                await self.bot.latte_tags.update_by_custom(
                    {"guild_id": ctx.guild.id, "tag_id": int(tag)}, data_check
                )
            elif type_data in ['str','int_but_str']:
                await self.bot.latte_tags.update_by_custom(
                    {"guild_id": ctx.guild.id, "tag": str(tag)}, data_check
                )
        
            embed_edit = discord.Embed(description=f"You have successfully edited **{data_check['tag']}**", timestamp=discord.utils.utcnow())
            embed_edit.color = 0x77dd77
            if ctx.author.avatar is not None:
                embed_edit.set_footer(text=f"Edited by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            else:
                embed_edit.set_footer(text=f"Edited by {ctx.author.display_name}")
            # await message_response.delete()
            await view.message.edit(embed=embed_edit)

    @commands.command(help="Show all tag in your server")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_list(self, ctx):

        #sort_tag
        data = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})
        
        #count_tag
        all_tag = []
        for x in data:
            tags = f'{x["tag"]} (ID : {x["tag_id"]})'
            all_tag.append(tags)
        
        #view_button
        if all_tag:
            p = SimplePages(entries=all_tag, per_page=10, ctx=ctx)
            p.embed.color = 0xBFA2DB
            await p.start()
        else:
            #reponse
            embed = discord.Embed(description=f"This server doesn't have any tags.", color=0xFF7878)
            await ctx.send(embed=embed, ephemeral=True)

    @commands.command(help="search tag")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_search(self, ctx, name:str = commands.Option(description="Input tag name")):

        #find_name_tag
        not_found = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})
        
        total:int = len(not_found)
        names = (r['tag'] for r in not_found)
        matches = get_close_matches(name , names , n=total)

        #coverter_to_string
        tag_found = []
        for x in matches:
            data = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id, "tag": x})
            find_id = '\n'.join(f'{i["tag_id"]}' for i in data)
            tag_name_id = f'{x} (ID : {find_id})'
            tag_found.append(tag_name_id)

        if tag_found:
            #view_button
            p = SimplePages(entries=tag_found, per_page=10, ctx=ctx)
#            p.embed.title = "Tags search"
            p.embed.color = 0xBFA2DB
            await p.start()
        else:
            #reponse
            embed = discord.Embed(description=f"**{name}** This tag not found", color=0x77dd77)
            await ctx.send(embed=embed, ephemeral=True)

    @commands.command(help="Total tag in your server")
    @commands.guild_only()
    @is_latte_guild()
    async def tagcount(self, ctx):
        data = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})
        embed_error = discord.Embed(color=0xFF7878)
        if bool(data) == False:
            embed_error.description = "This server doesn't have any tags."
            return await ctx.send(embed=embed_error, ephemeral=True)
        
        embed = discord.Embed(description=f"Total tags : `{len(data)}`",color=0x77dd77)
        await ctx.send(embed=embed)
  
def setup(bot):
    bot.add_cog(Tags(bot))