# -*- coding: utf-8 -*-
"""
Ogni oggetto obj ha un puntatore all'oggetto intorno a cui orbita (tale relazione è univoca)

getNumDep(): restituisce il numero di oggetti totali intorno obj orbita direttamente e indirettamente
getDepsChain(): restituisce la lista sotto forma di codici stringa degli oggetti intorno obj orbita direttamente e indirettamente

objs è un dictionary con tutti gli oggetti nel puzzle

Per trovare il numero di passi tra un oggetto A e un oggetto B si percorre a ritroso la catena di A e di B fino a trovare un elemento comune
"""

class Obj:
    pointTo = None
    code = None
    
    def __init__(self, code):
        self.code = code
    
    def getNumDep(self):
        k = 0
        pt = self.pointTo
        while pt is not None:
            k = k + 1
            pt = pt.pointTo
        return k
    
    def getDepsChain(self):
        pt = self.pointTo
        ret = []
        while pt is not None:
            ret.append(pt.code)
            pt = pt.pointTo            
        return ret
    

objs = {}

f = open("puzzle06.txt", "r")    
for line in f:
    rel = line.split(")")
    code1 = rel[0]
    code2 = rel[1].strip()
    if code1 not in objs:
        objs[code1] = Obj(code1)        
    if code2 not in objs:
        objs[code2] = Obj(code2)        
        
    if objs[code2].pointTo is not None:
        print("Errore!")    
        break
    
    objs[code2].pointTo = objs[code1] 
f.close()  

k = 0
for code in objs:
    k = k + objs[code].getNumDep()

print("TOT count: " + str(k))

youDeps = objs["YOU"].getDepsChain()
sanDeps = objs["SAN"].getDepsChain()

ceNum = len(list(set(youDeps).intersection(sanDeps)))

stepsNum = len(youDeps) + len(sanDeps) - 2*ceNum

print("Steps to: " + str(stepsNum))
