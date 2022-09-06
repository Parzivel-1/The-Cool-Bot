import discord
from discord.ext import commands as cmds



class Other_Commands(cmds.Cog , name = "other" , description = "Other commands.") :
    def __init__(self , bot) : self.bot = bot


    @cmds.group(name = "help" , aliases = ("Help" , "HELP" , "h" , "H") , description = "Shows the help menu") # Help command
    @cmds.cooldown(rate = 3 , per = 1)
    async def help_group(self , ctx) :
        if not ctx.invoked_subcommand :
            msg = discord.Embed(title = "Help Categories:" , description = "`help <category>` See the commands in the given category" , color = 0x00ff00)
            msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
            for cog_name , cog in self.bot.cogs.items() :
                if cog_name == "ignore" : await ctx.send(embed = msg)
                msg.add_field(name = cog_name.capitalize() , value = cog.description)


    @help_group.command(name = "owner")
    async def owner_help(self , ctx , * , cmd = "None") :
        if cmd :
            for bot_cmd in self.bot.cogs["owner"].get_commands() :
                if cmd.lower() == bot_cmd.name :
                    msg = discord.Embed(title = f"{bot_cmd.name} ({', '.join(alias for alias in bot_cmd.aliases)})" if bot_cmd.aliases else bot_cmd.name , description = bot_cmd.description , color = 0x00ff00)
                    return await ctx.send(embed = msg)
        msg = discord.Embed(title = "Owner Commands:" , color = 0x00ff00)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        for cmd in self.bot.cogs["owner"].get_commands() : msg.add_field(name = cmd.name , value = cmd.description , inline = False)
        await ctx.reply(embed = msg)


    @help_group.command(name = "staff")
    async def staff_help(self , ctx , * , cmd = None) :
        if cmd :
            for bot_cmd in self.bot.cogs["staff"].get_commands() :
                if cmd.lower() == bot_cmd.name :
                    msg = discord.Embed(title = f"{bot_cmd.name} ({', '.join(alias for alias in bot_cmd.aliases)})" if bot_cmd.aliases else bot_cmd.name , description = bot_cmd.description , color = 0x00ff00)
                    return await ctx.send(embed = msg)
        msg = discord.Embed(title = "Staff Commands:" , color = 0x00ff00)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        for cmd in self.bot.cogs["staff"].get_commands() : msg.add_field(name = cmd.name , value = cmd.description , inline = False)
        await ctx.reply(embed = msg)


    @help_group.command(name = "private vc" , aliases = ("private",))
    async def private_vc_help(self , ctx , * , cmd = None) :
        if cmd :
            for bot_cmd in self.bot.cogs["private vc"].get_commands() :
                if cmd.lower() == bot_cmd.name :
                    msg = discord.Embed(title = f"{bot_cmd.name} ({', '.join(alias for alias in bot_cmd.aliases)})" if bot_cmd.aliases else bot_cmd.name , description = bot_cmd.description , color = 0x00ff00)
                    return await ctx.send(embed = msg)
        msg = discord.Embed(title = "Private VC Commands:" , color = 0x00ff00)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        for cmd in self.bot.cogs["private vc"].get_commands() : msg.add_field(name = cmd.name , value = cmd.description , inline = False)
        await ctx.reply(embed = msg)


    @help_group.command(name = "fun")
    async def fun_help(self , ctx , * , cmd = None) :
        if cmd :
            for bot_cmd in self.bot.cogs["fun"].get_commands() :
                if cmd.lower() == bot_cmd.name :
                    msg = discord.Embed(title = f"{bot_cmd.name} ({', '.join(alias for alias in bot_cmd.aliases)})" if bot_cmd.aliases else bot_cmd.name , description = bot_cmd.description , color = 0x00ff00)
                    return await ctx.send(embed = msg)
        msg = discord.Embed(title = "Fun Commands:" , color = 0x00ff00)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        for cmd in self.bot.cogs["fun"].get_commands() : msg.add_field(name = cmd.name , value = cmd.description , inline = False)
        await ctx.reply(embed = msg)


    @help_group.command(name = "other")
    async def other_help(self , ctx , * , cmd = None) :
        if cmd :
            for bot_cmd in self.bot.cogs["other"].get_commands() :
                if cmd.lower() == bot_cmd.name :
                    msg = discord.Embed(title = f"{bot_cmd.name} ({', '.join(alias for alias in bot_cmd.aliases)})" if bot_cmd.aliases else bot_cmd.name , description = bot_cmd.description , color = 0x00ff00)
                    return await ctx.send(embed = msg)
        msg = discord.Embed(title = "Other Commands:" , color = 0x00ff00)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        for cmd in self.bot.cogs["other"].get_commands() : msg.add_field(name = cmd.name , value = cmd.description , inline = False)
        await ctx.reply(embed = msg)


    @cmds.slash_command(name = "test" , description = "Test!") # Test command
    @cmds.cooldown(rate = 3 , per = 1)
    async def test(self , ctx) :
        await self.bot.send(ctx , "Success!" , 0x00ff00)


    @cmds.slash_command(name = "ping" , description = "Checks the latency of the bot.") # Sends the ping
    @cmds.cooldown(rate = 3 , per = 1)
    async def ping(self , ctx) :
        latency = round(self.bot.latency * 1000)
        await self.bot.send(ctx , f"Pong! `{latency}ms`" , 0x00ff00)


    @cmds.slash_command(name = "info" , description = "Shows information about the given member") # Sends member info
    @cmds.cooldown(rate = 3 , per = 1)
    async def info(self , ctx , member : discord.Option(discord.Member , "Enter the member who you want to see the information of.") = None) :
        member = member or ctx.author
        owner = ctx.guild.owner
        member_id = str(member.id)
        data = self.bot.open_data(ctx)
        member_info = data[member_id] if member_id in data else {}
        kdr = member_info["KDR"] if "KDR" in member_info else [0,0,0]
        roles = list(member.roles)[::-1]
        roles.remove(ctx.guild.default_role)
        if not roles :
            text = f"{member.display_name} doesn't have any roles."
        else :
            text = "\n".join(role.mention for role in roles)
        msg = discord.Embed(title = "Member Information:" , color = 0x00ff00)
        if member == owner :
            msg.add_field(name = "The Owner:" , value = f"{member.display_name} is the owner of the server!" , inline = False)
        msg.add_field(name = "ID, User:" , value = f"ID: {member_id} , User: {member.mention}")
        msg.add_field(name = "User Created At:" , value = member.created_at.strftime(r"%d/%m/%Y, %H:%M"))
        msg.add_field(name = "Joined Server At:" , value = member.joined_at.strftime(r"%d/%m/%Y, %H:%M"))
        msg.add_field(name = "K/D/R:" , value = f"Killed: {kdr[0]} , Died: {kdr[1]} , Revived: {kdr[2]}" , inline = False)
        msg.add_field(name = f"{len(roles)} Roles:" , value = text , inline = False)
        msg.set_image(url = member.avatar)
        if member.banner : msg.set_thumbnail(url = member.banner.url)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await ctx.respond(embed = msg)


    @cmds.slash_command(name = "server" , description = "Shows information about the server.") # Sends server info
    @cmds.cooldown(rate = 3 , per = 1)
    async def server(self , ctx) :
        owner = ctx.guild.owner
        member_count = ctx.guild.member_count
        online_members = len([member for member in ctx.guild.members if member.status == discord.Status.online])
        offline_members = member_count - online_members
        roles_count = len(ctx.guild.roles)
        emojis_count = len(ctx.guild.emojis)
        vc_count = len(ctx.guild.voice_channels)
        tc_count = len(ctx.guild.text_channels)
        msg = discord.Embed(title = "Server Information:" , color = 0x00ff00)
        msg.add_field(name = "Prefix:" , value = self.bot.command_prefix(self.bot , ctx)[2])
        msg.add_field(name = "THE OWNER:" , value = owner.mention)
        msg.add_field(name = "ID, Name:" , value = f"ID: {ctx.guild.id} , Name: {ctx.guild.name}")
        msg.add_field(name = "Server Created At:" , value = ctx.guild.created_at.strftime(r"%d/%m/%Y, %H:%M"))
        msg.add_field(name = "All Members:" , value = member_count)
        msg.add_field(name = "Members Online:" , value = online_members)
        msg.add_field(name = "Members Offline:" , value = offline_members)
        msg.add_field(name = "Roles:" , value = roles_count)
        msg.add_field(name = "Emojis:" , value = emojis_count)
        msg.add_field(name = "Voice Channels:" , value = vc_count)
        msg.add_field(name = "Text Channels:" , value = tc_count)
        if ctx.guild.banner :
            msg.set_thumbnail(url = ctx.guild.banner.url)
        if ctx.guild.icon :
            msg.set_image(url = ctx.guild.icon.url)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await ctx.respond(embed = msg)



def setup(bot) : 
    bot.add_cog(Other_Commands(bot))