# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from xml.dom import minidom
from random import randint
import random
import math

TYPE_RACE = 0
TYPE_CLASS = 1
TYPE_BG = 2

def testScript():
    vat = generator()
    for r in vat.races:
        for c in vat.classes:
            for b in vat.backgrounds:
                vat.generate(race=r,cclass=c,bg=b)
    

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
            if name.lower() not in self.banraces:
                name=name.lower()
                self.races.append(name)
            else:
                print(name + " banned!")
            
        items = self.mydoc.getElementsByTagName('class')
        for item in items:
            name=item.getElementsByTagName("name")[0]
            name=name.firstChild.data
            if name.lower() not in self.banclasses:
                name=name.lower()
                self.classes.append(name)
            else:
                print(name + " banned!")
            
        items = self.mydoc.getElementsByTagName('background')
        for item in items:
            name=item.getElementsByTagName("name")[0]
            name=name.firstChild.data
            if name.lower() not in self.banbg:
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
        
        item=node.getElementsByTagName("trait")
        for i in item:
            result[i.getElementsByTagName("name")[0].firstChild.data]=i.getElementsByTagName("text")[0].firstChild.data
        
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
            
        item=node.getElementsByTagName("trait")
        for i in item:
            result[i.getElementsByTagName("name")[0].firstChild.data]=i.getElementsByTagName("text")[0].firstChild.data
        
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
        
        try:
            item=node.getElementsByTagName("proficiency")[0]
            result["proficiency"]=item.firstChild.data
        except:
            print("no BG proficiency")
        
        item=node.getElementsByTagName("trait")
        for i in item:
            result[i.getElementsByTagName("name")[0].firstChild.data]=i.getElementsByTagName("text")[0].firstChild.data
        
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
    
    def listInfo(self,search,searchType):
        result=[]
        items=[]
        search=search.lower()
        if searchType == TYPE_RACE:
            for race in self.races:
                if search in race:
                    items.append(self.mydoc.getElementsByTagName("race"))
                    break
        elif searchType == TYPE_CLASS:
            for cclass in self.classes:
                if search in cclass:
                    items.append(self.mydoc.getElementsByTagName("class"))
                    break
        elif searchType == TYPE_BG:
            for background in self.backgrounds:
                if search in background:
                    items.append(self.mydoc.getElementsByTagName("background"))
                    break
                
        if items==[]:
            print("no info in database")
            result=[]
            return result
        
        for itemS in items:
            for item in itemS:
#                print("......................")
#                print(item)
                name=item.getElementsByTagName("name")[0].firstChild.data
                namel=name.lower()
                if search in namel:
                    result.append(name)
                    #print(name)
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
        pStats = self.pStats
        for p in cclass["proficiency"].split():
            proficiency.append(p[0:3].lower())
        stats.sort()
        for p in proficiency:
            bestStats.append(stats.pop(-1))
            
        random.shuffle(bestStats)
        random.shuffle(stats)
        
        for stat in pStats:
            #print(stat)
            if stat.lower() in proficiency:
                #print("*")
                pStats[stat]=bestStats.pop(-1)
            else:
                pStats[stat]=stats.pop(-1)
        for stat in pStats:
            pStats[stat] = [pStats[stat]]
        return pStats
    
    def getMods(self,pStats):
        for stat in pStats:
            mod = math.floor((int(pStats[stat][0])-10)/2)
            if mod >0:
                mod="+"+str(mod)
            else:
                mod=str(mod)
            pStats[stat].append(mod)
        return pStats
                
    def racialFeatures(self,race,pStats):
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
            pStats[mod.upper()]=[pStats[mod.upper()][0]+ability[mod]]
            pStats[mod.upper()].append(strMod)
        
        return pStats
    
    # TODO: Class features per level
    def getHP(self,lvl,pClass):
        hd=int(pClass["hd"])
        hp=[hd]
        for i in range(lvl-1):
            r = random.randint(1,hd)
            hp[0]+= r
            hp.append(r)
        return hp
    
    def getProficiency(self,lvl):
        p = 2+math.floor((lvl-1)/4)
        p = "+"+str(p)
        return p
    
    def getDC(self,pClass,pStats,proficiency):
        pDC=pClass["spellAbility"]
        if pDC == "":
            print("barbarian?")
            return
        else:
            pDC=pDC[0:3].upper()    
            pDC=pStats[pDC]
#            print("-------------")
#            print(pDC)
        pDC=8+int(pDC[-1])+proficiency
        return pDC
        
        
    # TODO: USER INTERFACE
    # race should be a valid race
    # cclass should be a valid class
    # bg should be a valid background
    def generate(self,race="",cclass="",bg="",lvl=1):
