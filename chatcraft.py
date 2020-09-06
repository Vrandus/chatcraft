import discord
import io
import os
import threading
import time
import asyncio


client = discord.Client()

keywords_death = {"shot", "pummeled", "death", "escape", 
    "drowned", "up", "killed", "hit", "fell", "squashed",
    "flames", "walked", "fighting", "went", "swim", "lightning",
     "lava", "slain", "fireballed", "suffocated", "squished",
      "impaled", "live", "withered", "died"}

def between_listener(loop, channel):
    # loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(chat_listener(channel))
    loop.close()
async def chat_listener(channel):
    path = "../logs/latest.log"
    log_file = open(path, "r")
    while 1:
        if len(log_file.readline()) < 4 :
            break
    UUID = {}
    print("file opened")
    print(channel.id)
    minecraft_channel = client.get_channel(channel.id)
    while 1:
        str = log_file.readline()
        # print(str)
        if "*:25565" in str:
            print("server restart")
            embedded = discord.Embed(title="Server is Up!", colour=discord.Colour.green(), type="rich")
            await send_message(minecraft_channel, embedded, True)
        if "UUID of player" in str:
            split_str = str.split()
            UUID[split_str[7]] = split_str[9]
            # UUID[str[str.index("player")+7]] = str[str.index(" is ")+4:-1]
        
        if "joined" in str or "left" in str:
            # print("joined" in str or "left" in str)
            split_str = str.split()

            if "joined" in str:
                embedded = discord.Embed(title=str[33:], colour=discord.Colour.green(), type="rich")
            else:
                embedded = discord.Embed(title=str[33:], colour=discord.Colour.red(), type="rich")
            
            try:
                url = f'https://crafatar.com/avatars/{UUID[split_str[3]]}?size=32'
                print(url)
                embedded.set_thumbnail(url=url)
            except:
                await send_message(minecraft_channel, embedded, True)
                continue
            # print("DEBUG: in joined or left UUID: " + cached_UUID)
        if "[Server]" not in str:
            if "<" and ">" in str:
                str = str[33:]

                await send_message(minecraft_channel, str, False)
                print(str)
            else:
                split_str = str.split()
                check_death = set(split_str)
                if len(check_death & keywords_death) >= 1:
                    embedded = discord.Embed(title=str[33:], colour=discord.Colour.default(), type="rich")
                    try:
                        url = f'https://crafatar.com/avatars/{UUID[split_str[3]]}?size=32'
                        embedded.set_thumbnail(url=url)
                    except:
                        await send_message(minecraft_channel, embedded, True)
                        continue

        try:
            await client.wait_for('message', timeout=0.1)
        except:
            continue 
    log_file.close()

async def send_message(channel, message, embedded):
    if embedded == True:
        await channel.send(embed=message)
    else:    
        await channel.send(message)

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    perm_channel = discord.TextChannel
    print(channel_name)
    await client.change_presence(activity=discord.Game(name=ip))
    for channel in client.get_all_channels():
        if channel.name == channel_name:
            perm_channel = channel

    loop = client.loop
    x = threading.Thread(target=between_listener, args=(loop, perm_channel,),  daemon=True)
    x.start()
    
    

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name != channel_name:
        return
    
    command = f'screen -S mcserver -p 0 -X stuff "say <{message.author}> {message.content} ^M"'

    os.system(command)


token = ""
channel_name = ""
ip = ""
with open('bot.properties', 'r') as file:
    channel_name = file.readline()
    channel_name = channel_name[channel_name.index("=")+1: -1]
    print(channel_name)

    token = file.readline()
    token = token[token.index("=")+1:]
    ip = file.readline()
    ip = ip[ip.index("=")+1:]
    print(token)

    file.close()

client.run(token)

