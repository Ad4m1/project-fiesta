import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import datetime
from pathlib import Path
from random import *
import os

 #Adam's local branch!


Client = discord.Client()
client = commands.Bot(command_prefix = "!!")
cList = ["WARRIOR", "MAGE", "HUNTER", "ROGUE", "KNIGHT"]
#class#S;W;Sp;D;H;w;w;Armour;ring;xp
sWarrior = '1;7;1;3;1;12;short sword;none;none;none;0'
sMage = '1;2;7;3;2;10;beginners staff;none;none;none;0'
sHunter = '1;2;2;3;7;10;short bow;none;none;none;0'
sRogue = '1;2;1;4;7;10;rusty dagger;none;none;none;0'
sKnight = '1;4;1;2;1;16;short sword;damaged shield;none;none;0'
#amounts of rarity mobs
cLen = 5
uLen = 3
rLen = 2

#xp
c = 10
u = 15
r = 25

@client.event
async def on_ready():
    print("AIBO ONLINE")

#Get stat from user file
def gStat(line,stat):
    line = line.split(';')
    pClass = line[0]
    pLevel = line[1]
    pStrength = line[2]
    pWisdom = line[3]
    pSpeed = line[4]
    pDexterity = line[5]
    pHealth = line[6]
    pW1 = line[7]
    pW2 = line[8]
    pArmour = line[9]
    pRing = line[10]

    if stat == 'class':
        return pClass
    if stat == 'level':
        return pLevel
    if stat == 'strength':
        return pStrength
    if stat == 'wisdom':
        return pWisdom
    if stat == 'speed':
        return pSpeed
    if stat == 'dexterity':
        return pDexterity
    if stat == 'health':
        return pHealth
    if stat == 'w1':
        return pW1
    if stat == 'w2':
        return pW2
    if stat == 'armour':
        return pArmour
    if stat == 'ring':
        return pRing

def wAdv(uStats, advFile):
    
    u = open(uStats, 'r')
    sl = u.readline()
    u.close()

    hp = gStat(sl, 'health')
    w1 = gStat(sl, 'w1')
    w2 = gStat(sl, 'w2')
    
    wepFile = Path('items/' + w1 + '.item')
    w = open(wepFile, 'r')
    line = w.readline()
    w.close()
    wStats = line.split(';')
    wep = wStats[2]
    wDmg = wStats[4]
    

    if wep == 'Magic Weapon':
        att = gStat(sl, 'wisdom')
    if wep == 'Heavy Melee Weapon':
        att = gStat(sl, 'strength')
    if wep == 'Light Melee Weapon':
        att = gStat(sl, 'speed')
    if wep == 'Bow':
        att = gStat(sl, 'dexterity')

    hAtt = int(int(att)/2)
    
    

    #name;rarity;hp;dmg;phys/mag/true;drop
    
    a = open(advFile, 'r')
    line = a.readline().split(';')
    mobFile = line[0]
    a.close()
    
    m = open(mobFile, 'r')
    line = m.readline()
    m.close()

    mobStats = line.split(';')
    mHp = mobStats[2]
    mDmg = mobStats[3]


    a = open(advFile, 'w')
    a.write(mobFile + ';' + hp + ';' + wDmg + ';' + att + ';' + str(hAtt) + ';' + mHp + ';' + mDmg)
    a.close()
    
    

    
        
    

