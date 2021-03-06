import discord
from discord.ext import commands as cmds

TheBot = None



class Staff_Commands(cmds.Cog , name = "staff" , description = "Commands that can only be used by staff or by having permissions.") :
    def __init__(self , bot) : self.bot = bot


    async def check_staff(ctx) : return await TheBot.check_staff(ctx)


    @cmds.command(name = "warn" , description = "`warn <member> <reason>` Warns a member with the given reason. Can only be used by staff.") # Warn a member
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.check(check_staff)
    async def warn(self , ctx , member : discord.Member = None , * , reason = "Not provided") :
        if not member : raise cmds.MemberNotFound(member)
        elif member == ctx.author : return await self.bot.send(ctx , "You can't warn yourself!" , 0xffff00)
        elif member == ctx.me : return await self.bot.send(ctx , "You can't warn me!" , 0xffff00)
        author_position = ctx.author.top_role
        owner = ctx.guild.owner
        member_position = member.top_role
        member_id = str(member.id)
        if ctx.author != owner and member_position >= author_position : raise cmds.MissingPermissions(member_id)
        data = self.bot.open_data(ctx)
        if member_id in data :
            if "Warnings" in data[member_id] : data[member_id]["Warnings"].append(reason)
            else : data[member_id]["Warnings"] = [reason]
        else : data[member_id] = {"Warnings" : [reason]}
        self.bot.save_data(ctx , data)
        warnings = data[member_id]["Warnings"]
        msg_1 = discord.Embed(description = f"**{ctx.author.mention} warned {member.mention} !**" , color = 0xff0000)
        msg_1.add_field(name = f"Reason:" , value = reason , inline = False)
        msg_1.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await ctx.reply(embed = msg_1)
        msg_2 = discord.Embed(title = f"You have been warned in `{ctx.guild.name}` !" , description = f"**{ctx.author.mention} warned you!**" , color = 0xff0000)
        msg_2.add_field(name = f"Reason:" , value = reason , inline = False)
        msg_2.add_field(name = f"Total warnings:" , value = "".join(f"**{i+1}:** {warnings[i]}\n" for i in range(len(warnings))) or f"{member.mention} has no warnings." , inline = False)
        msg_2.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await member.send(embed = msg_2)


    @cmds.command(name = "unwarn" , description = "`unwarn <member> <reason>` Unwarns a member with the given reason. Can only be used by staff.") # Unwarn a member
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.check(check_staff)
    async def unwarn(self , ctx , member : discord.Member = None , index = None , * , reason = "Not provided") :
        if not member : raise cmds.MemberNotFound(member)
        elif member == ctx.author : return await self.bot.send(ctx , "You can't unwarn yourself!" , 0xffff00)
        elif member == ctx.me : return await self.bot.send(ctx , "You can't unwarn me!" , 0xffff00)
        else :
            try : index = int(index)
            except : return await self.bot.send(ctx , "You didn't provide the index of the warning!" , 0xff7f00)
        author_position = ctx.author.top_role
        owner = ctx.guild.owner
        member_position = member.top_role
        if ctx.author != owner and member_position >= author_position : return await self.bot.send(ctx , f"{member.mention} roles are higher than your roles!" , 0xff7f00)
        member_id = str(member.id)
        data = self.bot.open_data(ctx)
        if member_id in data and "Warnings" in data[member_id] :
            if index > len(data[member_id]["Warnings"]) : return await self.bot.send(ctx , f"{member.mention} doesn't have `{index}` warnings!" , 0xffff00)
            else :
                warning = data[member_id]["Warnings"].pop(index - 1)
                if data[member_id]["Warnings"] == [] :
                    data[member_id].pop("Warnings")
                    if data[member_id] == {} : data.pop(member_id)
                self.bot.save_data(ctx , data)
        else : return await self.bot.send(ctx , f"{member.mention} doesn't have any warnings!" , 0xffff00)
        warnings = data[member_id]["Warnings"] if member_id in data and "Warnings" in data[member_id] else ()
        msg_1 = discord.Embed(title = f"Rmoved the `{index}` warning!" , description = f"**{ctx.author.mention} removed the `{index}` warning from {member.mention} !**" , color = 0x00ff00)
        msg_1.add_field(name = f"Removed warning:" , value = warning , inline = False)
        msg_1.add_field(name = f"Reason:" , value = reason , inline = False)
        msg_1.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await ctx.reply(embed = msg_1)
        msg_2 = discord.Embed(title = f"You have been unwarned in `{ctx.guild.name}` !" , description = f"**{ctx.author.mention} removed the {index} warning from you!**" , color = 0x00ff00)
        msg_2.add_field(name = f"Removed warning:" , value = warning , inline = False)
        msg_2.add_field(name = f"Reason:" , value = reason , inline = False)
        msg_2.add_field(name = f"Total warnings:" , value = "".join(f"**{i+1}:** {warnings[i]}\n" for i in range(len(warnings))) or f"**{member.mention} has no warnings.**" , inline = False)
        msg_2.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await member.send(embed = msg_2)


    @cmds.command(name = "warnings" , description = "`warnings <member>` Shows all the warnings the given member has. Can only be used by staff.") # Sends member warnings
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.check(check_staff)
    async def warnings(self , ctx , * , member : discord.Member = None) :
        if not member : raise cmds.MemberNotFound(member)
        data = self.bot.open_data(ctx)
        member_id = str(member.id)
        warnings = data[member_id]["Warnings"] if member_id in data and "Warnings" in data[member_id] else ()
        msg = discord.Embed(title = "Total warnings:" , description = "\n".join(f"**{i+1}:** {warning}" for i , warning in enumerate(warnings)) or f"{member.mention} has no warnings." , color = 0x00ff00)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await ctx.reply(embed = msg)


    @cmds.command(name = "clear" , description = "`clear <amount>` Deletes the given amount of messages.") # Clearing messages
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.has_permissions(manage_messages = True)
    async def clear(self , ctx , amount = "None") :
        if not amount.isdigit() : return await self.bot.send(ctx , "You didn't provide an amount!" , 0xff7f00)
        amount = int(amount)
        if amount > 100 :
            await self.bot.send(ctx , "I can't delete more than 100 messages at a time!" , 0xffff00)
        elif amount <= 0 :
            await ctx.send(";-;")
        else :
            msg = discord.Embed(description = f"**Cleared `{amount}` messages!**" , color = 0x00ff00)
            await ctx.channel.purge(limit = amount + 1)
            await ctx.send(ctx.author.mention , embed = msg)


    @cmds.command(name = "kick" , description = "`kick <member> <reason>` Kicks the given member.") # Kicking members
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.has_permissions(kick_members = True)
    async def kick(self , ctx , member : discord.Member = None , * , reason = "Not provided") :
        if not member : raise cmds.MemberNotFound(member)
        author_position = ctx.author.top_role
        member_position = member.top_role
        if member == ctx.me : await self.bot.send(ctx , "I can't kick myself!" , 0xff7f00)
        elif member == ctx.guild.owner : await self.bot.send(ctx , "I can't kick the owner!" , 0xff7f00)
        elif member_position >= author_position : await self.bot.send(ctx , f"{member.mention} has higher roles than your roles!" , 0xff7f00)
        else :
            await member.kick(reason = reason)
            msg = discord.Embed(description = f"{ctx.author.mention} kicked `{member}` !" , color = 0xff0000)
            msg.add_field(name = "Reason:" , value = reason)
            msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
            await ctx.reply(embed = msg)


    @cmds.command(name = "ban" , description = "`ban <member> <reason>` Bans the given member.") # Banning members
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.has_permissions(ban_members = True)
    async def ban(self , ctx , user : discord.User = None , * , reason = "Not provided") :
        if not user : raise cmds.UserNotFound(user)
        elif not ctx.guild.get_member(user) :
            await ctx.guild.ban(user , reason = reason)
            msg = discord.Embed(description = f"**{ctx.author.mention} banned {user} !**" , color = 0xff0000)
            msg.add_field(name = "Reason:" , value = reason)
            msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
            await ctx.reply(embed = msg)
        elif user == ctx.me : await self.bot.send(ctx , "I can't ban myself!" , 0xff7f00)
        elif user == ctx.guild.owner : await self.bot.send(ctx , "I can't ban the owner!" , 0xff7f00)
        elif user.top_role >= ctx.author.top_role : await self.bot.send(ctx , f"{user.mention} has higher roles than your roles!" , 0xff7f00)
        elif user.top_role >= ctx.me.top_role : await self.bot.send(ctx , f"{user.mention} has higher roles than my roles!" , 0xff7f00)
        else :
            await ctx.guild.ban(user , reason = reason)
            msg = discord.Embed(description = f"**{ctx.author.mention} banned `{user}` !**" , color = 0xff0000)
            msg.add_field(name = "Reason:" , value = reason)
            msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
            await ctx.reply(embed = msg)


    @cmds.command(name = "unban" , description = "`unban <member>` Unbans the given user.") # Unbanning members
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.has_permissions(ban_members = True)
    async def unban(self , ctx , * , user : discord.User = None) :
        if not user : raise cmds.UserNotFound(user)
        try : await ctx.guild.unban(user)
        except discord.NotFound : await self.bot.send(ctx , f"`{user}` is not banned!" , 0xffff00)
        else : await self.bot.send(ctx , f"{ctx.author.mention} unbanned `{user}` !" , 0x00ff00)


    @cmds.group(name = "role" , description = "`role add/remove <member> <role>` Adds or removes a role from the given member.") # Role group
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.has_permissions(manage_roles = True)
    async def role_group(self , ctx) :
        if not ctx.invoked_subcommand : await self.bot.send(ctx , "You didn't enter `add` or `remove` !" , 0xff7f00)


    @role_group.command(name = "add") # Role add
    async def add_role(self , ctx , member : discord.Member = None , * , role : discord.Role = None) :
        if not member : raise cmds.MemberNotFound(member)
        elif not role : raise cmds.RoleNotFound(role)
        author = ctx.author
        owner = ctx.guild.owner
        if author != owner and role >= author.top_role : await self.bot.send(ctx , f"The {role.mention} role is higher than your roles!" , 0xff7f00)
        elif role >= ctx.me.top_role : await self.bot.send(ctx , f"The {role.mention} role is higher than my roles!" , 0xff7f00)
        else :
            if role in member.roles : await self.bot.send(ctx , f"{member.mention} already has the {role.mention} role!" , 0xffff00)
            else :
                await member.add_roles(role)
                await self.bot.send(ctx , f"Added the {role.mention} role to {member.mention} !" , 0x00ff00)


    @role_group.command(name = "remove") # Role remove
    async def remove_role(self , ctx , member : discord.Member = None , * , role : discord.Role = None) :
        if not member : raise cmds.MemberNotFound(member)
        elif not role : raise cmds.RoleNotFound(role)
        author = ctx.author
        owner = ctx.guild.owner
        if author != owner and role >= author.top_role : await self.bot.send(ctx , f"The {role.mention} role is higher than your roles!" , 0xff7f00)
        elif role >= ctx.me.top_role : await self.bot.send(ctx , f"The {role.mention} role is higher than my roles!" , 0xff7f00)
        else :
            if role not in member.roles : await self.bot.send(ctx , f"{member.mention} already doesn't have the {role.mention} role!" , 0xffff00)
            else :    
                await member.remove_roles(role)
                await self.bot.send(ctx , f"Removed the {role.mention} role from {member.mention} !" , 0x00ff00)


    @cmds.command(name = "lockdown" , description = "`lockdown <text-channel>` Locks the given channel from everyone.") # Locks the channel from everyone
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.has_permissions(manage_channels = True)
    async def lockdown(self , ctx , * , channel : discord.TextChannel = None) :
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role , send_messages = False)
        await channel.set_permissions(ctx.me , send_messages = True)
        await self.bot.send(ctx , f"Locked down {channel.mention} !" , 0x00ff00)


    @cmds.command(name = "unlockdown" , description = "`unlockdown <text-channel>` Unlocks the given channel from everyone.") # Unlocks the channel from everyone
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.has_permissions(manage_channels = True)
    async def unlockdown(self , ctx , * , channel : discord.TextChannel = None) :
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role , send_messages = None)
        await channel.set_permissions(ctx.me , overwrite = None)
        await self.bot.send(ctx , f"Unlocked down {channel.mention} !" , 0x00ff00)


    @cmds.command(name = "slowmode" , aliases = ["Slowmode" , "SLOWMODE" , "sw" , "Sw" , "SW"] , description = "`slowmode <seconds> <text-channel>` Sets the slowmode of the given channel as the given amount of seconds. ")
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.has_permissions(manage_channels = True)
    async def slowmode(self , ctx , seconds = 0 , * , channel : discord.TextChannel = None) :
        if not seconds.isdigit() : return await self.bot.send(ctx , "You didn't provide a number of seconds!" , 0xff7f00)
        seconds = int(seconds)
        if seconds < 0 : return await self.bot.send(ctx , "Provide a positive number of seconds!" , 0xff7f00)
        channel = channel or ctx.channel
        await channel.edit(slowmode_delay = seconds)
        await self.bot.send(ctx , f"Set slowmode to {seconds} in {channel.mention} !" , 0x00ff00)



def setup(bot) :
    global TheBot
    TheBot = bot
    bot.add_cog(Staff_Commands(bot))