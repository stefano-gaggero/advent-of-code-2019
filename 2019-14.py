# -*- coding: utf-8 -*-

"""
--- Day 14: Space Stoichiometry ---

As you approach the rings of Saturn, your ship's low fuel indicator turns on. There isn't any fuel here, but the rings have plenty of raw material. Perhaps your ship's Inter-Stellar Refinery Union brand nanofactory can turn these raw materials into fuel.

You ask the nanofactory to produce a list of the reactions it can perform that are relevant to this process (your puzzle input). Every reaction turns some quantities of specific input chemicals into some quantity of an output chemical. Almost every chemical is produced by exactly one reaction; the only exception, ORE, is the raw material input to the entire process and is not produced by a reaction.

You just need to know how much ORE you'll need to collect before you can produce one unit of FUEL.

Each reaction gives specific quantities for its inputs and output; reactions cannot be partially run, so only whole integer multiples of these quantities can be used. (It's okay to have leftover chemicals when you're done, though.) For example, the reaction 1 A, 2 B, 3 C => 2 D means that exactly 2 units of chemical D can be produced by consuming exactly 1 A, 2 B and 3 C. You can run the full reaction as many times as necessary; for example, you could produce 10 D by consuming 5 A, 10 B, and 15 C.

Suppose your nanofactory produces the following list of reactions:

10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL

The first two reactions use only ORE as inputs; they indicate that you can produce as much of chemical A as you want (in increments of 10 units, each 10 costing 10 ORE) and as much of chemical B as you want (each costing 1 ORE). To produce 1 FUEL, a total of 31 ORE is required: 1 ORE to produce 1 B, then 30 more ORE to produce the 7 + 7 + 7 + 7 = 28 A (with 2 extra A wasted) required in the reactions to convert the B into C, C into D, D into E, and finally E into FUEL. (30 A is produced because its reaction requires that it is created in increments of 10.)

Given the list of reactions in your puzzle input, what is the minimum amount of ORE required to produce exactly 1 FUEL?

----------------------------------------------------

--- Part Two ---

After collecting ORE for a while, you check your cargo hold: 1 trillion (1000000000000) units of ORE.

With that much ore, given the examples above:

    The 13312 ORE-per-FUEL example could produce 82892753 FUEL.
    The 180697 ORE-per-FUEL example could produce 5586022 FUEL.
    The 2210736 ORE-per-FUEL example could produce 460664 FUEL.

Given 1 trillion ORE, what is the maximum amount of FUEL you can produce?

"""
import math
import re
import collections

class Substance:
    def __init__(self, toupleRepr):
        self.name = toupleRepr[1]
        self.qty = int(toupleRepr[0])
        self.reqQuantity = 0
        self.usedIn = 0

    def __str__(self):
        return "[" + str(self.qty) + " " + str(self.name) + " - req: " + str(self.reqQuantity) + "]"
    
    def __repr__(self):
        return self.__str__()
    
    def useInReaction(self, val):
        self.reqQuantity = self.reqQuantity + val
        self.usedIn = self.usedIn - 1
        

class Reaction:    
    def __init__(self, reacStr):
        # (?: ... ) non capturing group
        # (?P<name>... ) capturing  group with name        
        rec = re.compile("(?:([0-9]+) {1}([A-Z]+),{0,1})+")
        parts = reacStr.split("=>")
        reagsRepr = rec.findall(parts[0])
        self.reags = [Substance(r) for r in reagsRepr]  
        
        prodRepr = (rec.findall(parts[1]))[0]
        self.prod = Substance(prodRepr)
    
    def __str__(self):
        return "[" + self.prod.name + " " + str(self.prod.reqQuantity) + " " + str(self.prod.usedIn) + "]"
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):     
        return self.name.__hash__()
    
        
 