@client.event
async def on_message(message):

    mID = message.author.id
    uStats = Path('users/' + mID + '.stat')
    advFile = Path('advs/' + mID + '.adv')
    tFile = Path('cd/' + mID + '.t')
    

    

        
    
    if message.content.upper().startswith('!!SAY'):
        if "428555143114653697" in [role.id for role in message.author.roles]:
            args = message.content.split(" ")
            await client.send_message(message.channel, "%s" % (" ".join(args[1:])))
            try:
                await client.delete_message(message)
            except discord.errors.NotFound:
                return

    if message.content.upper() == '!!BEGIN':
        await client.send_message(message.channel, '`!!begin [class]`')

    if message.content.upper() == '!!CLASSES':
        await client.send_message(message.channel, '**CLASSES**: \n`Warrior: +Strength \nMage: +Wisdom \nRogue: +Speed \nHunter: +Dexterity \nKnight: +Health`')
    
    if message.content.upper().startswith('!!BEGIN '):
        if uStats.is_file():
            await client.send_message(message.channel, 'You are already registered!')
        else:
            args = message.content.split(" ")
            if not args[1].upper() in cList:
                await client.send_message(message.channel, 'Please choose a valid class. `!!classes` for help.')
            else:
                if args[1].upper() == 'WARRIOR':
                    stats = sWarrior
                elif args[1].upper() == 'MAGE':
                    stats = sMage
                elif args[1].upper() == 'HUNTER':
                    stats = sHunter
                elif args[1].upper() == 'ROGUE':
                    stats = sRogue
                elif args[1].upper() == 'KNIGHT':
                    stats = sKnight
                u = open(uStats, 'w+')
                u.write(args[1] + ';' + stats)
                u.close()
                await client.send_message(message.channel, 'You have entered the realm as a ' + args[1].lower() + '.')

    if message.content.upper() == '!!STATS':
        if not uStats.is_file():
            await client.send_message(message.channel, 'You do not have a character yet. `!!begin` for help.')
        else:
            u = open(uStats, 'r')
            sl = u.readline()
            u.close()

            await client.send_message(message.channel, '**YOUR STATS:**\n`\n Class: ' + gStat(sl, 'class') + '\n Health: ' + gStat(sl, 'health') + '\n Strength: ' + gStat(sl, 'strength') + '\n Wisdom:' + gStat(sl, 'wisdom') + '\n Speed: ' + gStat(sl, 'speed') + '\n Dexterity: ' + gStat(sl, 'dexterity') + '\n Hand 1: ' + gStat(sl, 'w1') + '\n Hand 2: ' + gStat(sl, 'w2') + '\n Armour: ' + gStat(sl, 'armour') + '\n Ring: ' + gStat(sl, 'ring') + '`')                                                                                                                                   
            
    if message.content.upper() == '!!ADVENTURE' or message.content.upper() == '!!ADV':
        if not uStats.is_file():
            await client.send_message(message.channel, 'You do not have a character yet. `!!begin` for help.')
        else:
            if not advFile.is_file():

                
           
                if tFile.is_file():
                
                    t = open(tFile, 'r')
                    waitTil = int(t.readline())
                    t.close()

                    tCurr = str(datetime.datetime.now())
                    tCurr = tCurr.replace('-','')
                    tCurr = tCurr.replace(' ','')
                    tCurr = tCurr.replace(':','')
                    tCurr = tCurr.replace('.','')
                    tCurr = int(tCurr)

                    
              
                    if tCurr > waitTil + 100000000:

                        t = open(tFile, 'w+')
                        t.write(str(tCurr))
                        t.close()
             
                
                        uName = message.author.mention
                        find = randint(1,1000)
                        #common
                        if find > 579 or find < 400:
                            mob = randint(1,cLen)
                            mobFile = Path('mobs/' + 'c' + str(mob) + '.mob')
                            m = open(mobFile, 'r')
                            line = m.readline()
                            m.close()

                            line = line.split(';')
                            mName = line[0]
                            await client.send_message(message.channel,uName + ' encountered a **' + mName + '**\n'+ 'It\'s Health Points: ' + line[2] + '\n`!!adv` to fight or `!!flee` to make a run for it.')

                            a = open(advFile, 'w+')
                            a.write(str(mobFile))
                            a.close()

                            wAdv(uStats, advFile)


                        #uncommon
                        elif find > 399 and find < 520:
                            mob = randint(1,uLen)
                            mobFile = Path('mobs/' + 'u' + str(mob) + '.mob')
                            m = open(mobFile, 'r')
                            line = m.readline()
                            m.close()

                            line = line.split(';')
                            mName = line[0]
                            await client.send_message(message.channel,uName + ' encountered a **' + mName + '**\n'+ 'It\'s Health Points: ' + line[2] + '\n`!!adv` to fight or `!!flee` to make a run for it.')

                            a = open(advFile, 'w+')
                            a.write(str(mobFile))
                            a.close()

                            wAdv(uStats, advFile)
                        #rare
                        elif find > 519 and find < 580:
                            mob = randint(1,rLen)
                            mobFile = Path('mobs/' + 'r' + str(mob) + '.mob')
                            m = open(mobFile, 'r')
                            line = m.readline()
                            m.close()

                            line = line.split(';')
                            mName = line[0]
                            await client.send_message(message.channel, uName + ' encountered a **' + mName + '**\n'+ 'It\'s Health Points: ' + line[2] + '\n`!!adv` to fight or `!!flee` to make a run for it.')

                            a = open(advFile, 'w+')
                            a.write(str(mobFile))
                            a.close()

                            wAdv(uStats, advFile)
                
                #not file
                else:
                    tCurr = str(datetime.datetime.now())
                    tCurr = tCurr.replace('-','')
                    tCurr = tCurr.replace(' ','')
                    tCurr = tCurr.replace(':','')
                    tCurr = tCurr.replace('.','')
                    tCurr = str(tCurr)
                    
                    t = open(tFile, 'w+')
                    t.write(tCurr)
                    t.close()

                    uName = message.author.mention
                    find = randint(1,1000)
                    #common
                    if find > 579 or find < 400:
                        mob = randint(1,cLen)
                        mobFile = Path('mobs/' + 'c' + str(mob) + '.mob')
                        m = open(mobFile, 'r')
                        line = m.readline()
                        m.close()

                        line = line.split(';')
                        mName = line[0]
                        await client.send_message(message.channel,uName + ' encountered a **' + mName + '**\n'+ 'It\'s Health Points: ' + line[2] + '\n`!!adv` to fight or `!!flee` to make a run for it.')

                        a = open(advFile, 'w+')
                        a.write(str(mobFile))
                        a.close()

                        wAdv(uStats, advFile)


                    #uncommon
                    elif find > 399 and find < 520:
                        mob = randint(1,uLen)
                        mobFile = Path('mobs/' + 'u' + str(mob) + '.mob')
                        m = open(mobFile, 'r')
                        line = m.readline()
                        m.close()

                        line = line.split(';')
                        mName = line[0]
                        await client.send_message(message.channel,uName + ' encountered a **' + mName + '**\n'+ 'It\'s Health Points: ' + line[2] + '\n`!!adv` to fight or `!!flee` to make a run for it.')

                        a = open(advFile, 'w+')
                        a.write(str(mobFile))
                        a.close()

                        wAdv(uStats, advFile)
                    #rare
                    elif find > 519 and find < 580:
                        mob = randint(1,rLen)
                        mobFile = Path('mobs/' + 'r' + str(mob) + '.mob')
                        m = open(mobFile, 'r')
                        line = m.readline()
                        m.close()

                        line = line.split(';')
                        mName = line[0]
                        await client.send_message(message.channel, uName + ' encountered a **' + mName + '**\n'+ 'It\'s Health Points: ' + line[2] + '\n`!!adv` to fight or `!!flee` to make a run for it.')

                        a = open(advFile, 'w+')
                        a.write(str(mobFile))
                        a.close()

                        wAdv(uStats, advFile)
                    
                   
                
            else:
                

                a = open(advFile, 'r')
                advInfo = a.readline()
                a.close()

                advInfo = advInfo.split(';')
                
                deal = randint(int(advInfo[4]), int(advInfo[3])) + int(advInfo[2])
                take = randint(int(advInfo[6])-1,int(advInfo[6])+1)

                newHP = int(advInfo[1]) - take
                eneHP = int(advInfo[5]) - deal

                if newHP < 0:
                    newHP = 0
                if eneHP < 0:
                    eneHP = 0

                await client.send_message(message.channel, 'You attacked.\n `Dealt: ' + str(deal) + '` - `Took: ' + str(take) + '`\n Your HP: ' + str(newHP) + '\n Enemy HP: ' + str(eneHP))
                
                a = open(advFile, 'w')
                a.write(advInfo[0] + ';' + str(newHP) + ';' + advInfo[2] + ';' + advInfo[3] + ';' + advInfo[4] + ';' + str(eneHP) + ';' + advInfo[6])
                a.close()

                #win
                if int(eneHP) == 0:
                    u = open(uStats, 'r')
                    line = u.readline()
                    u.close()
                    
                    line = line.split(';')
                    line[11] = str(int(line[11]) + c)

                    line = ";".join(line)
                    
                    u = open(uStats, 'w')
                    u.write(str(line))
                    u.close()

                    await client.send_message(message.channel, 'You have been awarded ' + str(c) + 'xp for your victory!')
                    os.remove(advFile)
                #lose
                elif advInfo[1] == 0:
                    await client.send_message(message.channel, 'You have been defeated!')
                    os.remove(advFile)
                
               
    if message.content.upper() == '!!FLEE' or message.content.upper() == '!!FF':
        uName = message.author.mention
        
        if advFile.is_file():            
            os.remove(advFile)
            await client.send_message(message.channel, uName + ' has fled from battle.')
        else:
            await client.send_message(message.channel, uName + ', you are not in a battle.')



#~~TOKEN~~#~>            
client.run("NDMyMDgwOTk4MjM1MzczNTc4.DaoGpw.IXmBR4yn5Y_sULslOvxd4MWMJRM");
#~~~~~~~~~#~>
