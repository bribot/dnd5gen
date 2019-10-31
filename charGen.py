# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from xml.dom import minidom
from random import randint
import random

def testScript():
    vat = generator()
    for i in vat.classes:
        vat.generate(race="Orc",cclass=i)

class generator():
    def __init__(self,banraces=[],banclasses=[],banbg=[]):
        # parse an xml file by name
        self.mydoc = minidom.parse('./compendium/Character Compendium 3.1.0.xml')
        self.races = []
        self.classes = []
        self.backgrounds= []
        self.banraces = banraces
        self.banclasses = banclasses
        self.banbg = banbg
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
            #print(name)
            if name not in self.banraces:
                name=name.lower()
                self.races.append(name)
            else:
                print(name + " banned!")
            
        items = self.mydoc.getElementsByTagName('class')
        for item in items:
            name=item.getElementsByTagName("name")[0]
            name=name.firstChild.data
            if name not in self.banclasses:
                name=name.lower()
                self.classes.append(name)
            else:
                print(name + " banned!")
            
        items = self.mydoc.getElementsByTagName('background')
        for item in items:
            name=item.getElementsByTagName("name")[0]
            name=name.firstChild.data
            if name not in self.banbg:
                name=name.lower()
                self.backgrounds.append(name)
            else:
                print(name + " banned!")
    
    # ---------------------------------------------------
    # TODO: EITHER DELETE OR MAKE IT RIGHT
#    def genCharacter(self,race="",cclass="",lvl=1):
#        if race=="":
#            race=self.races[randint(0,len(self.races)-1)]
#        if cclass=="":
#            cclass=self.classes[randint(0,len(self.classes)-1)]
#        print("Behold the %s %s!" % (race,cclass))
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
    #TODO: RETURN INFO AS A STR 
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
            return "no info in database"
        
        for item in items:
            name=item.getElementsByTagName("name")[0].firstChild.data
            name=name.lower()
            if name.startswith(search):
                print("----------------------------------")
                self.findTextNodes(item.childNodes)
        return
    
    def listInfo(self,search):
        result=[]
        items=[]
        search=search.lower()
        for race in self.races:
            if search in race:
                items.append(self.mydoc.getElementsByTagName("race"))
                break
        for cclass in self.classes:
            if search in cclass:
                items.append(self.mydoc.getElementsByTagName("class"))
                break
        for background in self.backgrounds:
            if search in background:
                items.append(self.mydoc.getElementsByTagName("background"))
                break
        if items=="":
            print("no info in database")
            result=[""]
            return result
        for itemS in items:
            for item in itemS:
#                print("......................")
#                print(item)
                name=item.getElementsByTagName("name")[0].firstChild.data
                namel=name.lower()
                if search in namel:
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
        ability={}
        mods = race["ability"].split(",")
        if len(mods)<2:
            mods=[]
        
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
        
        
    # TODO: USER INTERFACE
    # race should be a valid race
    # cclass should be a valid class
    def generate(self,race="",cclass=""):
        
        if race == "":
            race = self.races[random.randint(0,len(self.races)-1)]
            race=self.listInfo(race)[0]
            print("random race: "+race)
            
        if cclass == "":
            cclass = self.classes[random.randint(0,len(self.classes)-1)]
            cclass=self.listInfo(cclass)[0]
            print("random class: "+cclass)
        race = self.listInfo(race)[0]
        cclass = self.listInfo(cclass)[0]
        print(race + ", " + cclass)
        # Changed for the user interface seccion
        #selection = self.listInfo(cclass)
        npcC = self.getClass(cclass)
        self.pClass = cclass
        s = self.genStats()[0]
        self.sortStats(s,npcC)
        #selection = self.listInfo(race)
        npcR = self.getRace(race)
         #-------------------------
        print(npcC)
        #-------------------------
        print(npcR)
        #-------------------------
        self.racialFeatures(npcR)
        for s in self.pStats:
            print(s + ":"+ str(self.pStats[s]))
    #    print(genStats())
    #    print(classes)
    

    

#if __name__=="__main__":
#    main()

class character():
    def __init__(self):
        self.name=""
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
