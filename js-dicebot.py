# JS-Bot.py
import os
import random

import discord

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD:
			break

	print(
		f'{client.user} is connected to the following guild:\n'
		f'{guild.name}(id: {guild.id})'
	)



@client.event
async def on_message(message):

	def startroll():
		nonlocal RollDesc
		nonlocal numdice
		nonlocal op
		nonlocal i
		nonlocal total
		nonlocal n
		i = 1
		n = 0
		total=0
		RollDesc=''
		op='+'
		numdice = 0
		
		
	def takenumber(num):
		nonlocal RollDesc
		nonlocal numdice
		nonlocal op
		nonlocal total
		if numdice==0:
			numdice = num
		else:
			tot = 0
			m=0
			if RollDesc != '':
				RollDesc += op
			for m in range(0,numdice):
				r=random.randint(1,num)
				tot+=r
				RollDesc += '['+str(r)+']'
			
			if op == '+': total += tot
			elif op == '-': total -= tot
			numdice = 0
	
		
	if message.author == client.user:
		return
	i=0
	n=0
	total=0
	RollDesc=''
	op='+'
	numdice=0
	hashmssg='' 
	
	if message.content.startswith('!'):
		startroll()
		
		i=1
		if message.content[i] in 'xX':
			takenumber(1)
			takenumber(20)
		elif message.content[i] in 'hH':
			total = 0
			i = len(message.content);
				
		while i < len(message.content):
			
			if message.content[i] in '1234567890':
				n = (n * 10) + int(message.content[i])
			else:
				if (n>0) or (message.content[i] in 'dD'): 
					if n>0:
						takenumber(n)
					n=0
				if message.content[i] in '+-': 
					op = message.content[i]
				elif message.content[i] == '#':
					hashmssg=message.content[i:]
					i=len(message.content)
				
			i+=1
		if (n>0):
			takenumber(n)
		if numdice > 0:
			RollDesc += op + str(numdice)
			if op == '+': total += numdice
			elif op == '-': total -= numdice
								
		if total > 0:		
			response = RollDesc + ' = ' + str(total)+' '+hashmssg
		else:
			response = """To use, type '!' followed by the dice equation ie. (3d6) (1d20+8) (2d6+1d8)
			If the desired dice equation is 1d20+[n], you can use !Xn"""
		await message.channel.send(response)
    
	else:
		return

client.run(TOKEN)