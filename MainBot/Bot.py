import json
# noinspection PyUnresolvedReferences
from DocGet.Bot import run
import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True


def get_info(data, file):
	f = open(file)
	info = f.read()
	f.close()
	bot_info = json.loads(info)
	return bot_info[data]


# Setup variables
bot_info_file = "BotInfo.json"

token = get_info("Token", bot_info_file)
guild_id = get_info("guild_id", bot_info_file)
RulesChannel = get_info("RulesChannel", bot_info_file)
ReactMSGID = get_info("ReactMSGID", bot_info_file)
bot_user_id = get_info("bot_user_id", bot_info_file)
unVerifiedRole = get_info("unVerifiedRole", bot_info_file)
VerifiedRole = get_info("VerifiedRole", bot_info_file)
tryout_channel = get_info("tryout_channel", bot_info_file)
InfoChannel = get_info("InfoChannel", bot_info_file)
applyChannel = get_info("applyChannel", bot_info_file)
welcomeChannel = get_info("welcomeChannel", bot_info_file)
ApplicationCategory = get_info("ApplicationCategory", bot_info_file)
supportChannel = get_info("supportChannel", bot_info_file)
botCommands = get_info("botCommands", bot_info_file)
botCommandsKeep = get_info("botCommandsKeep", bot_info_file)
AdminRoles = get_info("AdminRoles", bot_info_file)
getReactions = get_info("reactionGetChannel", bot_info_file)
#with open("BotInfo.json") as f:
#	react_roles = json.loads(f.read())
#	react_roles = react_roles["reactionData"]["Roles"]


client = commands.Bot(command_prefix='.', intents=intents)


def gen_embed_dcr(prefix, suffix, rules, desc="The Discord Server Rules.", title="  ", value="‎", color=0x5c2494):
	rules = rules.splitlines()
	embed = discord.Embed(title=title, description=desc, color=color)

	for x in rules:
		if str(rules).endswith(suffix):
			send = prefix + x
		else:
			send = prefix + x + suffix

		embed.add_field(name=send, value=value, inline=False)

	return embed


@client.event
async def on_ready():
	print("Startup")
	# Setup #rules channel
	tog = False
	a = False
	announce = False
	if announce:
		embed = discord.Embed(title="React", description="React with \"❗\" to be added to the announcements list.")
		channel = client.get_channel(getReactions)
		msg = await channel.send(embed=embed)
		reaction = "❗"
		await msg.add_reaction(reaction)


	if a:
		embed = discord.Embed(title="Apply", description="Apply to the clan, in this text-box please enter some background information about your skills.")
		channel = client.get_channel(applyChannel)
		await channel.send(embed=embed)

	if tog:
		Prefix, Suffix, Rules, Info = run()
		embed = gen_embed_dcr(Prefix, Suffix, Rules)
		channel = client.get_channel(RulesChannel)
		messages = await channel.history(limit=2000).flatten()
		for message in messages:
			msg_id = message.id
			msg = await channel.fetch_message(msg_id)
			await msg.delete()
		await channel.send(embed=embed)

		t = True

		if t:
			new_channel = client.get_channel(781442646358229002)
			new_embed = gen_embed_dcr("", "!", "React to this message to verify", "Read Rules Before Verification.")
			msg = await new_channel.send(embed=new_embed)
			reaction = '✅'
			await msg.add_reaction(reaction)
		# Finished on_ready function


@client.command()
async def announce(ctx, *, args):
	member_roles = []
	isAdmin = False
	for role in ctx.author.roles:
		member_roles += [role]
		if str(role) in AdminRoles:
			isAdmin = True

	if isAdmin:
		embed = discord.Embed(title="Announcement", description=args + f"\n\nPlease react with \"❗\" to get pings for announcements you can always stop getting pinged by typing \".announcementsoff\" in #bot-commands!")
		channel = client.get_channel(getReactions)
		Annrole = discord.utils.get(ctx.guild.roles, name="Announcements")
		msg = await channel.send(Annrole.mention, embed=embed)
		reaction = "❗"
		await msg.add_reaction(reaction)

