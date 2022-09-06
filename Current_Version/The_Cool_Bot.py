# The Cool Bot
# Created by Parzivel_1#4463 (ID = 643853842441830400)
# Version 10.0
# py-cord



# ===== IMPORTS =====



import discord , json , os
from discord.ext import commands as cmds
__location__ = os.path.realpath(os.path.join(os.getcwd() , os.path.dirname(__file__)))


# ===== BOT CREATION =====



def get_prefix(bot , msg) :
    if isinstance(msg.guild , discord.Guild) :
        guild_id = str(msg.guild.id)
        prefix = bot.data[guild_id]["Data"]["Prefix"]
    else :
        prefix = "p!"
    return cmds.when_mentioned_or(prefix)(bot , msg)



class MyBot(cmds.Bot) :
    def __init__(self , *args , **kwargs) :
        with open(os.path.join(__location__ , "data.json")) as f :
            self.data = json.load(f)
        super().__init__(*args , **kwargs)


    def open_data(self , ctx) :
        guild_id = str(ctx.guild.id)
        return self.data[guild_id]


    def save_data(self , ctx , guild_data) :
        guild_id = str(ctx.guild.id)
        bot.data[guild_id] = guild_data
        with open(os.path.join(__location__ , "data.json") , "w") as f :
            json.dump(self.data , f , indent = 4)


    async def send(self , ctx , text , color) :
        msg = discord.Embed(description = f"**{text}**" , color = color)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        if type(ctx) in (cmds.Context , discord.Message) :
            return await ctx.reply(embed = msg)
        elif type(ctx) == discord.ApplicationContext :
            return await ctx.respond(embed = msg)
        else :
            await ctx.send(embed = msg)


    async def check_owner(self , ctx) :
        if ctx.guild.owner == ctx.author :
            return True
        else :
            await self.bot.send(ctx , "This command can only be used by the owner!" , 0xff7f00)
            return False


    async def check_staff(self , ctx) :
        if ctx.author.guild_permissions.administrator :
            return True
        else :
            data = self.open_data(ctx)
            staff_roles = data["Data"]["Staff Roles"] if "Staff Roles" in data["Data"] else ()
            if not staff_roles :
                await self.send(ctx , "This command can only be used by the staff members!" , 0xff7f00)
                return False
            else :
                for role in ctx.author.roles :
                    if role.id in staff_roles :
                        return True
                await self.send(ctx , "This command can only be used by the staff members!" , 0xff7f00)
                return False


    async def check_vc(self , ctx) :
        if ctx.command.name == "help" :
            return True
        data = self.open_data(ctx)
        author_id = str(ctx.author.id)
        if author_id in data and "VC" in data[author_id] :
            return True
        else :
            await self.send(ctx , "You have to be in your voice channel to use this command!" , 0xff7f00)
            return False



bot = MyBot(command_prefix = get_prefix , help_command = None , intents = discord.Intents.all() , owner_ids = [643853842441830400 , 292770890792566784])



# ===== EVENTS =====



@bot.event # Member leaves a server
async def on_member_leave(member) :
    member_id = str(member.id)
    data = bot.open_data(member)
    if member_id in data :
        data.pop(member_id)
        bot.save_data(member , data)


