import discord
from discord.ext import commands as cmds



class Owner_Commands(cmds.Cog , name = "Owner" , description = "Commands that can only be used by the owner of the server.") :    
    def __init__(self , bot) :
        self.bot = bot


    async def cog_check(self , ctx) :
        return await self.bot.check_owner(ctx)


    staff_role_commands = discord.commands.SlashCommandGroup("staff_role" , "Staff Roles Commands.")


    @staff_role_commands.command(name = "list" , description = "Shows the list of all the staff roles.") # Staff list roles
    @cmds.cooldown(rate = 2 , per = 1)
    async def staff_list(self , ctx) :
        data = self.bot.open_data(ctx)
        if "Staff Roles" not in data["Data"] :
            return await self.bot.send(ctx , "There are no staff roles!" , 0xffff00)
        roles = [ctx.guild.get_role(role_id) for role_id in data["Data"]["Staff Roles"]]
        roles = [role.mention for role in roles if role]
        if roles :
            await self.bot.send(ctx , f"Staff Roles: {', '.join(roles)}" , 0x00ff00)
        else :
            return await self.bot.send(ctx , "There are no staff roles!" , 0xffff00)


    @staff_role_commands.command(name = "add" , description = "Adds the given role to the staff role list") # Staff add role
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("role" , description = "Enter the role to add to staff.")
    async def staff_add(self , ctx , role : discord.Role) :
        data = self.bot.open_data(ctx)
        if "Staff Roles" in data["Data"] and role.id in data["Data"]["Staff Roles"] :
            return await self.bot.send(ctx , f"The {role.mention} role is already a staff role!" , 0xffff00)
        elif "Staff Roles" not in data["Data"] :
            data["Data"]["Staff Roles"] = [role.id]
        else :
            data["Data"]["Staff Roles"].append(role.id)
        self.bot.save_data(ctx , data)
        await self.bot.send(ctx , f"Added the {role.mention} role to the staff roles!" , 0x00ff00)


    @staff_role_commands.command(name = "remove" , description = "Removes the given role from the staff role list") # Staff remove role
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("role" , description = "Enter the role to remove from staff.")
    async def staff_remove(self , ctx , role : discord.Role) :
        data = self.bot.open_data(ctx)
        if "Staff Roles" not in data["Data"] or role.id not in data["Data"]["Staff Roles"] :
            return await self.bot.send(ctx , f"The {role.mention} role is already not a staff role!" , 0xffff00)
        elif "Staff Roles" not in data["Data"] :
            data["Data"]["Staff Roles"].remove(role.id)
            if data["Data"]["Staff Roles"] == [] :
                data.pop("Staff Roles")
        self.bot.save_data(ctx , data)
        await self.bot.send(ctx , f"Removed the {role.mention} role from the staff roles!" , 0x00ff00)


    @cmds.slash_command(name = "autovc" , description = "When a user connects to this channel they will be given a private voice channel.") # Create the automatic voice channels
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("join_vc" , default = None , description = "Enter the voice channel to become automatic. Don't enter anything to disable it.")
    async def autovc(self , ctx , join_vc : discord.VoiceChannel) :
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