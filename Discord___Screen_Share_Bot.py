import discord
import asyncio
import shlex
import dbl
import signal

Token = "NjE0NDcxNTY3NzQ5MDIxNzI3.XV_9Rg.ozq08IVJNDt8zbzxojMDtST3dXw"

#TESTBOT
#Token = "NjE1NjIwMTYxMDA0ODk2MzA2.XWQq9w.p-xGYYyV7SARUBeRERtaiqlLhcU"
client = discord.Client()
DBO = None
Presence = None

@client.event
async def on_message(message):
    author = message.author

    bot_ad = "\n\n[Get Screen Share Bot for your discord](https://discordapp.com/oauth2/authorize?client_id=614471567749021727&scope=bot&permissions=3072)"

    if author == client.user:
        return

    try:
        input = shlex.split(message.content)
    except:
        input = message.content.split()
        pass
    if message.channel.type == discord.ChannelType.private:
        async with message.channel.typing():
            embed=discord.Embed(title="Hi, seems like you need some help. Here are my commands :)", description="", color=0xffff00)
            embed.add_field(name="!screenshare <ChannelName>", value="Outputs the link for the correspondant channel", inline=False)
            embed.add_field(name="!screenshare <ChannelID>", value="Outputs the link for the correspondant channel", inline=False)
            embed.add_field(name="!screenshare <ChannelID> <OutputChannel>", value="Outputs the link for the correspondant channel nicely into the OutputChannel\nDoes only work if you upvoted [HERE](https://discordbots.org/bot/614471567749021727)", inline=False)

            await message.channel.send(embed=embed)
            await message.channel.send(await DBO.get_vote(message.author.id))
    elif len(message.content.lower().split()) >= 1:
        if message.content.lower().split()[0] == "!screenshare":
            if message.author.guild_permissions.administrator:
                async with message.channel.typing():
                    if len(input) == 1:
                        embed=discord.Embed(title="Hi, sadly I don't know what you mean by that command :C TRY: ", description="", color=0xffff00)
                        embed.add_field(name="!screenshare <ChannelName>", value="Outputs the link for the correspondant channel", inline=False)
                        embed.add_field(name="!screenshare <ChannelID>", value="Outputs the link for the correspondant channel", inline=False)
                        embed.add_field(name="!screenshare <ChannelID> <OutputChannel>", value="Outputs the link for the correspondant channel nicely into the OutputChannel\nDoes only work if you upvoted [HERE](https://discordbots.org/bot/614471567749021727)", inline=False)
                        await message.channel.send(embed=embed)

                        embed=discord.Embed(title="You can even make the bot post the link stylishly to a channel", description="", color=0xff0000)
                        embed.add_field(name="!screenshare <ChannelID OR ChannelName> ChannelID", value="Outputs the link in the specified Channel"+bot_ad, inline=False)
                        await message.channel.send(embed=embed)
                    else:
                        if input[1].isdigit():
                            link = "https://discordapp.com/channels/" + str(message.guild.id) + "/" + input[1]
                        else:
                            ChannelID = discord.utils.get(message.guild.voice_channels, name=input[1])
                            try:
                                link = "https://discordapp.com/channels/" + str(message.guild.id) + "/" + str(ChannelID.id)
                            except AttributeError as e:
                                if str(e) == "'NoneType' object has no attribute 'id'":
                                    embed=discord.Embed(title='Hi, sadly the voice-channel specified was not found.", description="If you have spaced in your channel name, try surrounding it with ``"``', color=0xff0000)
                                    await message.channel.send(embed = embed)

                        if len(input) == 2:
                            embed=discord.Embed(title="", description="", color=0xffff00)
                            try:
                                embed.add_field(name="Have fun with your link :)", value="["+link+"]"+"("+link+")"+bot_ad, inline=False)
                            except UnboundLocalError as e:
                                if str(e) == "local variable 'link' referenced before assignment":
                                    pass
                            else:
                                await message.channel.send(embed=embed)
                        else:
                            if (await DBO.get_vote(int(message.author.id))) == False:
                                embed=discord.Embed(title="Hi, sadly it seems like you haven't voted for our bot", description="Change that by voting [Here](https://discordbots.org/bot/614471567749021727) and get nice features like this one", color=0xff0000)
                                await message.channel.send(embed=embed)
                            else:
                                embed=discord.Embed(title="", description="", color=0xffff00)
                                try:
                                    embed.add_field(name="Screenshare: ", value="[CLICK HERE]"+"("+link+")"+bot_ad, inline=False)
                                except UnboundLocalError as e:
                                    if str(e) == "local variable 'link' referenced before assignment":
                                        pass
                                else:
                                    if input[1].isdigit():
                                        if message.guild.id == client.get_channel(int(input[2])).guild.id:
                                            channel = client.get_channel(int(input[2]))
                                            await channel.send(embed=embed)
                                        else:
                                            embed=discord.Embed(title="The specified channel does not belong to your discord.", description=""+bot_ad, color=0xff0000)
                                            await message.channel.send(embed=embed)
                                    else:
                                        ChannelID = discord.utils.get(message.guild.text_channels, name=input[2])
                                        if message.guild.id == ChannelID.guild.id:
                                            await ChannelID.send(embed=embed)
                                        else:
                                            embed=discord.Embed(title="The specified channel does not belong to your discord.", description=""+bot_ad, color=0xff0000)
                                            await message.channel.send(embed=embed)               

