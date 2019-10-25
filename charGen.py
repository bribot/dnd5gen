# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from xml.dom import minidom
from random import randint
import random

races = []
classes = []
banlist = [] 
pStats={
        "STR":"",
        "DEX":"",
        "CON":"",
        "INT":"",
        "WIS":"",
        "CHA":""
        }


# parse an xml file by name
mydoc = minidom.parse('./compendium/Character Compendium 3.1.0.xml')

def init():
    items = mydoc.getElementsByTagName('race')
    
    for item in items:
        name=item.getElementsByTagName("name")[0]
        name=name.firstChild.data
        name=name.lower()
        #print(name)
        races.append(name)
        
    items = mydoc.getElementsByTagName('class')
    
    for item in items:
        name=item.getElementsByTagName("name")[0]
        name=name.firstChild.data
        name=name.lower()
        #print(name)
        classes.append(name)

# ---------------------------------------------------
def genCharacter(race="",cclass="",lvl=1):
    if race=="":
        race=races[randint(0,len(races)-1)]
    if cclass=="":
        cclass=classes[randint(0,len(classes)-1)]
    print("Behold the %s %s!" % (race,cclass))
# ---------------------------------------------------
    
def getRace(race):
    result={"name":race,
            "size":"",
            "speed":"",
            "ability":""}
    if race=="":
        print("no valid race")
        return result
    
    node = mydoc.getElementsByTagName('race')
    for subnode in node:
        if subnode.getElementsByTagName('name')[0].firstChild.data == race:
            node=subnode
            break
    
    item=node.getElementsByTagName("size")[0]
    result["size"]=item.firstChild.data
    
    item=node.getElementsByTagName("speed")[0]
    result["speed"]=item.firstChild.data
    
    item=node.getElementsByTagName("ability")[0]
    result["ability"]=item.firstChild.data
    
    return result

def getClass(cclass):
    result={"name":cclass,
            "hd":"",
            "proficiency":"",
            "spellAbility":""}
    if cclass=="":
        print("no valid class")
        return result
    
    node = mydoc.getElementsByTagName('class')
    for subnode in node:
        if subnode.getElementsByTagName('name')[0].firstChild.data == cclass:
            node=subnode
            break
    
    item=node.getElementsByTagName("hd")[0]
    result["hd"]=item.firstChild.data
    
    item=node.getElementsByTagName("proficiency")[0]
    result["proficiency"]=item.firstChild.data
    try:
        item=node.getElementsByTagName("spellAbility")[0]
        result["spellAbility"]=item.firstChild.data
    except:
        result["spellAbility"]=""
    
    return result

def findTextNodes(nodeList):
    noprint=["text","name"]
    for subnode in nodeList:
        if subnode.nodeType == subnode.ELEMENT_NODE:
            if subnode.tagName not in noprint:
                print(subnode.tagName)
            # call function again to get children
            findTextNodes(subnode.childNodes)
        elif subnode.nodeType == subnode.TEXT_NODE:
            if("\t" not in subnode.data):
                #print("text node: ")
                
                print(subnode.data)

def searchInfo(search):
    items=""
    search=search.lower()
    for race in races:
        if search in race:
            items=mydoc.getElementsByTagName("race")
    for cclass in classes:
        if search in classes:
            items=mydoc.getElementsByTagName("class")
    if items=="":
        print("no info in database")
        return
    for item in items:
        name=item.getElementsByTagName("name")[0].firstChild.data
        name=name.lower()
        if name.startswith(search):
            print("----------------------------------")
            findTextNodes(item.childNodes)
    return

def listInfo(search):
    result=[]
    items=""
    search=search.lower()
    for race in races:
        if search in race:
            items=mydoc.getElementsByTagName("race")
    for cclass in classes:
        if search in classes:
            items=mydoc.getElementsByTagName("class")
    if items=="":
        print("no info in database")
        result=[""]
        return result
    for item in items:
        name=item.getElementsByTagName("name")[0].firstChild.data
        namel=name.lower()
        if namel.startswith(search):
            result.append(name)
            print(name)
    return result

# TODO: OPTIONS TO ROLL
def genStats(diceS=6,diceR=4,diceK=3):
    stats=[]
    rolls=[]
    for i in range(len(pStats)):
        roll=[]
        stat=0
        for j in range(diceR):
            roll.append(random.randint(1,diceS))
        roll.sort(reverse=1)
        rolls.append(roll)
        
        stat = sum(roll[0:diceK])
        
#        for j in range(diceK):
#            stat+=roll[j]
        stats.append(stat)
        
    return stats,rolls

#def sortStats(oStats,npcConf):
#    newStats=[]
#    for i in npcConf:
#        newStats.append(0)
#    tmpStats=oStats.copy()
#    tmpStats.sort(reverse=1)
#    priority=1
#    while priority<=len(npcConf):
#        for current in range(len(npcConf)):
#            if npcConf[current][0]==priority:
#                if tmpStats[priority-1]!=0:
#                    newStats[current]=tmpStats[priority-1]+npcConf[current][1]
#                    tmpStats[priority-1]=0
#        priority+=1
#    for s in range(len(newStats)):
#        while newStats[s]==0:
#            r = random.randint(0,len(npcConf)-1)
#            newStats[s]=tmpStats[r]
#            tmpStats[r]=0
#    return newStats

def sortStats(stats,cclass):
    proficiency=[]
    bestStats=[]
    for p in cclass["proficiency"].split():
        proficiency.append(p[0:3].lower())
    stats.sort()
    for p in proficiency:
        bestStats.append(stats.pop(-1))
        
    random.shuffle(bestStats)
    random.shuffle(stats)
    
    for stat in pStats:
        print(stat)
        if stat.lower() in proficiency:
            print("*")
            pStats[stat]=bestStats.pop(-1)
        else:
            pStats[stat]=stats.pop(-1)
            

def main():    
    init()
    # Basic Selection
#    selection=listInfo("Elf")
#    print(getRace(selection[0]))
    selection=listInfo("rogue")
    npcC = getClass(selection[0])
    print(npcC)
    s=[10,11,12,13,14,15]
    sortStats(s,npcC)
    print(pStats)
#    print(genStats())
#    print(classes)
    

    

if __name__=="__main__":
    main()



