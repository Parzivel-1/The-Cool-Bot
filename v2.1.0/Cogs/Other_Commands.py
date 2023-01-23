import discord
from discord.ext import commands as cmds



class Other_Commands(cmds.Cog , name = "Other" , description = "Other commands.") :
    def __init__(self , bot) :
        self.bot = bot


    @cmds.slash_command(name = "help" , description = "Shows the help menu.") # Sends the help menu
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("category" , choices = ("Owner" , "Moderation" , "Fun" , "Private VC" , "Other") , description = "Enter the category you want to see the commands of.")
    async def help(self , ctx , category : str) :
        msg = discord.Embed(title = category , color = 0x00ff00)
        for command in self.bot.getting_cmds(category) :
            msg.add_field(name = f"{command.parent} {command.name}" if command.parent else command.name , value = command.description , inline = False)
        await ctx.respond(embed = msg)


    @cmds.slash_command(name = "test" , description = "Test!") # Test command
    @cmds.cooldown(rate = 2 , per = 1)
    async def test(self , ctx) :
        await self.bot.send(ctx , "Success!" , 0x00ff00)


    @cmds.slash_command(name = "ping" , description = "Checks the latency of the bot.") # Sends the ping
    @cmds.cooldown(rate = 2 , per = 1)
    async def ping(self , ctx) :
        latency = round(self.bot.latency * 1000)
        await self.bot.send(ctx , f"Pong! `{latency}ms`" , 0x00ff00)


    @cmds.slash_command(name = "info" , description = "Shows information about the given member") # Sends member info
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("member" , default = None , description = "Enter the member who you want to see the information of.")
    async def info(self , ctx , member : discord.Member) :
        member = member or ctx.author
        member_id = str(member.id)
        data = self.bot.open_data(ctx)
        member_info = data[member_id] if member_id in data else {}
        kdr = member_info["KDR"] if "KDR" in member_info else (0,0,0)
        roles = member.roles[::-1]
        roles.remove(ctx.guild.default_role)
        msg = discord.Embed(title = "Member Information:" , color = member.color if member.color else 0x000000)
        msg.add_field(name = "ID, User:" , value = f"ID: {member_id} , User: {member.mention}" , inline = False)
        msg.add_field(name = "Created At:" , value = member.created_at.strftime(r"%d/%m/%Y, %H:%M"))
        msg.add_field(name = "Joined Server At:" , value = member.joined_at.strftime(r"%d/%m/%Y, %H:%M")) if member.joined_at else None
        msg.add_field(name = "Badges:" , value = ", ".join(flag.name for flag in member.public_flags.all()).replace("_" , " ").title() if member.public_flags.all() else "No Badges." , inline = False)
        msg.add_field(name = "K/D/R:" , value = f"Killed: {kdr[0]} , Died: {kdr[1]} , Revived: {kdr[2]}" , inline = False)
        msg.add_field(name = f"{len(roles)} Roles:" , value = "\n".join(role.mention for role in roles) if roles else "No Roles." , inline = False)
        if member.banner :
            msg.set_thumbnail(url = member.banner)
        msg.set_image(url = member.avatar)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        if member.display_avatar != member.avatar :
            msg2 = discord.Embed(title = "test")
            msg2.set_image(url = member.display_avatar)
            await ctx.respond(embeds = [msg , msg2])
        else :
            await ctx.respond(embed = msg)


    @cmds.slash_command(name = "server" , description = "Shows information about the server.") # Sends server info
    @cmds.cooldown(rate = 2 , per = 1)
    async def server(self , ctx) :
        online_members = len([member for member in ctx.guild.members if member.status == discord.Status.online])
        offline_members = ctx.guild.member_count - online_members
        roles_count = len(ctx.guild.roles)
        emojis_count = len(ctx.guild.emojis)
        vc_count = len(ctx.guild.voice_channels)
        tc_count = len(ctx.guild.text_channels)
        msg = discord.Embed(title = "Server Information:" , color = 0x00ff00)
        msg.add_field(name = "The Owner:" , value = ctx.guild.owner.mention , inline = False)
        msg.add_field(name = "ID, Name:" , value = f"ID: {ctx.guild.id} , Name: {ctx.guild.name}")
        msg.add_field(name = "Server Created At:" , value = ctx.guild.created_at.strftime(r"%d/%m/%Y, %H:%M"))
        msg.add_field(name = "Online Members:" , value = str(online_members))
        msg.add_field(name = "Offline Members:" , value = str(offline_members))
        msg.add_field(name = "Roles:" , value = str(roles_count) , inline = False)
        msg.add_field(name = "Emojis:" , value = str(emojis_count))
        msg.add_field(name = "Voice Channels:" , value = str(vc_count))
        msg.add_field(name = "Text Channels:" , value = str(tc_count))
        if ctx.guild.banner :
            msg.set_thumbnail(url = ctx.guild.banner.url)
        if ctx.guild.icon :
            msg.set_image(url = ctx.guild.icon.url)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await ctx.respond(embed = msg)



def setup(bot) : 
    bot.add_cog(Other_Commands(bot))