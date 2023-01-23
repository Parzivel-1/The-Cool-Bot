import discord
from discord.ext import commands as cmds



class Staff_Commands(cmds.Cog , name = "Staff" , description = "Commands that can only be used by staff or by having permissions.") :
    def __init__(self , bot) :
        self.bot = bot


    async def cog_check(self , ctx) :
        return await self.bot.check_staff(ctx)


    role_commands = discord.commands.SlashCommandGroup("role" , "Staff Roles Commands.")


    @cmds.slash_command(name = "warn" , description = "Warns a member with the given reason, can only be used by staff.") # Warn a member
    @cmds.cooldown(rate = 2 , per = 1)

    @discord.commands.option("member" , description = "Enter the member to warn.")
    @discord.commands.option("reason" , default = "Not provied" , description = "Enter the reason.")
    async def warn(self , ctx , member : discord.Member , reason : str) :
        if member == ctx.author :
            return await self.bot.send(ctx , "You can't warn yourself!" , 0xffff00)
        elif member == ctx.me :
            return await self.bot.send(ctx , "You can't warn me!" , 0xffff00)
        member_id = str(member.id)
        if ctx.author != ctx.guild.owner and member.top_role >= ctx.author.top_role :
            raise cmds.MissingPermissions(["YourRoleTooLow" , member_id])
        data = self.bot.open_data(ctx)
        if member_id in data :
            if "Warnings" in data[member_id] :
                data[member_id]["Warnings"].append(reason)
            else :
                data[member_id]["Warnings"] = [reason]
        else :
            data[member_id] = {"Warnings" : [reason]}
        self.bot.save_data(ctx , data)
        warnings = data[member_id]["Warnings"]
        msg_1 = discord.Embed(description = f"**{ctx.author.mention} warned {member.mention} !**" , color = 0xff0000)
        msg_1.add_field(name = f"Reason:" , value = reason , inline = False)
        msg_1.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await ctx.respond(embed = msg_1)
        msg_2 = discord.Embed(title = f"You have been warned in `{ctx.guild.name}` !" , description = f"**{ctx.author.mention} warned you!**" , color = 0xff0000)
        msg_2.add_field(name = f"Reason:" , value = reason , inline = False)
        msg_2.add_field(name = f"Total warnings:" , value = "".join(f"**{i+1}:** {warnings[i]}\n" for i in range(len(warnings))) or f"{member.mention} has no warnings." , inline = False)
        msg_2.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await member.send(embed = msg_2)


    @cmds.slash_command(name = "unwarn" , description = "Unwarns a member with the given reason index, can only be used by staff.") # Unwarn a member
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("member" , description = "Enter the member to unwarn.")
    @discord.commands.option("index" , description = "Enter the index of thw warning.")
    @discord.commands.option("reason" , description = "Enter the reason")
    async def unwarn(self , ctx , member : discord.Member , index : int , reason : str) :
        if member == ctx.author :
            return await self.bot.send(ctx , "You can't unwarn yourself!" , 0xffff00)
        elif member == ctx.me :
            return await self.bot.send(ctx , "You can't unwarn me!" , 0xffff00)
        member_id = str(member.id)
        if ctx.author != ctx.guild.owner and member.top_role >= ctx.author.top_role :
            raise cmds.MissingPermissions(["YourRoleTooLow" , member_id])
        data = self.bot.open_data(ctx)
        if member_id in data and "Warnings" in data[member_id] :
            if index > len(data[member_id]["Warnings"]) :
                return await self.bot.send(ctx , f"{member.mention} doesn't have `{index}` warnings!" , 0xffff00)
            else :
                warning = data[member_id]["Warnings"].pop(index - 1)
                if data[member_id]["Warnings"] == [] :
                    data[member_id].pop("Warnings")
                    if data[member_id] == {} :
                        data.pop(member_id)
                self.bot.save_data(ctx , data)
        else :
            return await self.bot.send(ctx , f"{member.mention} doesn't have any warnings!" , 0xffff00)
        warnings = data[member_id]["Warnings"] if member_id in data and "Warnings" in data[member_id] else ()
        msg_1 = discord.Embed(title = f"Rmoved the `{index}` warning!" , description = f"**{ctx.author.mention} removed the `{index}` warning from {member.mention} !**" , color = 0x00ff00)
        msg_1.add_field(name = f"Removed warning:" , value = warning , inline = False)
        msg_1.add_field(name = f"Reason:" , value = reason , inline = False)
        if ctx.author.nick :
            name = f"{ctx.author} || {ctx.author.nick}"
        else :
            name = ctx.author
        msg_1.set_author(name = name , icon_url = ctx.author.avatar)
        await ctx.respond(embed = msg_1)
        msg_2 = discord.Embed(title = f"You have been unwarned in `{ctx.guild.name}` !" , description = f"**{ctx.author.mention} removed the {index} warning from you!**" , color = 0x00ff00)
        msg_2.add_field(name = f"Removed warning:" , value = warning , inline = False)
        msg_2.add_field(name = f"Reason:" , value = reason , inline = False)
        msg_2.add_field(name = f"Total warnings:" , value = "".join(f"**{i+1}:** {warnings[i]}\n" for i in range(len(warnings))) or f"**{member.mention} has no warnings.**" , inline = False)
        msg_2.set_author(name = name , icon_url = ctx.author.avatar)
        await member.send(embed = msg_2)


    @cmds.slash_command(name = "warnings" , description = "Shows all the warnings the given member has. Can only be used by staff.") # Sends member warnings
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("member" , description = "Enter the member to show all of the warnings to.")
    async def warnings(self , ctx , member : discord.Member) :
        data = self.bot.open_data(ctx)
        member_id = str(member.id)
        if member_id in data and "Warnings" in data[member_id] :
            warnings = data[member_id]["Warnings"]
        else :
            warnings = ()
        msg = discord.Embed(title = "Total warnings:" , description = "\n".join(f"**{i+1}:** {warning}" for i , warning in enumerate(warnings)) or f"{member.mention} has no warnings." , color = 0x00ff00)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await ctx.respond(embed = msg)


    @cmds.slash_command(name = "clear" , description = "Deletes the given amount of messages.") # Clearing messages
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("amount" , description = "Enter the amount of messages to delete.")
    async def clear(self , ctx , amount : int) :
        if amount > 100 :
            await self.bot.send(ctx , "I can't delete more than 100 messages at a time!" , 0xffff00)
        elif amount <= 0 :
            await ctx.send(";-;")
        else :
            msg = discord.Embed(description = f"**Cleared `{amount}` messages!**" , color = 0x00ff00)
            await ctx.channel.purge(limit = amount + 1)
            await ctx.send(ctx.author.mention , embed = msg)


    @cmds.slash_command(name = "kick" , description = "Kicks the given member.") # Kicking members
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("member" , description = "Enter the member to kick.")
    @discord.commands.option("reason" , default = "Not provided." , description = "Enter the reason for the kick.")
    async def kick(self , ctx , member : discord.Member , reason : str) :
        if member == ctx.me :
            await self.bot.send(ctx , "I can't kick myself!" , 0xff7f00)
        elif member == ctx.guild.owner :
            await self.bot.send(ctx , "I can't kick the owner!" , 0xff7f00)
        elif member.top_role >= ctx.author.top_role :
            raise cmds.MissingPermissions(["YourRoleTooLow" , str(member.id)])
        elif member.top_role >= ctx.me.top_role :
            raise cmds.BotMissingPermissions(["MyRoleTooLow" , str(member.id)])
        else :
            await member.kick(reason = reason)
            msg = discord.Embed(description = f"{ctx.author.mention} kicked `{member}` !" , color = 0xff0000)
            msg.add_field(name = "Reason:" , value = reason)
            if ctx.author.nick :
                name = f"{ctx.author} || {ctx.author.nick}"
            else :
                name = ctx.author
            msg.set_author(name = name , icon_url = ctx.author.avatar)
            await ctx.respond(embed = msg)


    @cmds.slash_command(name = "ban" , description = "Bans the given user.") # Banning members
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("user_id" , description = "Enter the ID of the user to ban.")
    @discord.commands.option("reason" , default = "Not provided." , description = "Enter the reason for the ban")
    async def ban(self , ctx , user_id : str , reason : str) :
        user = await self.bot.get_or_fetch_user(user_id)
        if not user :
            raise cmds.UserNotFound(user_id)
        elif user == ctx.me :
            await self.bot.send(ctx , "I can't ban myself!" , 0xff7f00)
        elif user == ctx.guild.owner :
            await self.bot.send(ctx , "I can't ban the owner!" , 0xff7f00)
        elif ctx.guild.get_member(user.id) and user.top_role >= ctx.author.top_role :
            raise cmds.MissingPermissions(["YourRoleTooLow" , user_id])
        elif ctx.guild.get_member(user.id) and user.top_role >= ctx.me.top_role :
            raise cmds.BotMissingPermissions(["MyRoleTooLow" , user_id])
        else :
            await ctx.guild.ban(user , reason = reason)
            msg = discord.Embed(description = f"**{ctx.author.mention} banned `{user}` !**" , color = 0xff0000)
            msg.add_field(name = "Reason:" , value = reason)
            if ctx.author.nick :
                name = f"{ctx.author} || {ctx.author.nick}"
            else :
                name = ctx.author
            msg.set_author(name = name , icon_url = ctx.author.avatar)
            await ctx.respond(embed = msg)


    @cmds.slash_command(name = "unban" , description = "Unbans the given user.") # Unbanning members
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("user_id" , description = "Enter the ID of the user to unban.")
    @discord.commands.option("reason" , default = "Not provided." , description = "Enter the reason for the unban.")
    async def unban(self , ctx , user_id : str , reason : str) :
        user = await self.bot.get_or_fetch_user(user_id)
        if not user :
            raise cmds.UserNotFound(user_id)
        elif user == ctx.me :
            return await self.bot.send(ctx , "I can't unban myself!" , 0xff7f00)
        elif user == ctx.guild.owner :
            return await self.bot.send(ctx , "I can't unban the owner!" , 0xff7f00)
        check = False
        async for ban in ctx.guild.bans() :
            if ban.user == user :
                check = True
                break
        if check :
            await ctx.guild.unban(user , reason = reason)
            msg = discord.Embed(description = f"{ctx.author.mention} unbanned `{user}` !" , color = 0xff0000)
            msg.add_field(name = "Reason:" , value = reason)
            if ctx.author.nick :
                name = f"{ctx.author} || {ctx.author.nick}"
            else :
                name = ctx.author
            msg.set_author(name = name , icon_url = ctx.author.avatar)
            await ctx.respond(embed = msg)
        else :
            await self.bot.send(ctx , f"`{user}` is not banned!" , 0xff7f00)


    @role_commands.command(name = "add" , description = "Adds the given role to the given member.") # Role add
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("member" , description = "Enter the member to add the role to.")
    @discord.commands.option("role" , description = "Enter the role to add to the member.")
    async def add_role(self , ctx , member : discord.Member , role : discord.Role) :
        if ctx.author != ctx.guild.owner and role >= ctx.author.top_role :
            await self.bot.send(ctx , f"The {role.mention} role is higher than your roles!" , 0xff7f00)
        elif role >= ctx.me.top_role :
            await self.bot.send(ctx , f"The {role.mention} role is higher than my roles!" , 0xff7f00)
        else :
            if role in member.roles :
                await self.bot.send(ctx , f"{member.mention} already has the {role.mention} role!" , 0xffff00)
            else :
                await member.add_roles(role)
                await self.bot.send(ctx , f"Added the {role.mention} role to {member.mention} !" , 0x00ff00)


    @role_commands.command(name = "remove" , description = "Removes the given role to the given member.") # Role remove
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("member" , description = "Enter the member to remove the role from.")
    @discord.commands.option("role" , description = "Enter the role to remove from the member.")
    async def remove_role(self , ctx , member : discord.Member , role : discord.Role) :
        if ctx.author != ctx.guild.owner and role >= ctx.author.top_role :
            await self.bot.send(ctx , f"The {role.mention} role is higher than your roles!" , 0xff7f00)
        elif role >= ctx.me.top_role :
            await self.bot.send(ctx , f"The {role.mention} role is higher than my roles!" , 0xff7f00)
        elif role not in member.roles :
            await self.bot.send(ctx , f"{member.mention} doesn't have the {role.mention} role!" , 0xffff00)
        else :    
            await member.remove_roles(role)
            await self.bot.send(ctx , f"Removed the {role.mention} role from {member.mention} !" , 0x00ff00)


    @cmds.slash_command(name = "lock" , description = "Locks the given channel from the given role.") # Locks the channel from the given role
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("channel" , description = "Enter the text channel to unlock.")
    @discord.commands.option("role" , description = "Enter the role to unlock the channel from.")
    async def lock(self , ctx , channel : discord.TextChannel , role : discord.Role) :
        await channel.set_permissions(role , send_messages = False)
        await self.bot.send(ctx , f"Locked {channel.mention} from {role.mention} !" , 0x00ff00)


    @cmds.slash_command(name = "unlock" , description = "Unlocks the given channel from the given role.") # Unlocks the channel from given role
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("channel" , description = "Enter the text channel to unlock.")
    @discord.commands.option("role" , description = "Enter the role to unlock the channel from.")
    async def unlock(self , ctx , channel : discord.TextChannel , role : discord.Role) :
        await channel.set_permissions(role , send_messages = True)
        await self.bot.send(ctx , f"Unlocked {channel.mention} from {role.mention} !" , 0x00ff00)


    @cmds.slash_command(name = "slowmode" , description = "Sets the slowmode of the given channel as the given amount of seconds. ")
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("seconds" , default = 0 , description = "Enter the time in seconds to set the slowmode to.")
    @discord.commands.option("channel" , default = None , description = "Enter the text channel to set the slowmode to.")
    async def slowmode(self , ctx , seconds : int , channel : discord.TextChannel) :
        if seconds < 0 :
            return await self.bot.send(ctx , "Provide a positive number of seconds!" , 0xff7f00)
        channel = channel or ctx.channel
        await channel.edit(slowmode_delay = seconds)
        await self.bot.send(ctx , f"Set slowmode to `{seconds}sec` in {channel.mention} !" , 0x00ff00)



def setup(bot) :
    bot.add_cog(Staff_Commands(bot))