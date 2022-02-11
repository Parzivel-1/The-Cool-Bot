import discord , json , asyncio
from discord.ext import commands as cmds



class Ignore(cmds.Cog , name = "ignore" , description = "Ignore") :
    def __init__(self , bot) : self.bot = bot


    fish_check = lambda ctx : ctx.guild.id in (607780933092769812 , 841292233276915712) or ctx.author.id == 643853842441830400


    @cmds.command()
    @cmds.is_owner()
    async def emotes(self , ctx) :
        await ctx.message.delete()
        r_m = await ctx.guild.fetch_emoji(860304177867259934)
        r_l = await ctx.guild.fetch_emoji(860304500653162516)
        r_v = await ctx.guild.fetch_emoji(870051215541698600)
        msg = discord.Embed(title = "React here to get your roles:" , description  = f"**{r_m} >> <@&841559631775268864>**\n\n**{r_l} >> <@&860302761497198652>**\n\n**{r_v} >> <@&860859599165849651>**" , color = 0x00ff00)
        msg.set_thumbnail(url = ctx.guild.icon_url)
        msg = await ctx.send(embed = msg)
        await msg.add_reaction(r_m)
        await msg.add_reaction(r_l)
        await msg.add_reaction(r_v)


    @cmds.command()
    @cmds.is_owner()
    async def run(self , ctx) :
        await ctx.send(content = "hello" , components = discord.Button(data = 123))


    @cmds.command()
    @cmds.is_owner()
    async def stop(self , ctx) :
        await ctx.message.delete()
        with open(r"D:\Users\Yair\Documents\Yair's_things\Python\The_Cool_Bot\data.json" , "w") as f : json.dump(self.bot.data , f , indent = 4)
        await self.bot.logout()
        print("\nQuit\n")


    @cmds.command()
    @cmds.is_owner()
    async def sheeesh(self , ctx) :
        await ctx.message.delete()
        vc = await ctx.author.voice.channel.connect()
        vc.play(source = discord.FFmpegPCMAudio(source = r"D:\Users\Yair\Documents\Yair's_things\Python\The_Cool_Bot\Current_Version\sheeesh.mp3"))
        while vc.is_playing() : pass
        await vc.disconnect()


    @cmds.command()
    @cmds.check(fish_check)
    async def fish(self , ctx , times  = "1") :
        if not times.isdigit() : return await self.bot.send(ctx , "You didn't provide a number of times!" , 0xff7f00)
        times = int(times)
        if times < 0 : return await self.bot.send(ctx , "Provide a positive number of times!" , 0xff7f00)
        vc = await ctx.author.voice.channel.connect()
        always = False
        if not times : always = True
        audio = discord.FFmpegPCMAudio(source = r"D:\Users\Yair\Documents\Yair's_things\Python\The_Cool_Bot\Current_Version\fish.mp3")
        while times or always :
            if not always : times -= 1
            vc.play(source = audio)
            while vc.is_playing() : await asyncio.sleep(1)
        await vc.disconnect()


    @cmds.command()
    @cmds.is_owner()
    async def idk(self , ctx , user_id : int = None) :
        user = await self.bot.fetch_user(user_id)
        if user.avatar : await ctx.send(user.avatar)
        if user.banner : await ctx.send(user.banner)
        date = user.created_at.strftime(r"%d/%m/%Y, %H:%M")
        await ctx.send(f"User >>> {user.mention} `{user}`")
        await ctx.send(f"Created At >>> `{date}`")
        await ctx.send(f"ID >>> {user.id}")
        guilds = "\n**---------------**\n".join(f"`{guild.name}`\n{guild.id}" for guild in user.mutual_guilds)
        if guilds : await ctx.send(f"Mutual Guilds:\n{guilds}")


    @cmds.command()
    @cmds.is_owner()
    async def find(self , ctx , username = None) :
        name , discriminator = username.split("#")
        user = discord.utils.get(self.bot.get_all_members() , name = name , discriminator = discriminator)
        await self.idk(ctx , user.id)


    @cmds.command()
    @cmds.is_owner()
    async def fail(self , ctx , msg_id : int = None) :
        msg = await ctx.author.fetch_message(msg_id)
        await msg.delete()


    @cmds.command()
    @cmds.is_owner()
    async def rules(self , ctx) :
        await ctx.message.delete()
        msg = discord.Embed(title = "RULES:" , description = """**
        1) Follow Discord ToS and guildelines: https://discord.com/terms, https://discordapp.com/guidelines.\n
        2) No earape, voice changers, very loud noises, swears, spams, promotions or annoying of any kind in all channels.\n
        3) Keep content in English and in the matching channels.\n
        4) No NSFW profile pictures or any kind of content in all channels.\n
        5) No NSFW content of any kind in all voice channels and text channels.\n
        6) Every channel is public, in exception for private channels.\n
        7) No self promotion in DM or in the server of any kind.\n
        8) Respect everyone, no hate speech of any kind.\n
        11) No griefing or trolling of any kind.\n
        12) Expect a punishment of some kind for breaking any of these rules.
        **""" , color = 0xff7f00)
        # 9) For any case of violating the rules or a suggestion for the server you can contact the staff by sending a DM to <@!575252669443211264> and choosing this server.\n
        # 10) No spam or vague use of <@!575252669443211264>.\n
        msg = await ctx.send(embed = msg)
        await msg.add_reaction("✅")


    @cmds.command()
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.is_owner()
    async def nickname(self , ctx , * , nickname = None) :
        await ctx.message.delete()
        nickname = nickname or f"[ {ctx.prefix} ] The Cool Bot"
        await ctx.me.edit(nick = nickname)
        await ctx.author.send(f"Changed nickname to\n```{nickname}```\nGuild >>> {ctx.guild.name} ({ctx.guild.id})")


    @cmds.command()
    @cmds.cooldown(rate = 3 , per = 1)
    @cmds.is_owner()
    async def reload(self , ctx , cog_name = None) :
        self.bot.reload_extension(name = cog_name)
        await ctx.send(f"Reloaded cog:\n```{cog_name}```")



def setup(bot) : bot.add_cog(Ignore(bot))