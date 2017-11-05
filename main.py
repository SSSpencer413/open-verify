import requests
import asyncio #await asyncio.sleep(seconds)
import discord
from discord.ext import commands

"""
[BOT NAME] : Open-Verify
[DATA STORED IN] : JSON file for now
[DISCORD.PY] : Rewrite
"""

invite_link = "https://bit.ly/Open-Verify"

bot_prefix = "$"

client = commands.Bot(description="A bot. What do you expect this description to say?!?!",command_prefix=bot_prefix,game=discord.Game(name=f"{bot_prefix}verify [ROBLOXNAME]"))

join_message = f"Thanks for inviting me to your discord server! Here are a few things you may want to know.\n\n**Verification**\nFor users to get verified they must do {bot_prefix}verify ROBLOXNAME. Bot will guide them through the rest.\nYou can set the verification role by doing {bot_prefix}setrole ROLENAME."

@client.event
async def on_ready():
	print('Connected.')
	print('Name : {}'.format(client.user.name))
	print('ID : {}'.format(client.user.id))
	print('Prefix : {}'.format(bot_prefix))
	print(discord.__version__)
  
@client.event
async def on_message(message):
    if not message.guild is None:
        #await client.process_commands(message)
        pass
    else:
        await message.author.send(f"I only work in servers! To invite me, use {invite_link}") #damn thats smart
        return
    if message.content.startswith(f"{client.user.mention} invite") or message.content.startswith(f"{bot_prefix}invite"):
        await message.channel.send("Can't wait to join your discord!\n\n**LINK**\n"+invite_link)
				
@client.event
async def on_guild_join(guild):
  for channel in guild.channels:
    try:
      await channel.send(join_message)
      return
    except:
      continue
  
 
