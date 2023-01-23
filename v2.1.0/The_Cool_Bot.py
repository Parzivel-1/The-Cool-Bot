# The Cool Bot
# Created by Parzivel_1#4463 (ID = 643853842441830400)
# Version 11.0
# Pycord v2.3



# ===== IMPORTS =====



import discord , json , os
from discord.ext import commands as cmds
__location__ = os.path.realpath(os.path.join(os.getcwd() , os.path.dirname(__file__)))



# ===== BOT CREATION =====



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
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if (type(ctx.author) == discord.Member and ctx.author.nick) else ctx.author , icon_url = ctx.author.avatar)
        if type(ctx) in (cmds.Context , discord.Message) :
            return await ctx.reply(embed = msg)
        elif type(ctx) == discord.ApplicationContext :
            return await ctx.respond(embed = msg)
        else :
            await ctx.send(embed = msg)


    def getting_cmds(self , cog_name) :
        cog = self.get_cog(cog_name)
        if not cog :
            return "Fuck me :/"
        for command in cog.get_commands() :
            if isinstance(command , discord.commands.SlashCommandGroup) :
                for sub_command in command.walk_commands() :
                    yield sub_command
            else :
                yield command


    async def check_owner(self , ctx) :
        if ctx.guild.owner == ctx.author :
            return True
        await self.send(ctx , "This command can only be used by the owner!" , 0xff7f00)
        return False


    async def check_staff(self , ctx) :
        if ctx.author.guild_permissions.administrator :
            return True
        data = self.open_data(ctx)
        staff_roles = data["Data"]["Staff Roles"] if "Staff Roles" in data["Data"] else ()
        for role in ctx.author.roles :
            if role.id in staff_roles :
                return True
        cmds_perms = {
            "clear" : discord.Permissions(manage_messages = True),
            "kick" : discord.Permissions(kick_members = True),
            "ban" : discord.Permissions(ban_members = True),
            "unban" : discord.Permissions(ban_members = True),
            "add" : discord.Permissions(manage_roles = True),
            "remove" : discord.Permissions(manage_roles = True),
            "lock" : discord.Permissions(manage_channels = True),
            "unlock" : discord.Permissions(manage_channels = True),
            "slowmode" : discord.Permissions(manage_channels = True)
        }
        if ctx.channel.permissions_for(ctx.author) >= cmds_perms[ctx.command.name] :
            return True
        await self.send(ctx , "This command can only be used by staff members, or by having specific permissions!" , 0xff7f00)


    async def check_vc(self , ctx) :
        data = self.open_data(ctx)
        author_id = str(ctx.author.id)
        if author_id in data and "VC" in data[author_id] :
            return True
        await self.send(ctx , "You have to be in your voice channel to use this command!" , 0xff7f00)
        return False



bot = MyBot(command_prefix = "p!" , help_command = None , intents = discord.Intents.all())



# ===== EVENTS =====



@bot.event # Bot joins a server
async def on_guild_join(guild) :
    guild_id = str(guild.id)
    bot.data[guild_id] = {"Data" : {}}
    with open(os.path.join(__location__ , "data.json") , "w") as f :
        json.dump(bot.data , f , indent = 4)
    msg = discord.Embed(title = "Hi :)" , description = f"Thank you for adding me to `{guild.name}` !\nType `/help` to see my commands." , color = 0x00ff00)
    for text_channel in guild.text_channels :
        try :
            await text_channel.send(embed = msg)
        except discord.HTTPException :
            print("http exception")
        else :
            break


@bot.event # Bot leaves a server
async def on_guild_remove(guild) :
    guild_id = str(guild.id)
    bot.data.pop(guild_id)
    with open(os.path.join(__location__ , "data.json") , "w") as f :
        json.dump(bot.data , f , indent = 4)


@bot.event # Member leaves a server
async def on_member_leave(member) :
    member_id = str(member.id)
    data = bot.open_data(member)
    if member_id in data :
        data.pop(member_id)
        bot.save_data(member , data)


@bot.event # Slash command got error
async def on_application_command_error(ctx , error) :
    if type(error) in (cmds.CommandOnCooldown , cmds.CommandNotFound , cmds.NotOwner) :
        return
    await ctx.user.create_dm()
    if ctx.channel.id == ctx.user.dm_channel.id :
        msg = await bot.send(ctx , "This command can only be used in a server!" , 0xff7f00)
    elif isinstance(error , cmds.MissingPermissions) :
        if "YourRoleTooLow" in error.missing_permissions :
            user = ctx.guild.get_member(int(error.missing_permissions[1]))
            msg = await bot.send(ctx , f"{user.mention} has higher roles than your roles!" , 0xff7f00)
        else :
            perms = ", ".join(error.missing_permissions).replace("_" , " ")
            msg = await bot.send(ctx , f"You don't have the `{perms}` permission to use this command!" , 0xff7f00)
    elif isinstance(error , cmds.BotMissingPermissions) :
        if "MyRoleTooLow" in error.missing_permissions :
            user = ctx.guild.get_member(int(error.missing_permissions[1]))
            msg = await bot.send(ctx , f"{user.mention} has higher roles than my roles!" , 0xff7f00)
        elif not ("send_messages" in error.missing_permissions or "embed_links" in error.missing_permissions) :
            perms = ", ".join(error.missing_permissions).replace("_" , " ")
            msg = await bot.send(error , f"I don't have the `{perms}` permission to use this command!" , 0xff7f00)
    elif isinstance(error , cmds.UserNotFound) :
        msg = await bot.send(ctx , f"Enter a valid user ID!" , 0xff7f00)
    elif type(error) != discord.CheckFailure :
        print("===== Slash Command Got Error =====")
        print(f"Guild >>> {ctx.guild}  /  {ctx.guild.id}")
        print(f"Channel >>> {ctx.channel.name}  /  {ctx.channel.id}")
        print(f"Type Error >>> {type(error)}")
        print(f"Error >>> {error}")
        print(f"User >>> {ctx.user} ({ctx.user.id})")
        print("\nRaised Error:\n")
        raise error


@bot.event # Bot starts
async def on_ready() :
    print("I'm Ready!")



# ===== BOT START =====



bot.load_extension("Cogs.Owner_Commands")
bot.load_extension("Cogs.Staff_Commands")
bot.load_extension("Cogs.Fun_Commands")
bot.load_extension("Cogs.Private_VC_Commands")
bot.load_extension("Cogs.Other_Commands")



bot.run("BOT TOKEN HERE")