@bot.event # Command got error
async def on_command_error(ctx , error) :
    print("===== Command got error =====")
    print(f"Type Error >>> {type(error)}")
    print(f"Error >>> {error}")
    print(f"Guild >>> {ctx.guild}  /  {ctx.guild.id}" if ctx.channel.guild else "Guild >>> Not in a guild")
    print(f"Channel >>> {ctx.channel.name}  /  {ctx.channel.id}")
    print(f"Message Link >>> {ctx.message.jump_url}")
    print("=============================")
    data = bot.open_data(ctx)
    if not ctx.channel.guild or type(error) in (cmds.CommandOnCooldown , cmds.CommandNotFound , cmds.NotOwner) :
        return
    elif isinstance(ctx.channel , discord.DMChannel) :
        await bot.send(ctx , "This command can only be used in a server!" , 0xff7f00)
    elif type(error) in (cmds.MemberNotFound , cmds.UserNotFound , cmds.RoleNotFound , cmds.ChannelNotFound) :
        options = {cmds.MemberNotFound : "member" , cmds.UserNotFound : "user" , cmds.RoleNotFound : "role" , cmds.ChannelNotFound : "voice channel"}
        option = options[type(error)]
        await bot.send(ctx , f"You didn't provide a {option}!" , 0xff7f00)
    elif isinstance(error , cmds.MissingPermissions) :
        perms = ", ".join(error.missing_perms).replace("_" , " ")
        await bot.send(ctx , f"You don't have the `{perms}` permission to use this command!" , 0xff7f00)
    elif isinstance(error , cmds.BotMissingPermissions) :
        if not ("send_messages" in error.missing_perms or "embed_links" in error.missing_perms) :
            perms = ", ".join(error.missing_perms).replace("_" , " ")
            await bot.send(error , f"I don't have the `{perms}` permission to use this command!" , 0xff7f00)
    elif type(error) != cmds.CheckFailure :
        print("\nRaised Error:\n")
        raise error


@bot.event # Slash command got error
async def on_application_command_error(ctx , error) :
    print("===== Slash Command got error =====")
    print(f"Type Error >>> {type(error)}")
    print(f"Error >>> {error}")
    print(f"Guild >>> {ctx.guild}  /  {ctx.guild.id}" if ctx.channel.guild else "Guild >>> Not in a guild")
    print(f"Channel >>> {ctx.channel.name}  /  {ctx.channel.id}")
    data = bot.open_data(ctx)
    if not ctx.channel.guild or type(error) in (cmds.CommandOnCooldown , cmds.CommandNotFound , cmds.NotOwner) :
        return
    elif isinstance(ctx.channel , discord.DMChannel) :
        msg = await bot.send(ctx , "This command can only be used in a server!" , 0xff7f00)
    elif type(error) in (cmds.MemberNotFound , cmds.UserNotFound , cmds.RoleNotFound , cmds.ChannelNotFound) :
        options = {cmds.MemberNotFound : "member" , cmds.UserNotFound : "user" , cmds.RoleNotFound : "role" , cmds.ChannelNotFound : "voice channel"}
        option = options[type(error)]
        msg = await bot.send(ctx , f"You didn't provide a {option}!" , 0xff7f00)
    elif isinstance(error , cmds.MissingPermissions) :
        perms = ", ".join(error.missing_perms).replace("_" , " ")
        msg = await bot.send(ctx , f"You don't have the `{perms}` permission to use this command!" , 0xff7f00)
    elif isinstance(error , cmds.BotMissingPermissions) :
        if not ("send_messages" in error.missing_perms or "embed_links" in error.missing_perms) :
            perms = ", ".join(error.missing_perms).replace("_" , " ")
            msg = await bot.send(error , f"I don't have the `{perms}` permission to use this command!" , 0xff7f00)
    if ctx.message :
        print(f"Message Link >>> {ctx.message.jump_url}\n")
    else :
        print(f"Message Link >>> welp\n")
    if type(error) != cmds.CheckFailure :
        print("\nRaised Error:\n")
        raise error
    print("=============================")


@bot.event # Every message
async def on_message(msg) :
    if msg.author.bot :
        return
    if msg.guild and msg.content in (msg.guild.me.mention , bot.user.mention) :
        await bot.send(msg , f"My prefix here is `{bot.command_prefix(bot , msg)[2]}` !" , 0x00ff00)
    else :
        await bot.process_commands(msg)


@bot.event # Bot starts
async def on_ready() :
    print("I'm Ready!")



# ===== BOT START =====



bot.load_extension("Cogs.Owner_Commands")
bot.load_extension("Cogs.Staff_Commands")
bot.load_extension("Cogs.Fun_Commands")
bot.load_extension("Cogs.Private_VC_Commands")
bot.load_extension("Cogs.Other_Commands")

# Two more cogs for some personal commands and tasks:

# bot.load_extension("Cogs.Ignore_Commands")
# bot.load_extension("Cogs.Loops")


# Add your own bot token if you want to run this:

bot.run("Bot Token Here :)")