# bot.py
import os
import random

import discord
from discord import app_commands
from dotenv import load_dotenv

import interactions 

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = interactions.Client(token=TOKEN)

@bot.command(
    name="dice",
    description="Roll some dice",
    options= [
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=False,
        ),
    ],
)

async def dice(ctx: interactions.CommandContext, text:str):
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
        numExpected=' '
    
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
    
    
    startRoll()
        
    i=0
    if text[i] in 'xX':
        numExpected='n'
        takeNumber(1)
        numExpected='d'
        takeNumber(20)
        makeRoll()
    elif text[i] in 'hH':
        total = 0
        i = len(text);
            
    while i < len(text):
        
        if text[i] in '1234567890':
            n = (n * 10) + int(text[i])
        else:
            if n>0:
                takeNumber(n)
                n=0
            if text[i] in 'dDrRkK': 
                if (numExpected in 'rR') and (text[i] in 'rR'):
                    keepRerolling = True
                numExpected = text[i]
            if text[i] in '+-': 
                makeRoll()
                op = text[i]
            elif text[i] == '#':
                hashmssg=text[i:]
                i=len(text)
            
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
    
    
    await ctx.send(response)

bot.start()