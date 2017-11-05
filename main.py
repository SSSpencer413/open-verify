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

@client.command()
async def verify(ctx, username: str):
	if ctx.message.author.id in client.verify:
		ctx.message.channel.send("Already verified as: `{}`".format(client.verify[ctx.message.author.id]))
		return
	exist = requests.get("https://www.roblox.com/UserCheck/DoesUsernameExist?username=" + username)
	exist = exist.json()
	exist = exist["success"]
	if exist == False:
		ctx.message.channel.send("User doesn't exist.")
		return
	words = random.choice(randomwords) + "-" + random.choice(randomwords) + "-" + random.choice(randomwords)
	await ctx.message.channel.send(f"Your words are: `{words}`, put them in your roblox description/motd. say {bot_prefix}finish when you're finished.")
	client.verifypending[ctx.message.author.id] = [words, username]
	save()

@client.command()
async def finish(ctx)
	idd = ctx.message.author.id
	if not idd in client.verifypending:
		await ctx.message.channel.send(f"Type {bot_prefix}verify to get started!")
		return
	id = requests.get("https://api.roblox.com/users/get-by-username?username=" + client.verifypending[idd][1])
	id = id.json()
	id = id["Id"]
	rodescription = requests.get("https://www.roblox.com/users/" + str(id) + "/profile")
	contentdecode = rodescription.content.decode('utf-8')
	async with ctx.message.channel.typing():
		if not .client.verifypending[idd][0] in contentdecode:
			await ctx.message.channel.send("Oh dear, I can't seem to find the words.")
			return
		client.verify[ctx.author.id] = client.verifypending[idd][1]
		await ctx.message.channel.send("Great! You are now verified as " + client.verify[ctx.author.id] + ".")
	joindate = re.search('<p class=text-lead>(\d+\/\d+\/\d+)<li class=p', contentdecode).group(1)
	placevisits = re.search('<p class=text-lead>([0-9,]+)<li class=profile-stat><p cl', contentdecode).group(1)
	forumposts = re.search('<p class=text-lead>([0-9,]+)<\/li><\/li><\/ul>', contentdecode).group(1)
	client.verifyinfo[ctx.author.id] = [id, joindate, placevisits, forumposts]
	client.verifypending.pop(idd, None)
	save()
	if ctx.author.guild.id in client.verifyrole:
		await member.addrole(client.verifyrole[ctx.author.guild.id], reason="Verified")

@client.command(description="What's that discord member's ROBLOX account?")
async def whois(self, ctx, member: discord.Member):
	if not member.id in self.client.verify:
		ctx.message.channel.send("Not verified!")
		return
	embed=discord.Embed(title=" ")
	embed.set_author(name="Who is " + member.name + "?")
	embed.set_thumbnail(url='https://www.roblox.com/bust-thumbnail/image?userId={}&width=420&height=420&format=png'.format(self.client.verifyinfo[member.id][0]))
	embed.add_field(name="Name", value=self.client.verify[member.id], inline=True)
	embed.add_field(name="ROBLOX ID", value=self.client.verifyinfo[member.id][0], inline=True)
	embed.add_field(name="Join Date", value=self.client.verifyinfo[member.id][1], inline=True)
	embed.add_field(name="Place Visits", value=self.client.verifyinfo[member.id][2], inline=True)
	embed.add_field(name="Forum Posts", value=self.client.verifyinfo[member.id][3], inline=True)
	await ctx.message.channel.send(embed=embed)
		
@client.event
async def on_message(message):
		if not message.guild is None:
				if message.content.startswith(f"{client.user.mention} invite") or message.content.startswith(f"{bot_prefix}invite"):
					await message.channel.send("Can't wait to join your discord!\n\n**LINK**\n"+invite_link)
				await client.process_commands(message)
		else:
				await message.author.send(f"I only work in servers! To invite me, use {invite_link}") #damn thats smart
				return


@client.event
async def on_guild_join(guild):
	for channel in guild.channels:
		try:
			await channel.send(join_message)
			return
		except:
			continue


