# Standard
import discord
from discord.ext import commands

# Third
from utils.checks import is_latte_guild
from utils.formats import format_dt
from utils.buttons import Confirm
from utils.buttons import TodoPageSource, BaseNewButton
from utils.custom_button import Button_URL

# Local

class TodoListView(BaseNewButton):

    def __init__(self, entries, *, ctx: commands.Context, per_page: int = 12):
        super().__init__(TodoPageSource(entries, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(colour=0xffffff)

class Todo(commands.Cog):
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
        cog = self.bot.get_cog("Todo")
                
        entries = cog.get_commands()
        command_signatures = [ctx.bot.help_command.get_minimal_command_signature_custom(c, ctx) for c in entries]
        commands_list = []
        for command in command_signatures:
            if not command == f"{ctx.clean_prefix}todo ":
                commands_list.append(command)
                
        await ctx.bot.help_command.send_group_help_user(signatures=commands_list, ctx=ctx, command_name=ctx.command, description="Todo commands")

    # @todo.command(help="Adds the specified task to your todo list.")
    @commands.command(aliases=['tda','todoa','todoadd'], help="Adds the specified task to your todo list.")
    @is_latte_guild()
    async def todo_add(self, ctx, *, content=commands.Option(description="Input content")):     
        
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
        embed = discord.Embed(title="Added to your todo list:", description=content)
        await ctx.send(embed=embed)

    # @todo.command(name="list", help="Sends a list of your tasks.")
    @commands.command(aliases=['tdl','todol','todolist'], help="Sends a list of your tasks.")
    @is_latte_guild()
    async def todo_list(self, ctx):
        #embed
        embed_error = discord.Embed(color=0xFF7878)

        data = await self.bot.latte_todo.find_many_by_custom({"user_id": ctx.author.id})

        #check_data
        if bool(data) == False:
            embed_error.description = f"Your todo list is empty" #check_data
            return await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)
        
        #count_tag
        all_todo = []
        number = 0
        for x in data:
            number = number + 1
            todo_entries = f"**[{number}]({x['jump_url']})**. {x['content']} ({format_dt(x['creation_date'], style='R')})"
            all_todo.append(todo_entries)
        
        p = TodoListView(entries=all_todo, ctx=ctx)
        p.embed.title = f"{ctx.author.name}'s todo list"
        await p.start()

    # @todo.command(help="Removes the specified task from your todo list")
    @commands.command(aliases=['tdr','todor','todoremove'], help="Removes the specified task from your todo list")
    @is_latte_guild()
    async def todo_remove(self, ctx, number: int = commands.Option(description="Todo number")):
        embed_error = discord.Embed(color=self.bot.error_color)
        data = await self.bot.latte_todo.find_many_by_custom({"user_id": ctx.author.id})
        
        #check_data
        if bool(data) == False:
            embed_error.description = f"Your todo list is empty"
            return await ctx.send(embeb=embed_error, ephemeral=True, delete_after=15)

        i = 0
        for x in data:
            i += 1
            if i == number:
                delete_id = x["todo_id"]
                break
        if delete_id:
            bofore_delete = await self.bot.latte_todo.find_by_custom({"user_id": ctx.author.id, "todo_id": int(delete_id)})
            data_deleting = await self.bot.latte_todo.delete_by_custom({"user_id": ctx.author.id, "todo_id": int(delete_id)})

            embed = discord.Embed(color=self.bot.white_color)
            if data_deleting and data_deleting.acknowledged:
                embed.title=f"Successfully removed task number **{number}**:"
                embed.description =f"{bofore_delete['content']} ({format_dt(bofore_delete['creation_date'], style='R')})"
                return await ctx.send(embed=embed)
            else:
                embed_error.description = "I could not find this todo"
                await ctx.send(embed=embed_error, ephemeral=True, delete_after=15)
        
    # @todo.command(help="Deletes all tasks from your todo list.")
    @commands.command(aliases=['tdc','todoc','todoclear','tdclear'], help="Deletes all tasks from your todo list.")
    @is_latte_guild()
    async def todo_clear(self, ctx):
        embed_error = discord.Embed(color=self.bot.error_color)
        check = await self.bot.latte_todo.find_many_by_custom({"user_id": ctx.author.id})

        if bool(check) == False:
            embed_error.description = f"Your todo list is empty"
            return await ctx.send(embeb=embed_error, ephemeral=True, delete_after=15)

        embed = discord.Embed(color=self.bot.white_color)
        embed.description = "Are you sure you want to clear your todo list?"

        view = Confirm(ctx=ctx)
        msg = await ctx.send(embed=embed, view=view)
        await view.wait()

        if view.value is None:
            return
        elif view.value:
            embed_suc = discord.Embed(color=self.bot.white_color)
            len_data = len(await self.bot.latte_todo.find_many_by_custom({"user_id": ctx.author.id}))
            data_deleted = await self.bot.latte_todo.delete_by_custom({"user_id": ctx.author.id})
            if data_deleted and data_deleted.acknowledged:
                embed_suc.description = f"Successfully removed {len_data} tasks."
                embed_suc.timestamp = discord.utils.utcnow()
                return await msg.edit(embed=embed_suc, view=None) 
            else:
                embed.description = "I could not remove todo"
                await msg.edit(embed=embed, view=None, ephemeral=True, delete_after=15)

        else:
            embed.description = f"Cancelled..."
            await msg.edit(embed=embed, view=None, ephemeral=True, delete_after=15)

    @commands.command(aliases=['tde','todoe','todoedit'], help="Edits the specified task")
    @is_latte_guild()
    async def todo_edit(
            self,
            ctx,
            number: int,
            *,
            content
        ):
        embed = discord.Embed()


        data = await self.bot.latte_todo.find_many_by_custom({"user_id": ctx.author.id})

        if bool(data) == False:
            embed.color = self.bot.error_color
            embed.description = f"Your todo list is empty"
            return await ctx.send(embed=embed, ephemeral=True, delete_after=15)

        i = 0
        for x in data:
            i += 1
            if i == number:
                edit_id = x["todo_id"]
                break

        if edit_id:
            old = await self.bot.latte_todo.find_by_custom({"user_id": ctx.author.id, "todo_id": int(edit_id)})

            if bool(old) == False:
                embed.color = self.bot.error_color
                embed.description = f"I couldn't find a task with index {number}"
                return await ctx.send(embed=embed, ephemeral=True, delete_after=15)
            
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