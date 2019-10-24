# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from xml.dom import minidom
from random import randint

races = []
classes = []
banlist = [] 

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

def genCharacter(race="",cclass="",lvl=1):
    if race=="":
        race=races[randint(0,len(races)-1)]
    if cclass=="":
        cclass=classes[randint(0,len(classes)-1)]
    print("Behold the %s %s!" % (race,cclass))
    
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
        return result
    for item in items:
        name=item.getElementsByTagName("name")[0].firstChild.data
        namel=name.lower()
        if namel.startswith(search):
            result.append(name)
            print(name)
    return result

def main():    
    init()
    selection=listInfo("dwarf")
    print(getRace(selection[0]))
    

    

if __name__=="__main__":
    main()



