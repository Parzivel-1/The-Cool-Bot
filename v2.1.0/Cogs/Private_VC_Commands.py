import discord , random
from discord.ext import commands as cmds



class Private_VC_Commands(cmds.Cog , name = "Private VC" , description = "Commands that can only be used while being in your private voice channel") :
    def __init__(self , bot) :
        self.bot = bot


    async def cog_check(self , ctx) :
        return await self.bot.check_vc(ctx)


    private_vc_commands = discord.commands.SlashCommandGroup("private_vc" , "Commands that can only be used while being in your private voice channel.")


    @private_vc_commands.command(name = "give" , description = "Transfers your private voice channel to the given member.")
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("member" , description = "Enter the member to give the voice channel to.")
    async def give(self , ctx , member : discord.Member) :
        if not member.voice or member.voice.channel != ctx.author.voice.channel :
            return await self.bot.send(ctx , f"{member.mention} is not connceted to your voice channel!" , 0xff7e00)
        elif member == ctx.author :
            return await self.bot.send(ctx , "You already have your voice channel!" , 0xff7e00)
        elif member.bot : 
            return await self.bot.send(ctx , "Bots can't have voice channels!" , 0xff7e00)
        data = self.bot.open_data(ctx)
        author_id = str(ctx.author.id)
        member_id = str(member.id)
        private_vc = ctx.author.voice.channel
        data[author_id].pop("VC")
        if data[author_id] == {} :
            data.pop(author_id)
        if member_id in data :
            data[member_id]["VC"] = private_vc.id
        else :
            data[member_id] = {"VC" : private_vc.id}
        self.bot.save_data(ctx , data)
        await self.bot.send(ctx , f"{member.mention} now has {private_vc.mention} !" , 0x00ff00)


    @private_vc_commands.command(name = "max" , description = "Limits your private voice channel to the given amount of members.")
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("amount" , default = 0 , description = "Enter the amount of users to limit your voice channel to.")
    async def max_vc(self , ctx , amount : int) :
        if amount < 0 :
            return await self.bot.send(ctx , "Provide a valide amount!" , 0xff7f00)
        await ctx.author.voice.channel.edit(user_limit = amount)


    @private_vc_commands.command(name = "lock" , description = "Locks your private voice channel from the given member.") # Locks the private voice channel
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("member" , description = "Enter the member to lock your voice channel from.")
    async def lock_vc(self , ctx , member : discord.Member) :
        if member == ctx.author :
            return await self.bot.send(ctx , "You can't lock your voice channel from yourself!" , 0xffff00)
        elif member == ctx.me :
            return await self.bot.send(ctx , "You can't lock me from your voice channel!" , 0xffff00)
        channel = ctx.author.voice.channel
        member_connect = channel.permissions_for(member).connect
        member_admin = member.guild_permissions.administrator
        if member_admin :
            await self.bot.send(ctx , f"You can't lock administrators from your voice channel!" , 0x00ff00)
        elif member_connect :
            await channel.set_permissions(member , connect = False)
            if member.voice and member.voice.channel == channel :
                await member.move_to(None) # type:ignore
            await self.bot.send(ctx , f"Locked {channel.mention} from {member.mention} !" , 0x00ff00)
        else :
            await self.bot.send(ctx , f"{member.mention} is already locked from {channel.mention} !" , 0xffff00)


    @private_vc_commands.command(name = "unlock" , description = "Unlocks your private voice channel from the given member.") # Unlocks the private voice channel
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("member" , description = "Enter the member to unlock your voice channel from.")
    async def unlock_vc(self , ctx , member : discord.Member) :
        if member == ctx.author :
            return await self.bot.send(ctx , "You can't unlock yourself from your voice channel!" , 0xffff00)
        elif member == ctx.me :
            return await self.bot.send(ctx , "You can't unlock me from your voice channel!" , 0xffff00)
        channel = ctx.author.voice.channel
        member_connect = channel.permissions_for(member).connect
        member_admin = member.guild_permissions.administrator
        if not member_admin and not member_connect :
            await channel.set_permissions(member , overwrite = None)
            await self.bot.send(ctx , f"Unlocked {channel.mention} from {member.mention} !" , 0x00ff00)
        else :
            await self.bot.send(ctx , f"{member.mention} is already unlocked from {channel.mention} !" , 0xffff00)


    @private_vc_commands.command(name = "rename" , description = "Renames your private voice channel to the given name.") # Renames the private voice channel
    @cmds.cooldown(rate = 2 , per = 1)
    @discord.commands.option("name" , description = "Enter the name you want to give to your voice channel.")
    async def rename_vc(self , ctx , name : str) :
        if len(name) > 99 :
            return await self.bot.send(ctx , "Names can only be under 100 characters!" , 0xffff00)
        channel = ctx.author.voice.channel
        pre_name = channel.name
        await channel.edit(name = name)
        await self.bot.send(ctx , f"Renamed {channel.mention}\nFrom:\n`{pre_name}`\nTo:\n`{name}` !" , 0x00ff00)


    @cmds.Cog.listener() # Voice state change
    async def on_voice_state_update(self , member , vs_before , vs_after) :
        if member.bot :
            return
        try :
            data = self.bot.open_data(member)
            if "Join VC" not in data["Data"] :
                return
            member_id = str(member.id)
            join_vc_id = data["Data"]["Join VC"]
            join_vc = member.guild.get_channel(join_vc_id)
            category = join_vc.category
            if member_id in data and "VC" in data[member_id] :
                private_vc_id = data[member_id]["VC"]
                private_vc = self.bot.get_channel(private_vc_id)
            else :
                private_vc = "No Voice Channel"
            if vs_before.channel == join_vc and vs_after.channel == private_vc :
                return
            elif vs_before.channel != private_vc and vs_after.channel == join_vc :
                if not category :
                    private_vc = await member.guild.create_voice_channel(f"{member.display_name}'s Voice Channel")
                else :
                    private_vc = await category.create_voice_channel(f"{member.display_name}'s Voice Channel")
                if member_id in data :
                    data[member_id]["VC"] = private_vc.id
                else :
                    data[member_id] = {"VC" : private_vc.id}
                self.bot.save_data(member , data)
                await member.move_to(channel = private_vc)
            elif vs_before.channel == private_vc and vs_after.channel != private_vc and isinstance(private_vc , discord.VoiceChannel) :
                data[member_id].pop("VC")
                if data[member_id] == {} :
                    data.pop(member_id)
                if not private_vc.members :
                    await private_vc.delete()
                    return self.bot.save_data(member , data)
                positions = {}
                for new_member in private_vc.members :
                    if new_member.bot :
                        continue
                    role_pos = new_member.top_role.position
                    if role_pos in positions :
                        positions[role_pos].append(new_member)
                    else :
                        positions[role_pos] = [new_member]
                if not positions :
                    await private_vc.delete()
                    return self.bot.save_data(member , data)
                else :
                    new_member = random.choice(positions[max(positions)])
                    new_member_id = str(new_member.id)
                    if new_member_id in data :
                        data[new_member_id]["VC"] = private_vc.id
                    else :
                        data[new_member_id] = {"VC" : private_vc.id}
                    self.bot.save_data(member , data)
        except Exception as error :
            print("===== ERROR IN VOICE STATE UPDATE =====")
            print(f"Guild >>> {member.guild}")
            print(f"Member >>> {member}    ({member.id})")
            print("=======================================")
            raise error



def setup(bot) :
    bot.add_cog(Private_VC_Commands(bot))