@client.command()
async def announcementsoff(ctx):
	Annrole = discord.utils.get(ctx.guild.roles, name="Announcements")
	await ctx.author.remove_roles(Annrole)


@client.event
async def on_member_join(member):
	channel = client.get_channel(welcomeChannel)
	await channel.send("Welcome, " + member.mention)
	role = discord.utils.get(member.guild.roles, name=unVerifiedRole)
	await member.add_roles(role)


@client.event
async def on_raw_reaction_add(payload):
	emoji = payload.emoji
	new_member = payload.member
	channel_id = payload.channel_id
	react_roles = ["❗"]
	if channel_id == getReactions:
		for role in react_roles:
			with open("BotInfo.json") as f:
				new_role = role
			if str(emoji) == new_role:
				role = discord.utils.get(new_member.guild.roles, name="Announcements")

				await new_member.add_roles(role)



	if payload.user_id != bot_user_id:
		message_id = payload.message_id
		if message_id == ReactMSGID:
			guild_id2 = payload.guild_id
			guild = discord.utils.find(lambda g: g.id == guild_id2, client.guilds)
			role = discord.utils.get(guild.roles, name=VerifiedRole)
			remove_role = discord.utils.get(guild.roles, name=unVerifiedRole)
			if role is None:
				print("Role Not Found")
				return 1
			member = payload.member
			if member is None:
				print("Member not found")
				return 1
			await member.add_roles(role)
			await member.remove_roles(remove_role)
	else:
		pass





