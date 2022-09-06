import discord
from discord.ext import commands as cmds

TheBot = None



class Owner_Commands(cmds.Cog , name = "owner" , description = "Commands that can only be used by the owner of the server.") :    
    def __init__(self , bot) : self.bot = bot


    async def check_owner(ctx) : return await TheBot.check_owner(ctx)


    @cmds.slash_command(name = "prefixset" , description = "Changes the prefix of the bot.") # Changing prefix
    @cmds.cooldown(rate = 3 , per = 1)
    async def prefixset(self , ctx , prefix : discord.Option(str , "Enter the prefix you want to change to.")) :
        data = self.bot.open_data(ctx)
        pre_prefix = data["Data"]["Prefix"]
        if prefix == pre_prefix :
            await self.bot.send(ctx , f"`{prefix}` is already the prefix!" , 0xffff00)
        else :
            data = self.bot.open_data(ctx)
            data["Data"]["Prefix"] = prefix
            self.bot.save_data(ctx , data)
            await self.bot.send(ctx , f"`{prefix}` is the prefix now!" , 0x00ff00)


    @cmds.slash_command(name = "staffadd") # Staff add role
    async def staffadd(self , ctx , role : discord.Option(discord.Role , "Enter the role to add to staff.")) :
        data = self.bot.open_data(ctx)
        if "Staff Roles" in data["Data"] and role.id in data["Data"]["Staff Roles"] :
            return await self.bot.send(ctx , f"The {role.mention} role is already a staff role!" , 0xffff00)
        elif "Staff Rols" not in data["Data"] :
            data["Data"]["Staff Roles"] = [role.id]
        else :
            data["Data"]["Staff Rols"].append(role.id)
        self.bot.save_data(ctx , data)
        await self.bot.send(ctx , f"Added the {role.mention} role to the staff roles!" , 0x00ff00)


    @cmds.slash_command(name = "staffremove") # Staff remove role
    async def remove_staff(self , ctx , role : discord.Option(discord.Role , "Enter the role to remove from staff.")) :
        data = self.bot.open_data(ctx)
        if "Staff Roles" not in data["Data"] or role.id not in data["Data"]["Staff Roles"] :
            return await self.bot.send(ctx , f"The {role.mention} role is already not a staff role!" , 0xffff00)
        elif "Staff Roles" not in data["Data"] :
            data["Data"]["Staff Roles"].remove(role.id)
            if data["Data"]["Staff Roles"] == [] :
                data.pop("Staff Roles")
        self.bot.save_data(ctx , data)
        await self.bot.send(ctx , f"Removed the {role.mention} role from the staff roles!" , 0x00ff00)


    @cmds.slash_command(name = "autovc" , description = "Sets the automatic voice channel, upon join it will give a voice channel controled by the user.") # Create the automatic voice channels
    @cmds.cooldown(rate = 3 , per = 1)
    async def autovc(self , ctx , join_vc : discord.Option(discord.VoiceChannel , "Enter the voice channel to become automatic. Don't enter anything to disable it.") = None) :
        data = self.bot.open_data(ctx)
        if not join_vc :
            if "Join VC" in data["Data"] :
                data["Data"].pop("Join VC")
                self.bot.save_data(ctx , data)
                await self.bot.send(ctx , "Disabled automatic voice channel!" , 0x00ff00)
            else :
                await self.bot.send(ctx , "Automatic voice channel is already disabled!" , 0xffff00)
        if "Join VC" in data["Data"] and data["Data"]["Join VC"] == join_vc.id :
            await self.bot.send(ctx , f"{join_vc.mention} is already set to the automatic voice channel!" , 0xffff00)
        else :
            data["Data"]["Join VC"] = join_vc.id
            self.bot.save_data(ctx , data)
            await self.bot.send(ctx , f"{join_vc.mention} is set to the automatic voice channel!" , 0x00ff00)



def setup(bot) :
    bot.add_cog(Owner_Commands(bot))