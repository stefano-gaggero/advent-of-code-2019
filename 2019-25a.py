# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 11:36:27 2020

@author: stefano
"""

import intcomputer as cmp

cpm = cmp.loadFromFile("puzzle25.txt")

while True:
    cpm.run()
    out = cpm.getOutputs()
    print(''.join(out))
    inp = input("--->")
    if inp=="bye":
        break
    if not(inp=="north" or inp=="south" or inp=="east" or inp=="west" or inp=="take" or inp=="drop" or inp=="inv"):
        print("Comando non riconosciuto")
    inp = list(inp)
    inp.append(10)
    cpm.addInputs(list(inp))