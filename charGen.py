# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from xml.dom import minidom
from random import randint
import random

class generator():
    def __init__(self):
        # parse an xml file by name
        self.mydoc = minidom.parse('./compendium/Character Compendium 3.1.0.xml')
        self.races = []
        self.classes = []
        self.backgrounds= []
        self.banlist = [] 
        #-------------------------
        self.pRace=""
        self.pClass=""
        self.pBackground=""
        self.pHP=0
        self.pDC=0
        self.pSpeed=0
        self.pStats={
                "STR":"",
                "DEX":"",
                "CON":"",
                "INT":"",
                "WIS":"",
                "CHA":""
                }
        #--------------------------
        items = self.mydoc.getElementsByTagName('race')
        for item in items:
            name=item.getElementsByTagName("name")[0]
            name=name.firstChild.data
            name=name.lower()
            #print(name)
            self.races.append(name)
            
        items = self.mydoc.getElementsByTagName('class')
        for item in items:
            name=item.getElementsByTagName("name")[0]
            name=name.firstChild.data
            name=name.lower()
            #print(name)
            self.classes.append(name)
            
        items = self.mydoc.getElementsByTagName('background')
        for item in items:
            name=item.getElementsByTagName("name")[0]
            name=name.firstChild.data
            name=name.lower()
            #print(name)
            self.backgrounds.append(name)
    
    # ---------------------------------------------------
    def genCharacter(self,race="",cclass="",lvl=1):
        if race=="":
            race=self.races[randint(0,len(self.races)-1)]
        if cclass=="":
            cclass=self.classes[randint(0,len(self.classes)-1)]
        print("Behold the %s %s!" % (race,cclass))
    # ---------------------------------------------------
        
    def getRace(self,race):
        result={"name":race,
                "size":"",
                "speed":"",
                "ability":""}
        if race=="":
            print("no valid race")
            return result
        
        node = self.mydoc.getElementsByTagName('race')
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
    
    def getClass(self,cclass):
        result={"name":cclass,
                "hd":"",
                "proficiency":"",
                "spellAbility":""}
        if cclass=="":
            print("no valid class")
            return result
        
        node = self.mydoc.getElementsByTagName('class')
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
    
    def getBackground(self,bg):
        result={"name":bg,
                "proficiency":"",
                "traits":[]}
        if bg=="":
            print("no valid background")
            return result
        
        node = self.mydoc.getElementsByTagName('background')
        for subnode in node:
            if subnode.getElementsByTagName('name')[0].firstChild.data == bg:
                node=subnode
                break
        
        item=node.getElementsByTagName("proficiency")[0]
        result["proficiency"]=item.firstChild.data
        
        item=node.getElementsByTagName("trait")
        for i in item:
            result["traits"].append(i.getElementsByTagName("name")[0].firstChild.data)
        
        return result
    
    def findTextNodes(self,nodeList):
        noprint=["text","name"]
        for subnode in nodeList:
            if subnode.nodeType == subnode.ELEMENT_NODE:
                if subnode.tagName not in noprint:
                    print(subnode.tagName)
                # call function again to get children
                self.findTextNodes(subnode.childNodes)
            elif subnode.nodeType == subnode.TEXT_NODE:
                if("\t" not in subnode.data):
                    #print("text node: ")
                    
                    print(subnode.data)
    
    def searchInfo(self,search):
        items=""
        search=search.lower()
        
        for race in self.races:
            if search in race:
                items = self.mydoc.getElementsByTagName("race")
        
        for cclass in self.classes:
            if search in self.classes:
                items=self.mydoc.getElementsByTagName("class")
                
        for bg in self.backgrounds:
            if search in self.backgrounds:
                items=self.mydoc.getElementsByTagName("background")
        
        if items=="":
            print("no info in database")
            return
        for item in items:
            name=item.getElementsByTagName("name")[0].firstChild.data
            name=name.lower()
            if name.startswith(search):
                print("----------------------------------")
                self.findTextNodes(item.childNodes)
        return
    
    def listInfo(self,search):
        result=[]
        items=""
        search=search.lower()
        for race in self.races:
            if search in race:
                items=self.mydoc.getElementsByTagName("race")
        for cclass in self.classes:
            if search in self.classes:
                items=self.mydoc.getElementsByTagName("class")
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
    def genStats(self,diceS=6,diceR=4,diceK=3):
        stats=[]
        rolls=[]
        for i in range(len(self.pStats)):
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
    
    def sortStats(self,stats,cclass):
        proficiency=[]
        bestStats=[]
        for p in cclass["proficiency"].split():
            proficiency.append(p[0:3].lower())
        stats.sort()
        for p in proficiency:
            bestStats.append(stats.pop(-1))
            
        random.shuffle(bestStats)
        random.shuffle(stats)
        
        for stat in self.pStats:
            #print(stat)
            if stat.lower() in proficiency:
                #print("*")
                self.pStats[stat]=bestStats.pop(-1)
            else:
                self.pStats[stat]=stats.pop(-1)
                
    def racialFeatures(self,race):
        mods = race["ability"].split(",")
        ability={}
        
        for mod in mods:
            temp=mod.split()
            ability[temp[0]]=int(temp[1])
        for mod in ability:
            # Look I just want to put a + sign ok?
            if ability[mod]>0:
                strMod="+"+str(ability[mod])
            else:
                strMod=str(ability[mod])
            self.pStats[mod.upper()]=[self.pStats[mod.upper()]+ability[mod],strMod]
        return
    
    # TODO: Class features per level
    def levelUp(self,lvl,pClass):
        hd=int(pClass["hd"])
        hp=hd+hd*(lvl-1)
        return hp
        
        
    
    def generate(self,race,cclass):
        selection = self.listInfo(cclass)
        npcC = self.getClass(selection[0])
        self.pClass = selection[0]
        #-------------------------
        print(npcC)
        #-------------------------
        s = self.genStats()[0]
        self.sortStats(s,npcC)
        selection = self.listInfo(race)
        npcR = self.getRace(selection[0])
        self.racialFeatures(npcR)
        for s in self.pStats:
            print(s + ":"+ str(self.pStats[s]))
    #    print(genStats())
    #    print(classes)
    

    

#if __name__=="__main__":
#    main()

class character():
    def __init__(self):
        self.race=""
        self.cclass=""
        self.HP=0
        self.Stats={
                "STR":"",
                "DEX":"",
                "CON":"",
                "INT":"",
                "WIS":"",
                "CHA":""}
        self.DC=0
        self.speed=0