@client.event
async def on_message(message):


	channel = message.channel.id
	content = message.content
	author = message.author.id
	if author != 781421122699788299:
		write_to_file = f"channel = {channel}, content = {content}, author = {author} \n"
		f = open("LOGS.txt", 'a')
		f.write(write_to_file)
		f.close()

	questions = []
	# DELETE MESSAGES
	messageSkipper = 0
	if channel == botCommands:
		channel2 = client.get_channel(botCommands)
		messages = await channel2.history(limit=2000).flatten()
		get_info("botCommandsKeep", "BotInfo.json")
		for message in messages:
			if messageSkipper >= botCommandsKeep:
				msg_id = message.id
				msg = await channel2.fetch_message(msg_id)
				try:
					await msg.delete()
				except discord.errors.NotFound:
					pass
			else:
				messageSkipper += 1

	if channel == applyChannel and author != bot_user_id:
		channel2 = client.get_channel(applyChannel)
		messages = await channel2.history(limit=2000).flatten()
		for message in messages:
			msg_id = message.id
			msg = await channel2.fetch_message(msg_id)
			try:
				await msg.delete()
			except discord.errors.NotFound:
				pass
		embed = discord.Embed(title="Apply", description="To apply to the clan, in this text-box please enter some background information about your skills.")
		await channel2.send(embed=embed)

	with open("../MainBot/ApplyQuestions.txt") as f:
		for question in f.readlines():
			questions = questions + [question.strip("\n")]
	if author == bot_user_id:
		return 0
	ticket_list = []
	with open("../Tickets/Tickets.txt") as f:
		for line in f.readlines():
			line = line.strip("\n")
			ticket_list = ticket_list + [line]
	for ticket in ticket_list:
		if ticket == "":
			pass
		else:
			ticketN = ticket.split(" = ")
			ticketS = ticket.split(" = ")
			ticketS = ticketS[0]
			ticketN = ticketN[1]

			ticket_loaded = json.loads(ticketN)
			ticket_id = ticket_loaded["ID"]
			if ticket_id == str(channel):
				currentQuestion = ticket_loaded["CurrentQuestion"]
				currentQuestion = int(currentQuestion)
				currentQuestion += 1
				f = open("../Tickets/Tickets.txt")
				oldFile = f.readlines()
				for line in oldFile:
					if line == "\n":
						pass
				else:
					pass
				f.close()
				f = open("../Tickets/Tickets.txt", 'w')

				oldFile3 = []
				for x in oldFile:
					if str(x).strip("\n") == ticket.strip("\n"):
						pass
					elif x == '':
						pass
					else:
						oldFile3 = oldFile3 + [x]
				addOld = ""
				addOld = addOld.join(oldFile3)
				write = addOld + "\n" + f"{str(ticketS)} = " + "{\"ID\": \"" + f"{str(ticket_id)}\", \"CurrentQuestion\": \"" + str(currentQuestion) + "\"" + "} \n"
				f.write(write)
				f.close()
				channel = client.get_channel(channel)
				try:
					await channel.send(questions[currentQuestion])
				except IndexError:
					pass

	contentTest = content.lower()
	member_roles = []
	isAdmin = False
	for role in message.author.roles:
		member_roles += [role]
		if str(role) in AdminRoles:
			isAdmin = True
	if contentTest == ".refreshrules" and isAdmin:
		Prefix, Suffix, Rules, Info = run()
		embed = gen_embed_dcr(Prefix, Suffix, Rules)
		channel = client.get_channel(RulesChannel)
		messages = await channel.history(limit=2000).flatten()
		for message in messages:
			msg_id = message.id
			msg = await channel.fetch_message(msg_id)
			await msg.delete()
		await channel.send(embed=embed)

	elif contentTest == ".refreshinfo" and isAdmin:
		Prefix, Suffix, Rules, Info = run()
		embed = gen_embed_dcr(Prefix, Suffix, Info, "The Discord Server Info.")
		channel = client.get_channel(InfoChannel)
		messages = await channel.history(limit=2000).flatten()
		for message in messages:
			msg_id = message.id
			msg = await channel.fetch_message(msg_id)
			await msg.delete()
		await channel.send(embed=embed)

	elif contentTest == ".deltickets" and isAdmin:
		category = client.get_channel(ApplicationCategory)

		for channel in category.text_channels:
			await channel.delete()
		f = open("TicketNum.txt", 'w')
		f.close()
		f = open("../Tickets/Tickets.txt", 'w')
		f.close()

	if channel == tryout_channel and str(author) != "★★ 𝟗𝟗𝟗 ★★#2622":
		f = open("TicketNum.txt")
		num = f.read()
		f.close()
		try:
			num = int(num)
		except ValueError:
			num = 1
		num += 1
		f = open("TicketNum.txt", 'w')
		f.write(str(num))
		f.close()
		guild = message.guild
		category = client.get_channel(ApplicationCategory)

		member_object = guild.get_member(author)
		TicketRole = discord.utils.get(message.guild.roles, name="Ticket Reviewer")
		AuthorPerm = member_object
		overwrites = {
			guild.default_role: discord.PermissionOverwrite(
				read_messages=False,
				send_messages=False,
			),
			TicketRole: discord.PermissionOverwrite(
				read_messages=True,
				send_messages=True,
			),
			AuthorPerm: discord.PermissionOverwrite(
				read_messages=True,
				send_messages=True,
			)
		}

		channel = await guild.create_text_channel(f'ticket-{num}', category=category, overwrites=overwrites)
		f = open("../Tickets/Tickets.txt", 'a')
		f.write(f"\n Ticket-{num} = " + "{\"ID\": \"" + f"{str(channel.id)}\", \"CurrentQuestion\": \"1\"" + "}")
		f.close()
		authorAt = f"<@{author}>"
		role = discord.utils.get(message.guild.roles, name="Ticket Reviewer")
		await channel.send(authorAt + ", " + role.mention + "\n " + content)
		await channel.send("**How many hours do you have?**")

	else:
		pass
	f.close()
	await client.process_commands(message)
client.run(token)