class DiscordBotsOrgAPI:
    def __init__(self, client):
        self.client = client
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxNDQ3MTU2Nzc0OTAyMTcyNyIsImJvdCI6dHJ1ZSwiaWF0IjoxNTY2ODUxMTY1fQ.DnQLfx6dqZjvnGs5D9WzyzCj2PFdqUyoEUQQxGkVRUg'
        self.dblpy = dbl.DBLClient(client, self.token)
        self.loop = self.client.loop.create_task(self.update_stats())

    def stop(self):
        self.loop.cancel()

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        while not self.client.is_closed():
            print('Attempting to post server count')
            try:
                await self.dblpy.post_guild_count()
                print('Posted server count ({})'.format(self.dblpy.guild_count()))
            except Exception as e:
                print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(10)

    async def get_vote(self, userid):
        return await self.dblpy.get_user_vote(int(userid))

class PresenceLoop():
    def __init__(self, client):
        self.client = client
        self.bg_task = client.loop.create_task(self.my_background_task())

    def stop(self):
        self.bg_task.cancel()

    async def my_background_task(self):
        await self.client.wait_until_ready()
        wait_time = 10
        while not self.client.is_closed():
            await self.client.change_presence(status=discord.Status.dnd, afk=False, activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(client.guilds))+" Guilds"))
            print("[PRESENCE] Changed to Guilds")
            await asyncio.sleep(wait_time)
            await self.client.change_presence(status=discord.Status.dnd, afk=False, activity=discord.Activity(type=discord.ActivityType.listening, name="!screenshare"))
            print("[PRESENCE] Changed to Command")
            await asyncio.sleep(wait_time)

@client.event
async def on_ready():
    msg = 'Logged in as ' + client.user.name + ":" + str(client.user.id)
    print(msg)
    print('-' * len(msg))
    global DBO
    DBO = DiscordBotsOrgAPI(client)
    global Presence
    Presence = PresenceLoop(client)

def sigint_handler(signum, frame):
    DBO.stop()
    Presence.stop()
    exit (0);
 
signal.signal(signal.SIGINT, sigint_handler)

client.run(Token)
"""
try:
    client.run(Token)
except RuntimeError as e:
    if str(e) == "Event loop stopped before Future completed.":
        DBO.stop()
        Presence.stop()
    else:
        raise e
"""