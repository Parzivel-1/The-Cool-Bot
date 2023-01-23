import discord
from discord.ext import commands as cmds



class Fun_Commands(cmds.Cog , name = "Fun" , description = "Commands that don't do something useful, used for fun.") :
    def __init__(self , bot) :
        self.bot = bot


    @cmds.slash_command(name = "kill" , description = "Kills the given member!!!") # Kills someone
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("dead" , description = "Enter the member to kill!!!")
    async def kill(self , ctx , dead : discord.Member) :
        killer = ctx.author
        killer_id = str(killer.id)
        dead_id = str(dead.id)
        if dead == ctx.me :
            return await self.bot.send(ctx , "You can't kill me, I'm immortal!" , 0xffff00)
        elif killer == dead :
            return await self.bot.send(ctx , "You can't kill yourself, I don't support suicide!" , 0xffff00)
        data = self.bot.open_data(ctx)
        if dead_id in data :
            if "KDR" in data[dead_id] :
                data[dead_id]["KDR"][1] += 1
            else :
                data[dead_id]["KDR"] = [0 , 1 , 0]
        else : data[dead_id] = {"KDR" : [0 , 1 , 0]}
        if killer_id in data :
            if "KDR" in data[killer_id] :
                data[killer_id]["KDR"][0] += 1
            else :
                data[killer_id]["KDR"] = [1 , 0 , 0]
        else :
            data[killer_id] = {"KDR" : [1 , 0 , 0]}
        self.bot.save_data(ctx , data)
        kdr_1 = data[killer_id]["KDR"]
        kdr_2 = data[dead_id]["KDR"]
        desc = f"**{killer.mention} K/D/R:** \n Killed: `{kdr_1[0]}` , Died: `{kdr_1[1]}` , Revived: `{kdr_1[2]}` \n\n **{dead.mention} K/D/R:** \n Killed: `{kdr_2[0]}` , Died: `{kdr_2[1]}` , Revived: `{kdr_2[2]}`"
        msg = discord.Embed(title = f"`{killer.display_name}` KILLED `{dead.display_name}` !!!" , description = desc , color = 0xff0000)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await ctx.respond(embed = msg)


    @cmds.slash_command(name = "revive" , description = "Revives the given member!!!") # Revives someone
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("alive" , description = "Enter the member to revive!!!")
    async def revive(self , ctx , alive : discord.Member) :
        healer = ctx.author
        healer_id = str(healer.id)
        alive_id = str(alive.id)
        if alive == ctx.me :
            return await self.bot.send(ctx , "You can't revive me, I'm immortal!" , 0xffff00)
        elif healer == alive :
            return await self.bot.send(ctx , "You can't revive yourself, it's not possible!" , 0xffff00)
        data = self.bot.open_data(ctx)
        if alive_id in data and "KDR" in data[alive_id] :
            data[alive_id]["KDR"][1] -= 1
            if data[alive_id]["KDR"] == [0 , 0 , 0] :
                data[alive_id].pop("KDR")
                if data[alive_id] == {} : data.pop(alive_id)
        else :
            return await self.bot.send(ctx , "You can't revive someone who has no deaths!" , 0xffff00)
        if healer_id in data :
            if "KDR" in data[healer_id] :
                data[healer_id]["KDR"][2] += 1
            else :
                data[healer_id]["KDR"] = [0 , 0 , 1]
        else :
            data[healer_id] = {"KDR" : [0 , 0 , 1]}
        self.bot.save_data(ctx , data)
        kdr_1 = data[healer_id]["KDR"]
        kdr_2 = data[alive_id]["KDR"] if alive_id in data and "KDR" in data[alive_id] else [0 , 0 , 0]
        desc = f"**{healer.mention} K/D/R:** \n Killed: `{kdr_1[0]}` , Died: `{kdr_1[1]}` , Revived: `{kdr_1[2]}` \n\n **{alive.mention} K/D/R:** \n Killed: `{kdr_2[0]}` , Died: `{kdr_2[1]}` , Revived: `{kdr_2[2]}`"
        msg = discord.Embed(title = f"`{healer.display_name}` REVIVED `{alive.display_name}` !!!" , description = desc , color = 0x00ff00)
        msg.set_author(name = f"{ctx.author} || {ctx.author.nick}" if ctx.author.nick else ctx.author , icon_url = ctx.author.avatar)
        await ctx.respond(embed = msg)



def setup(bot) :
    bot.add_cog(Fun_Commands(bot))