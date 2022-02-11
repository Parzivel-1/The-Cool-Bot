from discord.ext import tasks
from discord.ext import commands as cmds



class Loops(cmds.Cog , name = "loops" , description = "Loops") :
    def __init__(self , bot) : self.bot = bot


    @cmds.Cog.listener()
    async def on_ready(self) :
        self.start()


    @tasks.loop(minutes = 5) # Every 5 minutes
    async def every_5_min(self) :
        guild_1 = self.bot.get_guild(760761492453720065)
        channel_1 = guild_1.get_channel(763773278098817026)
        role_1 = guild_1.get_role(813136882191040593)
        await channel_1.edit(name = f"Members: {len(role_1.members)} 👥")
        guild_2 = self.bot.get_guild(841292233276915712)
        channel_2 = guild_2.get_channel(859500385072447488)
        role_2 = guild_2.get_role(859499712893026334)
        await channel_2.edit(name = f"Members: {len(role_2.members)} 👥")
        guild_3 = self.bot.get_guild(880550855680589836)
        channel_3 = guild_3.get_channel(880566316866617384)
        role_3 = guild_3.get_role(880580282053451796)
        await channel_3.edit(name = f"Members: {len(role_3.members)} 👥")


    @tasks.loop(minutes = 20) # Every 20 minutes
    async def every_20_min(self) :
        parzi = self.bot.get_user(643853842441830400)
        await parzi.send(f"***-----------------------------> D E Y N <-----------------------------***" , delete_after = 15)


    def start(self) :
        if not self.every_5_min.is_running() : self.every_5_min.start()
        # if not self.every_20_min.is_running() : self.every_20_min.start()


    def stop(self) :
        if self.every_5_min.is_running() : self.every_5_min.cancel()
        if self.every_20_min.is_running() : self.every_20_min.cancel()


    @cmds.command()
    @cmds.is_owner()
    async def thing(self , ctx , * , arg = None) :
        self.start() if arg != "stop" else self.stop()


def setup(bot) : bot.add_cog(Loops(bot))