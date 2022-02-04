# Standard
import discord
from discord.ext import commands

# Third
from utils.checks import is_latte_guild
from utils.formats import format_dt
from utils.buttons import Confirm
from utils.buttons import TodoPageSource, BaseNewButton
from utils.custom_button import Button_URL
from utils.useful import RenlyEmbed
from utils.errors import UserInputErrors

# Local

class TodoListView(BaseNewButton):

    def __init__(self, entries, *, ctx: commands.Context, per_page: int = 12):
        super().__init__(TodoPageSource(entries, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(colour=0xffffff)

class todolist_button(discord.ui.View):
    def __init__(self, ctx, entries=None):
        super().__init__()
        self.ctx = ctx
        self.entries = entries
        self.is_command = ctx.command is not None
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.user)
        self.clear_items()
        self.fill_items()
        
    def fill_items(self) -> None:
        if self.entries is not None:
            self.add_item(self.todolist_button)
    
    async def interaction_check(self, item, interaction: discord.Interaction) -> bool:
        """Only allowing the context author to interact with the view"""
        ctx = self.ctx
        author = ctx.author
        mystic_role = discord.utils.get(interaction.user.roles, id=842304286737956876)
        if interaction.user == ctx.bot.renly:
            return True
        if bool(mystic_role) == True:
            return True
        if interaction.user != ctx.author:
            if self.is_command:
                command = ctx.bot.get_command_signature(ctx, ctx.command)
                content = f"Only `{author}` can use this menu. If you want to use it, use `{command}`"
            else:
                content = f"Only `{author}` can use this."
            embed = RenlyEmbed.to_error(description=content)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    async def on_error(self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction) -> None:
        embed_error = discord.Embed(color=0xffffff)
        if interaction.response.is_done():
            embed_error.description='An unknown error occurred, sorry'
            await interaction.followup.send(embed=embed_error, ephemeral=True)
        else:
            embed_error.description='An unknown error occurred, sorry'
            await interaction.response.send_message(embed=embed_error, ephemeral=True)
        
    @discord.ui.button(label="Current todo list", style=discord.ButtonStyle.primary)
    async def todolist_button(self, button, interaction):
        ctx = self.ctx
        data = self.entries
        all_todo = []
        number = 0
        for x in data:
            number = number + 1
            todo_entries = f"**[{number}]({x['jump_url']})**. {x['content']} ({format_dt(x['creation_date'], style='R')})"
            all_todo.append(todo_entries)
        
        p = TodoListView(entries=all_todo, ctx=ctx)
        p.embed.title = f"{ctx.author.name}'s todo list"
        await p.start()

class UserInputErrors(commands.UserInputError):
    pass

class Todo(commands.Cog, command_attrs = dict(slash_command=True, slash_command_guilds=[840379510704046151,887274968012955679])):
    """Todo commands"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='love_note', id='909498501799505930', animated=False)
    
    @commands.command(help="Todo commands")
    @is_latte_guild()
    async def todo(self, ctx):                
        await ctx.bot.help_command.send_group_help_user("Todo", ctx)

    # @todo.command(help="Adds the specified task to your todo list.")
    @commands.command(aliases=['tda','todoa','todoadd'], help="Adds the specified task to your todo list.")
    @is_latte_guild()
    async def todo_add(self, ctx, *, content=commands.Option(description="Input content")):             
        
        if len(content) > 100:
            raise UserInputErrors('todo content is a maximum of 100 characters.')

        #data_user_count
        user_count = await self.bot.latte_todo.find_many_by_custom({"user_id": ctx.author.id})
        if len(user_count) >= 50 and ctx.author != self.bot.renly:
            raise UserInputErrors("You can't have more than 50 todo at the moment.")

        #data_count
        data_count = await self.bot.latte_todo.find_many_by_custom({})
        
        #create_id
        try:
            num_list = []
            for x in data_count:
                num = x['todo_id']
                num_list.append(num)
            next_num = max(num_list) + 1
        except:
            next_num = 1
        
        todo_filter = {"user_id": ctx.author.id, "todo_id": next_num}
        todo_data = {"content": content, "jump_url": ctx.message.jump_url, "creation_date": ctx.message.created_at}

        #upsert_data
        await self.bot.latte_todo.upsert_custom(todo_filter, todo_data)
        embed = discord.Embed(title="Added to your todo list:", description=content , color=self.bot.white_color)
        await ctx.send(embed=embed)

    # @todo.command(name="list", help="Sends a list of your tasks.")
    @commands.command(aliases=['tdl','todol','todolist'], help="Sends a list of your tasks.")
    @is_latte_guild()
    async def todo_list(self, ctx):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()

        data = await self.bot.latte_todo.find_many_by_custom({"user_id": ctx.author.id})

        #check_data
        if bool(data) == False:
            raise UserInputErrors(f"Your todo list is empty")
        
        #count_tag
        all_todo = []
        number = 0
        for x in data:
            number = number + 1
            todo_entries = f"**[{number}]({x['jump_url']})**. {x['content']} ({format_dt(x['creation_date'], style='R')})"
            all_todo.append(todo_entries)
        
        p = TodoListView(entries=all_todo, ctx=ctx)
        if ctx.author.avatar is not None:
            p.embed.set_author(name=f"{ctx.author.display_name}'s todo list", icon_url=ctx.author.avatar.url)
        else:
            p.embed.set_author(name=f"{ctx.author.display_name}'s todo list")
        await p.start()

    # @todo.command(help="Removes the specified task from your todo list")
    @commands.command(aliases=['tdr','todor','todoremove'], help="Removes the specified task from your todo list")
    @is_latte_guild()
    async def todo_remove(self, ctx, *, number = commands.Option(description="Todo number")):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()
        
        data = await self.bot.latte_todo.find_many_by_custom({"user_id": ctx.author.id})
        
        #check_data
        if bool(data) == False:
            raise UserInputErrors(f"Your todo list is empty")
        
        data_deleting = None
        description = ""
        number_split = number.split(" ")
        i = 0
        try:
            for x in data:
                i += 1
                if str(i) in number_split:
                    delete_id = x["todo_id"]
                    bofore_delete = await self.bot.latte_todo.find_by_custom({"user_id": ctx.author.id, "todo_id": int(delete_id)})
                    description +=f"\n**[{i}]({bofore_delete['jump_url']})**. {bofore_delete['content']} ({format_dt(bofore_delete['creation_date'], style='R')})"
                    data_deleting = await self.bot.latte_todo.delete_by_custom({"user_id": ctx.author.id, "todo_id": int(delete_id)})
        except KeyError:
            raise UserInputErrors
        
        sord_num = sorted(number_split)
        sord_num = ', '.join(sord_num) 
        embed = discord.Embed(color=self.bot.white_color)
        if data_deleting and data_deleting.acknowledged:
            embed.title=f"Successfully removed task number **{sord_num}**:"
            embed.description = description
            await ctx.send(embed=embed)
        else:
            raise UserInputErrors("I could not find your todo")
        
    # @todo.command(help="Deletes all tasks from your todo list.")
    @commands.command(aliases=['tdc','todoc','todoclear','tdclear'], help="Deletes all tasks from your todo list.")
    @is_latte_guild()
    async def todo_clear(self, ctx):
        check = await self.bot.latte_todo.find_many_by_custom({"user_id": ctx.author.id})

        if bool(check) == False:
            raise UserInputErrors("Your todo list is empty")

        embed = discord.Embed(color=self.bot.white_color)
        embed.description = "Are you sure you want to clear your todo list?"

        view = Confirm(ctx=ctx)
        msg = await ctx.send(embed=embed, view=view)
        await view.wait()

        if view.value is None:
            return
        elif view.value:
            if ctx.interaction is not None:
                await ctx.interaction.response.defer()
            embed_suc = discord.Embed(color=self.bot.white_color)
            len_data = len(await self.bot.latte_todo.find_many_by_custom({"user_id": ctx.author.id}))
            data_deleted = await self.bot.latte_todo.delete_by_custom({"user_id": ctx.author.id})
            if data_deleted and data_deleted.acknowledged:
                embed_suc.description = f"Successfully removed {len_data} tasks."
                embed_suc.timestamp = discord.utils.utcnow()
                return await msg.edit(embed=embed_suc, view=None) 
            else:
                raise UserInputErrors("I could not remove todo")
                
        else:
            raise UserInputErrors('Cancelled...')

    @commands.command(aliases=['tde','todoe','todoedit'], help="Edits the specified task")
    @is_latte_guild()
    async def todo_edit(
            self,
            ctx,
            number: int,
            *,
            content
        ):
        if ctx.interaction is not None:
            await ctx.interaction.response.defer()
        
        embed = discord.Embed()
        data = await self.bot.latte_todo.find_many_by_custom({"user_id": ctx.author.id})

        if bool(data) == False:
            raise UserInputErrors("Your todo list is empty")

        i = 0
        for x in data:
            i += 1
            if i == number:
                edit_id = x["todo_id"]
                break

        if edit_id:
            old = await self.bot.latte_todo.find_by_custom({"user_id": ctx.author.id, "todo_id": int(edit_id)})

            if bool(old) == False:
                raise UserInputErrors(f"I couldn't find a task with index {number}")
            
            new_data = {"content": content, "jump_url": ctx.message.jump_url, "creation_date": ctx.message.created_at}
            await self.bot.latte_todo.update_by_custom({"user_id": ctx.author.id, "todo_id": number}, new_data)
            new = await self.bot.latte_todo.find_by_custom({"user_id": ctx.author.id, "todo_id": number})
            
            embed.color=self.bot.white_color
            embed.title = f"Successfully edited task number **{number}**:"
            embed.add_field(name="Old",value=f"Text: {old['content']}\nCreation date: {format_dt(old['creation_date'], style='R')}",inline=False)
            embed.add_field(name="New",value=f"Text: {new['content']}\nCreation date: {format_dt(new['creation_date'], style='R')}",inline=False)
            view_url = {
                "Old Source":f"{old['jump_url']}",
                "New Source":f"{new['jump_url']}"
            }
            view = Button_URL(label=view_url.keys(), url=view_url.values())
            await ctx.send(embed=embed, view=view)
        
def setup(bot):
    bot.add_cog(Todo(bot))