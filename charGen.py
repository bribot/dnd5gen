# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from xml.dom import minidom
#from random import randint
import random
import math
from string import punctuation

TYPE_RACE = 0
TYPE_CLASS = 1
TYPE_BG = 2
#
#import charGen as gen
#vat = gen.generator()

def testScript():
    vat = generator()
    for r in vat.races:
        for c in vat.classes:
            for b in vat.backgrounds:
                vat.generate(race=r,cclass=c,bg=b)
def testClasses():
    vat = generator()
    for r in vat.classes:
        c=vat.listInfo(r)[0]
        c=vat.getClass(c)
        print("--------------------")
        print(c["name"])
        print(c["proficiency"])
        print(c["quickbuild"])
def testType():
    vat=generator()
    for r in vat.races:
        t = vat.getType(r)
        if t !=0:
            print("error in %s" % r)
            return 
    for r in vat.classes:
        t = vat.getType(r)
        if t !=1:
            print("error in %s" % r)
            return 
    for r in vat.backgrounds:
        t = vat.getType(r)
        if t !=2:
            print("error in %s" % r)
            return 
    print("ALL DONE!")
    

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
    
    def interface(self,search):
        """
        Returns: Str, code
        code:
            0 = random option
            1 = everything is right
            2 = more than one option
            3 = no options
        """
        r = ""
        c = ""
        b = ""
        if len(search)>0:
            for s in search.split(","):
                if s[0]==" ":
                    s=s[1:]
                    
                code=000
                ty = self.getType(s)
                if ty == 0:
                    r = s
                    code+=1
                elif ty == 1:
                    c = s
                    code+=10
                elif ty == 2:
                    b = s
                    code+=100
                elif ty ==10:
                    info=self.listInfo(s,0)
                    r=info[random.randint(0,len(info)-1)]
                    code+=2
                elif ty ==11:
                    info=self.listInfo(s,1)
                    c=info[random.randint(0,len(info)-1)]
                    code+=20
                elif ty ==12:
                    info=self.listInfo(s,2)
                    b=info[random.randint(0,len(info)-1)]
                    code+=200
                else:
                    print("Something went wrong")
                    return "error"
                
#                code=333
        #print("r: %s, c: %s, b: %s" % (r,c,b))
        res = self.generate(race=r,cclass=c,bg=b)
        
#        print(res)
        return res
    
    def getType(self,search):
        """    
        ty = 0 Race
        ty = 1 Class
        ty = 2 Background
        ty = 3 more than one element
        ty = 4 error 
    """
        search = search.lower()
        ty = 4
        if search in self.races:
            ty = 0
        elif search in self.classes:
            ty = 1
        elif search in self.backgrounds:
            ty = 2
        else:
            search=self.listInfo(search)
            if len(search)==0:
                return 4
            search = search[0].lower()
#            print(search)
            if search in self.races:
#                print("hey")
                ty = 10
            elif search in self.classes:
                ty = 11
            elif search in self.backgrounds:
                ty = 12
        return ty
        
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
                "quickbuild":"",
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
            
        item=node.getElementsByTagName("quickbuild")[0]
        result["quickbuild"]=item.firstChild.data
            
        item=node.getElementsByTagName("trait")
        for i in item:
            result[i.getElementsByTagName("name")[0].firstChild.data]=i.getElementsByTagName("text")[0].firstChild.data
      #-------------------------------------------------      
        item=node.getElementsByTagName("autolevel")
        for i in item:
            if i.getAttribute("level")=="1":
                t = i.getElementsByTagName("feature")
                for i in t:
            u=i.getElementsByTagName("name")
        #-------------------------------------------------
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
    
    def listInfo(self,search,searchType=4):
        result=[]
        items=[]
        search=search.lower()
        if searchType == TYPE_RACE or searchType==4:
            for race in self.races:
                if search in race:
                    items.append(self.mydoc.getElementsByTagName("race"))
                    break
        if searchType == TYPE_CLASS or searchType==4:
            for cclass in self.classes:
                if search in cclass:
                    items.append(self.mydoc.getElementsByTagName("class"))
                    break
        if searchType == TYPE_BG or searchType==4:
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
                name=item.getElementsByTagName("name")[0].firstChild.data
                namel=name.lower()
                if search in namel:
                    if namel[namel.find(search)-1] in punctuation+" " or namel == search or namel.find(search) == 0:
#                        print("hey")
#                        print(race[race.find(search)-1])
                        result.append(name)
                    #print(name)
        return result
        
    # TODO: OPTIONS TO ROLL
    # TODO: REROLL ON LOW STATS
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
    
    # TODO: use remaining stats
    def sortStats(self,stats,cclass):
        proficiency=[]
        bestStats=[]
#        otherStats=[]
        pStats = self.pStats
        
        for p in cclass["quickbuild"].split(","):
#            print("-------------")
#            print(p)
#            print("-------------")
            if len(p.split("or"))>1:
                p=p.split("or")[random.randint(0,len(p.split("or"))-1)]
#                print("-------------")
#                print(p)
#                print("-------------")
            if p[0]==" ":
                p=p[1:]
            proficiency.append(p[0:3].lower())
#        print(proficiency)
        stats.sort()
#        print(stats)
        for p in proficiency:
            bestStats.append(stats.pop(-1))
#            print(bestStats)
            
#        random.shuffle(bestStats)
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
        
        
    # TODO: ADD CLASSS EQUIPMENT
    # TODO: ADD TRINKET
    # TODO: SAVE CHARACTERS
    # race should be a valid race
    # cclass should be a valid class
    # bg should be a valid background
    def generate(self,race="",cclass="",bg="",lvl=1):
        result="-----GENERATING-----"
        if race.lower()  in self.races:
            raceT = self.listInfo(race,TYPE_RACE)
            for r in raceT:
                if r.lower() == race.lower():
                    race = r
        elif race == "":
            race = self.races[random.randint(0,len(self.races)-1)]
            race = self.listInfo(race,TYPE_RACE)[0]
            result+=("\n"+"random race: "+race)
        else:
            print("Not a valid race")
            return "Not a valid race"
            
        if cclass.lower() in self.classes:
            cclassT = self.listInfo(cclass,TYPE_CLASS)
            for c in cclassT:
                if c.lower().startswith(cclass.lower()):
                    cclass = c
        elif cclass == "":
            cclass = self.classes[random.randint(0,len(self.classes)-1)]
            cclass = self.listInfo(cclass,TYPE_CLASS)[0]
            result+=("\n"+"random class: "+cclass)
        else:
            print("Not a valid class")
            return "Not a valid class"
            
        if bg.lower() in self.backgrounds:
            bgT = self.listInfo(bg,TYPE_BG)
            for b in bgT:
                if b.lower().startswith(bg.lower()):
                    bg = b
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
        #-------------------------------------------
#       UNCOMMENT BEFORE RELEASE
        for s in pStats:
            result+=("\n"+s + ":"+ str(pStats[s][0])+"("+str(pStats[s][-1])+ ")")
            
        result+=("\nRacial: " + pRace["ability"])
        result+=("\n"+"HP: "+str(pHP))
        result+=("\n"+"Proficiency: "+str(pProficiency))
        result+=("\n"+pClass["proficiency"])
        result+=("\n"+pBg["proficiency"])
        result+=("\n"+"Spellcasting Ability: "+str(pClass["spellAbility"]))
        result+=("\n"+"DC: "+str(pDC))
        result+=("\n"+"Speed: "+str(pSpeed))
        result+=("\n"+"Equipment: \nBy Background:"+pBg["Equipment"])
        #------------------------------------------------------------------
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