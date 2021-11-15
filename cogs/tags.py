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
from utils.custom_button import content_button
from utils.converter import is_url_image

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

    @discord.ui.button(label="Content before edit", style=discord.ButtonStyle.green)
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

    async def delete_message(self):  
        self.value = False
        try:
            await self.message.delete()
        except:
            return

class TagName(commands.clean_content):
    def __init__(self, *, lower=False):
        self.lower = lower
        super().__init__()

    async def convert(self, ctx, argument):
        converted = await super().convert(ctx, argument)
        lower = converted.lower().strip()

        if not lower:
            raise commands.BadArgument('Missing tag name.')

        if len(lower) > 100:
            raise commands.BadArgument('Tag name is a maximum of 100 characters.')

        first_word, _, _ = lower.partition(' ')

        # # get tag command.
        # root = ctx.bot.get_command('tag')
        # if first_word in root.all_commands:
        #     raise commands.BadArgument('This tag name starts with a reserved word.')

        return converted if not self.lower else lower

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
    async def tag(self, ctx, *, tag:TagName =commands.Option(description="Input name or id")):
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
            # try:
            #     check_img = is_url_image(image_url=message)
            # except Exception:
            #     check_img = False
            # if ctx.clean_prefix != "/" or check_img is True:
            #     return await ctx.send(message)
            if ctx.clean_prefix != "/" or message.lower().endswith(('png','jpeg','jpg','gif','webp','mp4')):
                return await ctx.send(message)
            await ctx.send(f"**`{check_data['tag']}`**\n{message}")
        else:
            not_found = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})
            names = (r['tag'] for r in not_found)
            matches = get_close_matches(tag , names)
            embed_r = discord.Embed(colour=self.bot.white_color)
            if matches:
                matches = "\n".join(matches)
                embed_r.description = f"Tag not found. Did you mean...\n`{matches}`"
                cooldown = 30
            else:
                embed_r.description = f"Tag not found."
                cooldown = 15
            await ctx.send(embed=embed_r , ephemeral=True, delete_after=cooldown)

    @commands.command(aliases=['tagcreate','tagc'], help="Creates a new tag owned by you.")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_create(self, ctx, *, name: TagName(lower=True) = commands.Option(description="Input name")):
        #embed
        embed_error = discord.Embed(color=0xFF7878)
        embed = discord.Embed(color=0xfdfd96)

        #find_data
        data_check = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": name})
        if bool(data_check) == True:
            embed_error.description = "This tag already exists, please use another tag."
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)

        #data_count
        data_tags = await self.bot.latte_tags.find_many_by_custom({})
        data_count = reversed(data_tags)
        
        #create_id
        try:
            some_id = []
            i = 0
            for x in data_count:
                i += 1 
                next_id = x['tag_id']
                some_id.append(next_id)
                if i == 10:
                    break
            next_num = max(some_id) + 1
        except:
            next_num = 1

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
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)
        
        if not view.value:
            return
        elif view.value:

            tag_filter = {"user_id": ctx.author.id, "guild_id": ctx.guild.id, "tag_id": next_num}
            tag_data = {"tag": name, "content": content}

            #upsert_data
            await self.bot.latte_tags.upsert_custom(tag_filter, tag_data)

            #reponse
            embed_edit = discord.Embed(description=f"Tag **{name}** successfully created.", timestamp=discord.utils.utcnow(), color=0x77dd77)
            # await message_response.delete()
            # await view.message.edit(embed=embed_edit, view=None)
            await view.delete_message()
            await ctx.channel.send(embed=embed_edit)

    @commands.command(aliases=['tagremove','tagr','tagdelete'], help="remove your tag")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_remove(self, ctx, *, name: TagName = commands.Option(description="Input your tag name")):
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
            embed_error.description = "Tag not found"
            return await ctx.send(embeb=embed_error, ephemeral=True, delete_after=15)

        #check_owner_tag
        if data_check["user_id"] != ctx.author.id:
            embed_error.description = "You are not the owner of the tag"
            return await ctx.send(embed=embed_error , ephemeral=True, delete_after=15)
        
        #deletd_data
        if isInt:
            data_deleted = await self.bot.latte_tags.delete_by_custom({"guild_id": ctx.guild.id, "tag_id": int(name)})
            if bool(data_deleted) == False:
                data_deleted = await self.bot.latte_tags.delete_by_custom({"guild_id": ctx.guild.id, "tag": str(name)})
        else:
            data_deleted = await self.bot.latte_tags.delete_by_custom({"guild_id": ctx.guild.id, "tag": str(name)})
        
        # #check_data_deleted?
        # if bool(data_deleted) == False:
        #     print("data deleted false")
        #     return

        embed = discord.Embed(color=0xFF7878)
        #delete_is_true_or_false
        if data_deleted and data_deleted.acknowledged:
            embed.description=f"You have successfully deleted **{data_check['tag']}**."
            embed.timestamp = discord.utils.utcnow()
            return await ctx.send(embed=embed)
        else:
            embed.description = "I could not find tag"
            await ctx.send(embed=embed, ephemeral=True, delete_after=15)

    @commands.command(aliases=['tagrename','tagre'], help="rename your tag")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_rename(self, ctx, name_old:TagName = commands.Option(description="tag old name"), *, name_new:TagName=commands.Option(description="tag new name")):
        #find_data
        data_check = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": name_old})
        
        embed_error = discord.Embed(color=0xFF7878)

        #check_data
        if bool(data_check) == False:
            embed_error.description = "tag not found"
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)

        #check_owner_tag
        if str(data_check["user_id"]) != str(ctx.author.id):
            embed_error.description = "You are not the owner of the tag"
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)

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

    @commands.command(aliases=['tagedit','tage'], help="edit your tag")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_edit(self, ctx, *, tag:TagName =commands.Option(description="Input your tag name or id")):
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
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)

        #check_owner_tag
        if data_check["user_id"] != ctx.author.id:
            embed_error.description = "You are not the owner of this tag."
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)

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
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)

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
            # await view.message.edit(embed=embed_edit, view=None)
            await view.delete_message()
            await ctx.channel.send(embed=embed_edit)

    @commands.command(aliases=['taglist','tagl'], help="Lists all the tags that belong to you or someone else.")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_list(self, ctx, member: discord.Member = commands.Option(default=None, description="Spectify member")):
        #embed
        embed_error = discord.Embed(color=0xFF7878)

        if member is None:
            member = ctx.author

        data = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id, "user_id": member.id})

        #check_data
        if bool(data) == False:
            embed_error.description = f"{member.display_name} doesn't have any tags."#
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)
        data = sorted(data, key=lambda x: x["tag"])
        
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
            embed = discord.Embed(description=f"{member.display_name} doesn't have any tags.", color=0xFF7878)
            await ctx.send(embed=embed, ephemeral=True, delete_after=15)
    
    @commands.command(aliases=['tagall'], help="Lists all server-specific tags for this server.")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_all(self, ctx):
        #embed
        embed_error = discord.Embed(color=0xFF7878)

        data = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})

        #check_data
        if bool(data) == False:
            embed_error.description = "Not found tag from this server." #check_data
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)
        data = sorted(data, key=lambda x: x["tag"])
        
        #count_tag
        all_tag = []
        for x in data:
            tags = f'{x["tag"]} (ID : {x["tag_id"]})'
            all_tag.append(tags)
        
        #view_button
        if all_tag:
            p = SimplePages(entries=all_tag, ctx=ctx)
            p.embed.color = 0xBFA2DB
            await p.start()
        else:
            #reponse
            embed = discord.Embed(description=f"This server doesn't have any tags.", color=0xFF7878)
            await ctx.send(embed=embed, ephemeral=True, delete_after=15)

    @commands.command(aliases=['tagsearch','tags'], help="Searches for a tag.")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_search(self, ctx, *, name:TagName(lower=True) = commands.Option(description="Input tag name")):

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
            await ctx.send(embed=embed, ephemeral=True, delete_after=15)

    @commands.command(aliases=['taginfo','tagi'], help="Shows information about the specified tag.")
    @commands.guild_only()
    @is_latte_guild()
    async def tag_info(self, ctx, *, tag:TagName =commands.Option(description="Input your tag name or id")):
        isInt = True
        try:
            int(tag)
        except ValueError:
            isInt = False

        #check_int_true_or_false
        if isInt:
            data = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag_id": int(tag)})
            if bool(data) == False:
                data = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": str(tag)})
        else:
            data = await self.bot.latte_tags.find_by_custom({"guild_id": ctx.guild.id, "tag": str(tag)})
        
        #found_or_not_found
        if data is not None:
            view = content_button(ctx=ctx , content=data['content'])
            owner_tag = ctx.guild.get_member(int(data['user_id']))

            embed = discord.Embed(color=self.bot.white_color)
            embed.title = f"Tag Info"
            embed.description = f"**Tag name:** {data['tag']}\n"
            embed.description += f"**Author:** {owner_tag.mention}\n"
            embed.set_footer(text=f"ID : {data['tag_id']}")

            await ctx.send(embed=embed, view=view)

        else:
            not_found = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})
            names = (r['tag'] for r in not_found)
            matches = get_close_matches(tag , names)
            embed_r = discord.Embed(colour=self.bot.white_color)
            if matches:
                matches = "\n".join(matches)
                embed_r.description = f"Tag not found. Did you mean...\n`{matches}`"
                cooldown = 30
            else:
                embed_r.description = f"Tag not found."
                cooldown = 15
            await ctx.send(embed=embed_r , ephemeral=True, delete_after=cooldown)

    @commands.command(aliases=['tag_count'], help="Total tag in your server")
    @commands.guild_only()
    @is_latte_guild()
    async def tagcount(self, ctx):
        data = await self.bot.latte_tags.find_many_by_custom({"guild_id": ctx.guild.id})
        embed_error = discord.Embed(color=0xFF7878)
        if bool(data) == False:
            embed_error.description = "This server doesn't have any tags."
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)
        
        embed = discord.Embed(description=f"Total tags : `{len(data)}`",color=0x77dd77)
        await ctx.send(embed=embed)
  
def setup(bot):
    bot.add_cog(Tags(bot))