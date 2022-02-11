# The Cool Bot
# Created by Parzivel_1#4463 (643853842441830400)
# Version 10.0
# Pycord



# ===== IMPORTS =====



import discord , json , os
from discord.ext import commands as cmds
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))



# ===== BOT CREATION =====



def get_prefix(bot , msg) :
        if isinstance(msg.guild , discord.Guild) :
            guild_id = str(msg.guild.id)
            prefix = bot.data[guild_id]["Data"]["Prefix"]
        else : prefix = "p!"
        return cmds.when_mentioned_or(prefix)(bot , msg)


class MyBot(cmds.Bot) :
    def __init__(self , *args , **kwargs) :
        with open(os.path.join(__location__, "data.json")) as f : self.data = json.load(f)
        super().__init__(*args , **kwargs)


    def open_data(self , ctx) :
        guild_id = str(ctx.guild.id)
        return self.data[guild_id]


    def save_data(self , ctx , guild_data) :
        guild_id = str(ctx.guild.id)
        bot.data[guild_id] = guild_data
        with open(os.path.join(__location__, "data.json") , "w") as f : json.dump(self.data , f , indent = 4)


    async def send(self , ctx , text , color) :
        msg = discord.Embed(description = f"**{text}**" , color = color)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        return await ctx.reply(embed = msg) if type(ctx) in (cmds.Context , discord.Message) else await ctx.send(embed = msg)


    async def check_owner(self , ctx) :
        if ctx.guild.owner == ctx.author : return True
        else :
            await self.bot.send(ctx , "This command can only be used by the owner!" , 0xff7f00)
            return False


    async def check_staff(self , ctx) :
        if ctx.author.guild_permissions.administrator : return True
        else :
            data = self.open_data(ctx)
            staff_roles = data["Data"]["Staff Roles"] if "Staff Roles" in data["Data"] else ()
            if not staff_roles :
                await self.send(ctx , "This command can only be used by the staff members!" , 0xff7f00)
                return False
            else :
                for role in ctx.author.roles :
                    if role.id in staff_roles : return True
                await self.send(ctx , "This command can only be used by the staff members!" , 0xff7f00)
                return False


    async def check_vc(self , ctx) :
        if ctx.command.name == "help" : return True
        data = self.open_data(ctx)
        author_id = str(ctx.author.id)
        if author_id in data and "VC" in data[author_id] : return True
        else :
            await self.send(ctx , "You have to be in your voice channel to use this command!" , 0xff7f00)
            return False


bot = MyBot(command_prefix = get_prefix , help_command = None , intents = discord.Intents.all())



# ===== EVENTS =====



@bot.event # Bot joins a server
async def on_guild_join(guild) :
    parzi = bot.get_user(643853842441830400)
    await parzi.send(f"```py\n Joined Server: \n\n {guild.name} \n {guild.id} ```")
    guild_id = str(guild.id)
    bot.data[guild_id] = {"Data":{"Prefix": "p!" , "Reacting": True}}
    with open(os.path.join(__location__, "data.json") , "w") as f : json.dump(bot.data , f , indent = 4)
    msg = discord.Embed(title = "Hi :)" , description = f"""Thank you for adding me to {guild.name} ! \n My defult prefix is `p!`, but the owner can change it any time. Type `p!help` to know everything that you need to know about me.""" , color = 0x00ff00)
    for text_channel in guild.text_channels :
        try : await text_channel.send(embed = msg)
        except Exception : pass
        else : break


@bot.event # Bot leaves a server
async def on_guild_remove(guild) :
    Parzivel_1 = bot.get_user(643853842441830400)
    await Parzivel_1.send(f"```py\n Left Server: \n\n {guild.name} \n {guild.id} ```")
    guild_id = str(guild.id)
    bot.data.pop(guild_id)
    with open(os.path.join(__location__, "data.json") , "w") as f : json.dump(bot.data , f , indent = 4)


@bot.event # Member joins a server
async def on_member_join(member) :
    if member.bot : return
    elif member.guild.id == 880550855680589836 :
        msg = discord.Embed(title = f"Hi :)" , description = "Make sure to read <#880552882871631943>" , color = 0x00ff00)
        msg.set_thumbnail(url = member.avatar)
        msg = await bot.get_channel(880561333370777601).send(member.mention , embed = msg)
        await msg.add_reaction("👋")
    elif member.guild.id == 760761492453720065 :
        await member.add_roles(member.guild.get_role(813136882191040593))
        msg = discord.Embed(title = f"Hi :)" , description = "Make sure to read <#781273158090752050>" , color = 0x00ff00)
        msg.set_thumbnail(url = member.avatar)
        msg = await bot.get_channel(773199465167323186).send(member.mention , embed = msg)
        await msg.add_reaction("👋")
    elif member.guild.id == 841292233276915712 :
        msg = discord.Embed(title = f"Hi :)" , description = "Make sure to read <#859509133040156712>" , color = 0x00ff00)
        msg.set_thumbnail(url = member.avatar)
        msg = await bot.get_channel(859498467227205682).send(member.mention , embed = msg)
        await msg.add_reaction("👋")


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
    if not ctx.channel.guild or type(error) in (cmds.CommandOnCooldown , cmds.TooManyArguments , cmds.CommandNotFound , cmds.NotOwner) or not data["Data"]["Reacting"] : return
    elif isinstance(ctx.channel , discord.DMChannel) : await bot.send(ctx , "This command can only be used in a server!" , 0xff7f00)
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


@bot.event # Reaction Add
async def on_raw_reaction_add(pyld) :
    if pyld.member.bot : return
    elif pyld.message_id == 869345039308955769 :
        role = pyld.member.guild.get_role(859499712893026334)
        await pyld.member.add_roles(role)
    elif pyld.message_id == 880930699870359672 :
        role = pyld.member.guild.get_role(880580282053451796)
        await pyld.member.add_roles(role)
    elif pyld.message_id == 870057482251280415 :
        roles = {860304500653162516 : 860302761497198652 , 860304177867259934 : 841559631775268864 , 870051215541698600 : 860859599165849651}
        role = pyld.member.guild.get_role(roles[pyld.emoji.id])
        await pyld.member.add_roles(role)


@bot.event # Reaction Remove
async def on_raw_reaction_remove(pyld) :
    guild = bot.get_guild(pyld.guild_id)
    member = guild.get_member(pyld.user_id)
    if pyld.message_id == 870057482251280415 :
        emoji_role = {860304500653162516 : 860302761497198652 , 860304177867259934 : 841559631775268864 , 870051215541698600 : 860859599165849651}
        role = guild.get_role(emoji_role[pyld.emoji.id])
        await member.remove_roles(role)


@bot.event # Every message
async def on_message(msg) :
    if msg.author.bot : return
    if msg.guild and msg.content in (msg.guild.me.mention , bot.user.mention) :
        await bot.send(msg , f"My prefix here is `{bot.command_prefix(bot , msg)[2]}` !" , 0x00ff00)
    elif not (msg.guild and msg.guild.id in (760761492453720065 , 890204187982458901) and msg.channel.id not in (890224245265817642 , 794926006611345419 , 773201130632511528 , 773201742555774976 , 819952133486411846) and msg.author.id != 643853842441830400) :
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
bot.load_extension("Cogs.Ignore_Commands")
bot.load_extension("Cogs.Loops")

bot.run("Bot Token Here")