# JS-Bot.py
import os
import random

import discord

#
#from dotenv import load_dotenv
#load_dotenv()

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

	def startRoll():
		nonlocal RollDesc
		nonlocal numDice
		nonlocal op
		nonlocal i
		nonlocal total
		nonlocal numExpected
		nonlocal dType
		nonlocal keepNum
		nonlocal rerollVal
		nonlocal keepRerolling
		i = 1
		n = 0
		total=0
		RollDesc=''
		op='+'
		numdice = 0
		numExpected='n'
		dType=0
		keepNum=0
		rerollVal=0
		keepRerolling=False
		
	def makeRoll():
		nonlocal RollDesc
		nonlocal numDice
		nonlocal dType
		nonlocal keepNum
		nonlocal rerollVal
		nonlocal keepRerolling
		nonlocal op
		nonlocal numExpected
		nonlocal total
		rerolled = False
		rolls = []
		r=0
		if dType<1:
			rolls.append(numDice)
			numDice=0
		while len(rolls) < numDice:
			r=random.randint(1,dType)
			if (r > rerollVal) or (rerolled and not keepRerolling):
				rolls.append(r)
				rerolled = False
			else:
				rerolled = True
		if keepNum>0:
			rolls.sort();
			while len(rolls)>keepNum:
				rolls.pop(0)
		if (len(rolls)>0) and not (RollDesc==''):
			RollDesc+=' '+op+' '
		while len(rolls)>0:
			if dType>0:
				RollDesc+='['+str(rolls[0])+']'
			else:
				RollDesc+=str(rolls[0])
			if op == '+': 
				total += rolls[0]
			elif op == '-': 
				total -= rolls[0]
			rolls.pop(0)
		numDice=0
		dType=0		
		keepNum=0
		rerollVal=0
		keepRolling=False
		numExpected='n'
				
	def takeNumber(num):
		nonlocal numDice
		nonlocal dType
		nonlocal keepNum
		nonlocal rerollVal
		nonlocal numExpected
		if numExpected in 'nN':
			numDice = num
		elif numExpected in 'dD':
			dType = num
		elif numExpected in 'rR':
			rerollVal = num
		elif numExpected in 'kK':
			keepNum = num
		numExpecte=' '
		
		
	if message.author == client.user:
		return
	i = 0
	n = 0
	total = 0
	hashmssg = '' 
	numDice = 0
	numExpected = 0
	keepNum = 0
	dType = 0;
	rerollVal = 0
	keepRerolling = False
	RollDesc=''
	
	if message.content.startswith('!'):
		startRoll()
		
		i=1
		if message.content[i] in 'xX':
			numExpected='n'
			takeNumber(1)
			numExpected='d'
			takeNumber(20)
			makeRoll()
		elif message.content[i] in 'hH':
			total = 0
			i = len(message.content);
				
		while i < len(message.content):
			
			if message.content[i] in '1234567890':
				n = (n * 10) + int(message.content[i])
			else:
				if n>0:
					takeNumber(n)
					n=0
				if message.content[i] in 'dDrRkK': 
					if (numExpected in 'rR') and (message.content[i] in 'rR'):
						keepRerolling = True
					numExpected = message.content[i]
				if message.content[i] in '+-': 
					makeRoll()
					op = message.content[i]
				elif message.content[i] == '#':
					hashmssg=message.content[i:]
					i=len(message.content)
				
			i+=1
		if (n>0):
			takeNumber(n)
			n=0
			
		if numDice > 0:
			makeRoll()
								
		if total > 0:		
			response = RollDesc + ' = ' + str(total)+' '+hashmssg
		else:
			response = """To use, type '!' followed by the dice equation ie. (3d6) (1d20+8) (2d6+1d8)
			To reroll rolls at or below a minimum value(once), use r, such as !3d6r1 
			To keep rerolling, use rr instead, !3d6rr1
			To only keep some of the dice rolled, use k, such as !4d6k3
			If the desired dice equation is 1d20+[n], you can use !Xn"""
		await message.channel.send(response)
    
	else:
		return

client.run(TOKEN)