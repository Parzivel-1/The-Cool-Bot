import discord
from discord.ext import commands as cmds

TheBot = None



class Owner_Commands(cmds.Cog , name = "owner" , description = "Commands that can only be used by the owner of the server.") :    
    def __init__(self , bot) : self.bot = bot


    async def check_owner(ctx) : return await TheBot.check_owner(ctx)


    @cmds.command(name = "prefixset" , description = "`prefixset <prefix>` Changes the prefix of the bot.") # Changing prefix
    @cmds.cooldown(rate = 3 , per = 1)
    async def prefixset(self , ctx , prefix = None) :
        if not prefix : await self.bot.send(ctx , "You didn't enter a prefix!" , 0xff7f00)
        elif prefix == ctx.prefix : await self.bot.send(ctx , f"`{prefix}` is already the prefix!" , 0xffff00)
        else :
            data = self.bot.open_data(ctx)
            data["Data"]["Prefix"] = prefix
            self.bot.save_data(ctx , data)
            await self.bot.send(ctx , f"`{prefix}` is the prefix now!" , 0x00ff00)


    @cmds.group(name = "reacting" , description = "`reacting enable/disable` Enables or disables the bots reaction if someone tries to use a command they can't use.") # Reacting group
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.has_permissions(manage_roles = True)
    async def reacting_group(self , ctx) :
        if not ctx.invoked_subcommand : await self.bot.send(ctx , "You didn't enter `enable` or `disable` !" , 0xff7f00)


    @reacting_group.command(name = "enable") # Reacting enable
    async def enable_reacting(self , ctx) :
        data = self.bot.open_data(ctx)
        reacting_info = data["Data"]["Reacting"]
        if not reacting_info :
            data["Data"]["Reacting"] = True
            self.bot.save_data(ctx , data)
            await self.bot.send(ctx , "Enabled reacting!" , 0x00ff00)
        else : await self.bot.send(ctx , "Reacting is already enabled!" , 0xffff00)


    @reacting_group.command(name = "disable") # Reacting disable
    async def disable_reacting(self , ctx) :
        data = self.bot.open_data(ctx)
        reacting_info = data["Data"]["Reacting"]
        if reacting_info :
            data["Data"]["Reacting"] = False
            self.bot.save_data(ctx , data)
            await self.bot.send(ctx , "Disabled reacting!" , 0x00ff00)
        else : await self.bot.send(ctx , "Reacting is already disabled!" , 0xffff00)


    @cmds.group(name = "staff_role" , description = "`staff_role add/remove <role>` Adds or removes a role from the staff roles. Administrators are automatically considerd staff.") # Staff group
    @cmds.cooldown(rate = 3 , per = 1)
    async def staff_role(self , ctx) :
        if not ctx.invoked_subcommand : await self.bot.send(ctx , "You didn't enter `add` or `remove` !" , 0xff7f00)


    @staff_role.command(name = "add") # Staff add
    async def add_staff(self , ctx , * , role : discord.Role = None) :
        if not role : raise cmds.RoleNotFound(role)
        data = self.bot.open_data(ctx)
        if "Staff Roles" in data["Data"] and role.id in data["Data"]["Staff Roles"] : return await self.bot.send(ctx , f"The `{role.name}` role is already a staff role!" , 0xffff00)
        elif "Staff Rols" not in data["Data"] : data["Data"]["Staff Roles"] = [role.id]
        else : data["Data"]["Staff Rols"].append(role.id)
        self.bot.save_data(ctx , data)
        await self.bot.send(ctx , f"Added the `{role.name}` role to the staff roles!" , 0x00ff00)


    @staff_role.command(name = "remove") # Staff remove
    async def remove_staff(self , ctx , * , role : discord.Role = None) :
        if not role : raise cmds.RoleNotFound(role)
        data = self.bot.open_data(ctx)
        if "Staff Roles" not in data["Data"] or role.id not in data["Data"]["Staff Roles"] : return await self.bot.send(ctx , f"The `{role.name}` role is already not a staff role!" , 0xffff00)
        elif "Staff Roles" not in data["Data"] :
            data["Data"]["Staff Roles"].remove(role.id)
            if data["Data"]["Staff Roles"] == [] : data.pop("Staff Roles")
        self.bot.save_data(ctx , data)
        await self.bot.send(ctx , f"Removed the `{role.name}` role from the staff roles!" , 0x00ff00)


    @cmds.command(name = "autovc" , description = "`autovc <voice-channel>` Sets the voice channel to be automatic, that means anyone who joins it will be given a new voice channel which will be controled by him") # Create the automatic voice channels
    @cmds.cooldown(rate = 3 , per = 1)
    async def autovc(self , ctx , * , join_vc : discord.VoiceChannel = None) :
        if not join_vc : raise cmds.ChannelNotFound(join_vc)
        data = self.bot.open_data(ctx)
        if "Join VC" in data["Data"] and data["Data"]["Join VC"] == join_vc.id : await self.bot.send(ctx , f"{join_vc.mention} is already the voice channel!" , 0xffff00)
        else :
            data["Data"]["Join VC"] = join_vc.id
            self.bot.save_data(ctx , data)
            await self.bot.send(ctx , f"{join_vc.mention} is the automatic voice channel now!" , 0x00ff00)


    @cmds.command(name = "autovcdelete" , description = "`autovcdelete` Disables the automatic voice channel.") # Delete the automatic voice channels
    @cmds.cooldown(rate = 3 , per = 1)
    async def autovcdelete(self , ctx) :
        data = self.bot.open_data(ctx)
        if "Join VC" in data["Data"] :
            data["Data"].pop("Join VC")
            self.bot.save_data(ctx , data)
            await self.bot.send(ctx , "There is no voice channel now!" , 0x00ff00)
        else : await self.bot.send(ctx , "There is no automatic voice channel already!" , 0xffff00)



def setup(bot) : bot.add_cog(Owner_Commands(bot))