class Reactions:
    def __init__(self, fileName, fuelQty=1):
        
       
        #La struttura reactions contiene tutte le reazioni usando come chiave il nome del prodotto
        #Ciascun elemento è prodotto da almeno una relazione (a parte ORE)
        #Dunque l'istanza Reagent relativa al prodotto è anche la classe principale per tale elemento che tiene conto delle quantità di tale elemento richiesta dalle precedenti reazioni
        self.reactions = {} 
               
        #Coda con le relazioni da processare
        self.queue = [] 
        self.oreQty = 0
        with open(fileName) as f:
            for line in f:
                r = Reaction(line)
                self.reactions[r.prod.name] = r
        
        for key in self.reactions:
            reaction = self.reactions[key]
            for r in reaction.reags:
                if r.name != 'ORE':
                    self.reactions[r.name].prod.usedIn = self.reactions[r.name].prod.usedIn + 1
                
        #for key in self.reactions:
        #       print(self.reactions[key] )
        #print("-----------------")
                
        #Inserisco la prima relazione nella coda
        fuelReac = self.reactions['FUEL']
        fuelReac.prod.useInReaction(fuelQty) 
        self.addToQueue(fuelReac)

    #Aggiunge una reazione nella coda, se non presente, altrimenti ne aggiorna la quantità richiesta
    def addToQueue(self, obj): 
        if not obj in self.queue:
            #print("add: " + obj.prod.name + " (" + str(obj.prod.reqQuantity) + ")")
            self.queue.insert(0, obj)


    def processReaction(self, k = 0):
        if k==50:  
            print("Raggiunta massima profondità")
            return  #Massima profondità di ricorsione
        k = k + 1
        
        try:
            reaction = self.queue.pop()  #Prossima relazione

            #print("pop " + reaction.prod.name)
            if reaction.prod.usedIn > 0:
                self.addToQueue(reaction)
                self.processReaction(k+1)
                return
        except:
            return #la coda è vuota

        elName = reaction.prod.name #Nome dell'elemento X prodotto dalla relazione
        reactionQty = reaction.prod.qty  #Quantità di X ottenuta dalla reazione R
        elQty = reaction.prod.reqQuantity #Quantità di X richiesta dalle precedenti reazioni
          
        
        #n è il moltiplicatore da applicare alla reazione per ottenere la quantità voluta ei X
        n = int(math.ceil(elQty/reactionQty))  #approssimazione per eccesso
        
        #print("Produce " + reaction.prod.name + " (qty: " + str(n*reactionQty) + ", requested: " + str(reaction.prod.reqQuantity) + ", used: " + str(reaction.prod.reqQuantity-elQty) + ")")                        
        
        #Scorre i reagenti, aggiorna le quantità richieste e li inserisce nella coda (se non presenti)
        for reag in reaction.reags:
            if reag.name=='ORE':
                self.oreQty = self.oreQty + reag.qty*n
                #print("Add " + str(reag.qty*n) + " ORE to product " + str(n*reactionQty) + " " + elName)
            else:
                reagMain = self.reactions[reag.name]  #Reazione di produzione di reag
                reagMain.prod.useInReaction(reag.qty*n) #Aggiorna la quantità richiesta
                self.addToQueue(reagMain) #Aggiunge la relazione alla coda

        #print(self.queue)
        self.processReaction(k)
        
#-----------------------------------------------------------------------------

r = Reactions("puzzle14.txt")     
r.processReaction()
    
print(r.oreQty) #337862 
print("------")

#Part 2------------------------------------------
N = 1000000000000
r = Reactions("puzzle14.txt",1)      
r.processReaction()

n = int(N*1.245/r.oreQty)

while r.oreQty<N:
    if (n%1000)==0:
        print("Test " + str(n))
    n = n + 1
    r = Reactions("puzzle14.txt",n)      
    r.processReaction()
    
print(n-1) #460665
r = Reactions("puzzle14.txt",n-1)      
r.processReaction()
print(r.oreQty)
print(r.oreQty<N)
print("------")
r = Reactions("puzzle14.txt",n)      
r.processReaction()
print(r.oreQty)
print(r.oreQty<N)