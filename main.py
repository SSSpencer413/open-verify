import json
import requests
import asyncio #await asyncio.sleep(seconds)
import discord
import random
from discord.ext import commands

invite_link = "https://bit.ly/Open-Verify"

randomwords = ['curious','suppose','berry','infamous','panoramic','grandmother','cake','title','poison','childlike','ancient','mine','bushes','yummy','ring','discreet','borrow','far','sour','letters','ground','pathetic','pie','deer','kindhearted','rampant','beneficial','tricky','acid','blot','spray','camera','scare','drag','periodic','sedate','arrogant','business','stingy','plastic','camp','rabbit','brawny','bedroom','melodic','mean','sloppy','old','ruthless','gate','cemetery','satisfying','fade','knowledgeable','possible','truthful','aware','cause','guttural','wool','frogs','relation','lush','nonstop','scent','grab','dysfunctional','zebra','attend','embarrass','axiomatic','attractive','tire','third','moor','soft','coat','moldy','crown','incandescent','brick','watch','sad','important','grape','sin','talented','live','applaud','thankful','skinny','imminent','unpack','dependent','horn','soggy','supreme','minute','ask','ghost','defeated','coherent','coast','literate','boast','hammer','curved','government','fearful','memorise','shape','furniture','baseball','innocent','bury','travel','tested','sweltering','release','actor','rub','steady','elfin','trade','bed','fix','motion','aspiring','fine','entertaining','stocking','bewildered','sneaky','profit','employ','suit','communicate','weak','side','spark','small','doubt','needle','prickly','harmonious','dusty','damage','flippant','impolite','tumble','part','bounce','word','wide','unwritten','land','pushy','spoil','uptight','dock','flower','fire','fang','private','red','last','orange','throat','battle','nebulous','skate','consider','grade','cherries','annoy','instrument','reproduce','cooperative','suit','aback','snatch','rate','serve','striped','beef','slope','jellyfish','potato','amuse','ship','busy','visit','mindless','spotted','dress','sack','memory','spotty','cheat','stop','drunk','crayon','whine','female','love','shaggy','return','panicky','cooing','zippy','narrow','punch','alive','nappy','surprise','pat','nervous','protest','energetic','rotten','crazy','haircut','slimy','bag','gleaming','utopian','tick','signal','intelligent','language','honorable','teeth','stop','debonair','slow','yak','swing','key','diligent','afterthought','awesome','breakable','hole','puny','changeable','little','disarm','aromatic','join','calculating','guard','horses','certain','learned','respect','cellar','star','brush','coal','relax','fairies','woozy','hungry','beautiful','grass','substance','oven','ink','plot','outstanding','deafening','petite','obeisant','week','start','murder','ski','racial','belief','spiky','trashy','beam','lick','bent','wild','offend','magic','payment','irritating','creepy','injure','lock','tame','incompetent','fantastic','waiting','story','hellish','four','cluttered']

bot_prefix = "$"

client = commands.Bot(description="A bot. What do you expect this description to say?!?!",command_prefix=bot_prefix,game=discord.Game(name=f"{bot_prefix}verify [ROBLOXNAME]"))

join_message = f"Thanks for inviting me to your discord server! Here are a few things you may want to know.\n\n**Verification**\nFor users to get verified they must do {bot_prefix}verify ROBLOXNAME. Bot will guide them through the rest.\nYou can set the verification role by doing {bot_prefix}setrole ROLENAME."

with open('save.json') as json_data:
	load_json = json.load(json_data)
	client.verify = load_json["verify"]
	client.verifyinfo = load_json["info"]
	client.verifypending = load_json["pending"]
	client.verifyrole = load_json["role"]

@client.event
async def on_ready():
	print('Connected.')
	print('Name : {}'.format(client.user.name))
	print('ID : {}'.format(client.user.id))
	print('Prefix : {}'.format(bot_prefix))
	print(discord.__version__)
	
	
def save():
	with open("save.json", "w") as outf:
		json.dump({'verify' : client.verify, 'info' : client.verifyinfo, 'pending' : client.verifypending, 'role' : client.verifyrole}, outf, indent=4)

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
async def finish(ctx):
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
		if not client.verifypending[idd][0] in contentdecode:
			await ctx.message.channel.send("Oh dear, I can't seem to find the words.")
			return
		client.verify[ctx.author.id] = client.verifypending[idd][1]
		await ctx.message.channel.send("Great! You are now verified as " + client.verify[ctx.author.id] + ".")
	joindate = re.search('<p class=text-lead>(\d+\/\d+\/\d+)<li class=p', contentdecode).group(1)
	placevisits = re.search('<p class=text-lead>([0-9,]+)<li class=profile-stat><p cl', contentdecode).group(1)
	forumposts = re.search('<p class=text-lead>([0-9,]+)<\/li><\/li><\/ul>', contentdecode).group(1)
	client.verifyinfo[ctx.author.id] = [id, joindate, placevisits, forumposts]
	client.verifypending.pop[idd] = None
	save()
	if ctx.author.guild.id in client.verifyrole:
		await member.addrole(client.verifyrole[ctx.author.guild.id], reason="Verified")

@client.command(description="What's that discord member's ROBLOX account?")
async def whois(self, ctx, member: discord.Member):
	if not member.id in client.verify:
		ctx.message.channel.send("Not verified!")
		return
	embed=discord.Embed(title=" ")
	embed.set_author(name="Who is " + member.name + "?")
	embed.set_thumbnail(url='https://www.roblox.com/bust-thumbnail/image?userId={}&width=420&height=420&format=png'.format(client.verifyinfo[member.id][0]))
	embed.add_field(name="Name", value=client.verify[member.id], inline=True)
	embed.add_field(name="ROBLOX ID", value=client.verifyinfo[member.id][0], inline=True)
	embed.add_field(name="Join Date", value=client.verifyinfo[member.id][1], inline=True)
	embed.add_field(name="Place Visits", value=client.verifyinfo[member.id][2], inline=True)
	embed.add_field(name="Forum Posts", value=client.verifyinfo[member.id][3], inline=True)
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

client.run("Mzc2NzgwMzQ5OTE0NjExNzEy.DODXjw.2dPUDBLCYZ9jzrQHsjsGmn_BfGU")