#        print("-----GENERATING-----")
        result="-----GENERATING-----"
        if race.lower()  in self.races:
            race = self.listInfo(race,TYPE_RACE)[0]
        elif race == "":
            race = self.races[random.randint(0,len(self.races)-1)]
            race = self.listInfo(race,TYPE_RACE)[0]
            result+=("\n"+"random race: "+race)
        else:
            print("Not a valid race")
            return "Not a valid race"
            
        if cclass.lower() in self.classes:
            cclass = self.listInfo(cclass,TYPE_CLASS)[0]
        elif cclass == "":
            cclass = self.classes[random.randint(0,len(self.classes)-1)]
            cclass = self.listInfo(cclass,TYPE_CLASS)[0]
            result+=("\n"+"random class: "+cclass)
        else:
            print("Not a valid class")
            return "Not a valid class"
            
        if bg.lower() in self.backgrounds:
            bg = self.listInfo(bg,TYPE_BG)[0]
        elif bg == "":
            bg = self.backgrounds[random.randint(0,len(self.backgrounds)-1)]
            bg = self.listInfo(bg,TYPE_BG)[0]
            result+=("\n"+"random background: "+ bg)
        else:
            print("Not a valid background")
            return "Not a valid background"
        
        pRace = self.getRace(race)
        pClass = self.getClass(cclass)
        pBg = self.getBackground(bg)
#        self.pClass = cclass
        opStats = self.genStats()
        pStats = self.sortStats(opStats[0],pClass)
        pStats = self.racialFeatures(pRace,pStats)
        pStats = self.getMods(pStats)
#        print(pStats)
        pHP = self.getHP(lvl,pClass)
        pProficiency = self.getProficiency(lvl)
        pDC = self.getDC(pClass,pStats,int(pProficiency))
        pSpeed = pRace["speed"]
#        print("--------------------------")
        result+="\n"+race+" "+cclass+" "+bg

        for s in pStats:
            result+=("\n"+s + ":"+ str(pStats[s][0])+"("+str(pStats[s][-1])+ ")")
            
        result+=("Racial: " + pRace["ability"])
        result+=("\n"+"HP: "+str(pHP))
        result+=("\n"+"Proficiency: "+str(pProficiency))
        result+=("\n"+pClass["proficiency"])
        result+=("\n"+pBg["proficiency"])
        result+=("\n"+"Spellcasting Ability: "+str(pClass["spellAbility"]))
        result+=("\n"+"DC: "+str(pDC))
        result+=("\n"+"Speed: "+str(pSpeed))
#        print("Languages:")
#        try:
#            print("*"+pRace["Languages"])
#        except:
#            print("")
#        try:
#            print("*"+pBg["Languages"])
#        except:
#            print("")
        result+=("\n"+"Equipment: "+pBg["Equipment"])
        
        
#        print("Rolls: ")
#        for r in opStats[1]:
#            print(str(r))
        #-------------------------
#        print(pClass)
#        print(pRace)
#        print(pBg)
        #-------------------------
#        print("---------------------------")
#        for i in pClass:
#            print(i)
#        print("---------------------------")
        return result
        
        
    

    

#if __name__=="__main__":
#    main()

class character():
    def __init__(self):
        self.name=""
        self.pRace=""
        self.pClass=""
        self.pBackground=""
        self.proficiency=""
        self.skillProficiency=""
        self.spellcastingAbility=""
        self.pHP=0
        self.pDC=0
        self.pSpeed=0
        self.Equipment=""
        self.pStats={
                "STR":"",
                "DEX":"",
                "CON":"",
                "INT":"",
                "WIS":"",
                "CHA":""
                }

#def bannedChar():
#    banr=['aarakocra',
# 'aasimar (fallen)',
# 'aasimar (protector)',
# 'aasimar (scourge)',
# 'bugbear',
# 'firbolg',
# 'genasi (air)',
# 'genasi (earth)',
# 'genasi (fire)',
# 'genasi (water)',
# 'goliath',
# 'hobgoblin',
# 'kenku',
# 'kobold',
# 'lizardfolk',
# 'shifter (razorclaw)',
# 'shifter (wildhunt)',
# 'tabaxi',
# 'triton',
# 'yuan-ti pureblood']
#    banc=['artificer',
# 'mystic (ua)',
# 'ranger (revised)']
#    bamb=['acolyte',
# 'caravan specialist',
# 'charlatan',
# 'city watch',
# 'clan crafter',
# 'cloistered scholar',
# 'cormanthor refugee',
# 'courtier',
# 'criminal',
# 'earthspur miner',
# 'entertainer',
# 'faction agent',
# 'far traveler',
# 'folk hero',
# 'gate urchin',
# 'guild artisan',
# 'harborfolk',
# 'haunted one',
# 'hermit',
# 'hillsfar merchant',
# 'hillsfar smuggler',
# 'inheritor',
# 'investigator',
# 'knight of the order',
# 'mercenary veteran',
# 'mulmaster aristocrat',
# 'noble',
# 'outlander',
# 'phlan refugee',
# 'sage',
# 'sailor',
# 'secret identity',
# 'shade fanatic',
# 'soldier',
# 'trade sherrif',
# 'urban bounty hunter',
# 'urchin',
# 'uthgardt tribe member',
# 'variant criminal (spy)',
# 'variant entertainer (gladiator)',
# 'variant guild artisan (guild merchant)',
# 'variant noble (knight)',
# 'variant sailor (pirate)',
# 'waterdhavian noble']