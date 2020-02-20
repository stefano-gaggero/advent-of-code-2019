# -*- coding: utf-8 -*-

import numpy as np

"""
Intcode computer v.9.0 ---------------------------------------------

---------------------------------------------------
v day2

An Intcode program is a list of integers separated by commas (like 1,0,0,3,99). To run one, start by looking at the first integer (called position 0). Here, you will find an opcode - either 1, 2, or 99. The opcode indicates what to do; for example, 99 means that the program is finished and should immediately halt. Encountering an unknown opcode means something went wrong.

Opcode 1 adds together numbers read from two positions and stores the result in a third position. The three integers immediately after the opcode tell you these three positions - the first two indicate the positions from which you should read the input values, and the third indicates the position at which the output should be stored.

For example, if your Intcode computer encounters 1,10,20,30, it should read the values at positions 10 and 20, add those values, and then overwrite the value at position 30 with their sum.

Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them. Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.

Once you're done processing an opcode, move to the next one by stepping forward 4 positions.

---------------------------------------------------
v day5

The Thermal Environment Supervision Terminal (TEST) starts by running a diagnostic program (your puzzle input). The TEST diagnostic program will run on your existing Intcode computer after a few modifications:

First, you'll need to add two new instructions:

    Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example, the instruction 3,50 would take an input value and store it at address 50.
    Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address 50.

Programs that use these instructions will come with documentation that explains what should be connected to the input and output. The program 3,0,4,0,99 outputs whatever it gets as input, then halts.

Second, you'll need to add support for parameter modes:

Each parameter of an instruction is handled based on its parameter mode. Right now, your ship computer already understands parameter mode 0, position mode, which causes the parameter to be interpreted as a position - if the parameter is 50, its value is the value stored at address 50 in memory. Until now, all parameters have been in position mode.

Now, your ship computer will also need to handle parameters in mode 1, immediate mode. In immediate mode, a parameter is interpreted as a value - if the parameter is 50, its value is simply 50.

Finally, some notes:

    It is important to remember that the instruction pointer should increase by the number of values in the instruction after the instruction finishes. Because of the new instructions, this amount is no longer always 4.
    Integers can be negative: 1101,100,-1,4,0 is a valid program (find 100 + -1, store the result in position 4).

---------------------------------------------------
v day9

Your existing Intcode computer is missing one key feature: it needs support for parameters in relative mode.

Parameters in mode 2, relative mode, behave very similarly to parameters in position mode: the parameter is interpreted as a position. Like position mode, parameters in relative mode can be read from or written to.

The important difference is that relative mode parameters don't count from address 0. Instead, they count from a value called the relative base. The relative base starts at 0.

The address a relative mode parameter refers to is itself plus the current relative base. When the relative base is 0, relative mode parameters and position mode parameters with the same value refer to the same address.

For example, given a relative base of 50, a relative mode parameter of -7 refers to memory address 50 + -7 = 43.

The relative base is modified with the relative base offset instruction:

    Opcode 9 adjusts the relative base by the value of its only parameter. The relative base increases (or decreases, if the value is negative) by the value of the parameter.

For example, if the relative base is 2000, then after the instruction 109,19, the relative base would be 2019. If the next instruction were 204,-34, then the value at address 1985 would be output.

Your Intcode computer will also need a few other capabilities:

    The computer's available memory should be much larger than the initial program. Memory beyond the initial program starts with the value 0 and can be read or written like any other memory. (It is invalid to try to access memory at a negative address, though.)
    The computer should have support for large numbers. Some instructions near the beginning of the BOOST program will verify this capability.

"""

class Command:   
    def __init__(self, program):
        self.program = program
        val = self.program.getVal(self.program.ip)
        self.code = val%100
        self.paramsMode = [0,0,0]
        self.paramsMode[0] = (val%1000 - self.code)/100
        self.paramsMode[1] = (val%10000 - val%1000)/1000
        self.paramsMode[2] = (val%100000 - val%10000)/10000        
        
    #Restituisce il parametro decodificandolo in base alla tipologia
    #Non usato per gli indirizzi di scrittura
    def getParam(self, idx):
        val = self.program.getVal(self.program.ip + idx + 1)
        if self.paramsMode[idx]==0:  #Position mode
            return self.program.getVal(val)
        elif self.paramsMode[idx]==1: #Immediate mode
            return val
        elif self.paramsMode[idx]==2: #Relative mode
            return self.program.getVal(val + self.program.relativeBase)
     
    #Restituisce l'indirizzo di scrittura
    #La relative mode viene usata anche per gli indirizzi di scrittura
    def getAddress(self, idx):
        val = self.program.getVal(self.program.ip + idx + 1)
        if self.paramsMode[idx]==2: #Relative mode
            return val + self.program.relativeBase
        else:
            return val
    
    def toString(self):
        return str(self.code) + " " + str(self.paramsMode)
        
               
class Program:
          
    #Mai assegnarecome default [] ad un parametro:
    #https://nikos7am.com/posts/mutable-default-arguments/
    def __init__(self, progStr, name="", inputs=None):  
        self.program = np.array(list(map(int, progStr.split(","))), dtype='int64')  #per gestire grossi interi
        self.name = str(name)
        
        if inputs==None: self.inputs = []
        else: self.inputs = inputs
        
        self.outputs = []
        self.ended = False
        self.ic = 0 #Contatore degli input        
        self.oc = 0 #Contatore degli output
        self.ip = 0 #Instruction pointer
        self.relativeBase = 0
        self.rom = progStr
    
    def reset(self):
        self.__init__(self.rom, self.name, [])
        

    def addInput(self, val):        
        self.inputs.append(val)
                
    def getOutput(self, clearOutput=False):
        ret = self.outputs[self.oc]
        self.oc = self.oc + 1
        if clearOutput:
            self.outputs = []
            self.oc = 0            
        return ret
    
    def getLastOutput(self, clearOutput=False):
        return self.outputs[len(self.outputs)-1]
    
    def getOutputs(self, clearOutput=False):
        res = self.outputs.copy()
        if clearOutput:
            self.outputs = []
            self.oc = 0            
        return res

    def isEnded(self):
        return self.ended

    #All'occorrenza estende l'array
    def __extendTo(self, pos):
        N = pos - len(self.program) + 1
        if N > 0:
            self.program = np.pad(self.program, (0, N), 'constant') #Estende la memoria in caso di scrittura oltre le dimensioni del programma
    
    def writeTo(self, pos, val):
        self.__extendTo(pos)
        self.program[pos] = val
        
    def getVal(self, pos):
        self.__extendTo(pos)
        return self.program[pos]
        
    def run(self, debug=False):
        
        ip0 = -1     
        pause = False
        
        if debug:
            print("run....")
            
        while not pause:
            
            if(self.ip >= len(self.program)):
                break;
                
            if self.ip==ip0:
                print("Endless loop!")
                break
            ip0 = self.ip
            
            cmd = Command(self)
                                          
            if cmd.code==99: break
                   
            if cmd.code==1:
                res = cmd.getAddress(2)
                arg1 = cmd.getParam(0)
                arg2 = cmd.getParam(1)
                
                if debug:
                    print("[" + self.name + "] " + str(self.ip) + " - add " +  str(arg1) + ", " + str(arg2) + " --> " + str(res) + " - cmd:" + cmd.toString())
                                
                self.writeTo(res, arg1 + arg2)
                self.ip = self.ip + 4
                
            elif cmd.code==2:        
                res = cmd.getAddress(2)
                arg1 = cmd.getParam(0)
                arg2 = cmd.getParam(1)
                
                if debug:
                    print("[" + self.name + "] " + str(self.ip) + " - mul " +  str(arg1) + ", " + str(arg2) + " --> " + str(res) + " - cmd:" + cmd.toString())                
                                
                self.writeTo(res, arg1 * arg2)
                self.ip = self.ip + 4
                
                
            elif cmd.code==3: #Input   
                #Se gli input non sono sufficienti il metodo run esce e il programma si mette in pausa
                #Per risvegliarlo rilanciare run
                if self.ic < len(self.inputs):
                    arg1 = self.inputs[self.ic]
                    if debug:
                        print("[" + self.name + "] " + str(self.ip) + " input: " + str(arg1) + " - cmd:" + cmd.toString())                        
                    res = cmd.getAddress(0)
                    self.writeTo(res, arg1)
                    self.ic = self.ic + 1
                    self.ip = self.ip + 2
                else:
                    if debug:
                        print("[" + self.name + "] " + str(self.ip) + " is waiting for input.... " + "ic = " + str(self.ic))
                    pause = True

                
            elif cmd.code==4: #Output
                arg1 = cmd.getParam(0)                
                self.outputs.append(arg1)
                
                if debug:
                    print("[" + self.name + "] " + str(self.ip) + " output: " + str(arg1) + " - cmd:" + cmd.toString())                                     
                
                self.ip = self.ip + 2
                
            elif cmd.code==5: #jump-if-true
                arg1 = cmd.getParam(0)
                arg2 = cmd.getParam(1)
                                
                if debug:
                    print("[" + self.name + "] " + str(self.ip) + " - jump-if-true " +  str(arg1) +  " --> " + str(arg2) + " - cmd:" + cmd.toString())      
                
                if arg1 != 0:
                    self.ip =  arg2
                else:
                    self.ip = self.ip + 3
                    
            elif cmd.code==6: #jump-if-false
                arg1 = cmd.getParam(0)
                arg2 = cmd.getParam(1)
                
                if debug:
                    print("[" + self.name + "] " + str(self.ip) + " - jump-if-false " +  str(arg1) +  " --> " + str(arg2) + " - cmd:" + cmd.toString())   
                
                if arg1 == 0:
                    self.ip = arg2
                else:
                    self.ip = self.ip + 3
                    
            elif cmd.code==7: #less-then
                res = cmd.getAddress(2)                
                arg1 = cmd.getParam(0)
                arg2 = cmd.getParam(1)                
                
                if debug:
                    print("[" + self.name + "] " + str(self.ip) + " - less-then " +  str(arg1) + ", " + str(arg2) +  " --> " + str(res) + " - cmd:" + cmd.toString())        
                                
                if arg1 < arg2:            
                    self.writeTo(res, 1)
                else:
                    self.writeTo(res, 0)
                    
                self.ip = self.ip + 4
                    
            elif cmd.code==8: #equals
                arg1 = cmd.getParam(0)
                arg2 = cmd.getParam(1)                
                res = cmd.getAddress(2)
                
                if debug:
                    print("[" + self.name + "] " + str(self.ip) + " - equals " +  str(arg1) + ", " + str(arg2) +  " --> " + str(res) + " - cmd:" + cmd.toString())
                                
                if arg1 == arg2:            
                    self.writeTo(res, 1)
                else:
                    self.writeTo(res, 0)
                    
                self.ip = self.ip + 4
                
            elif cmd.code==9: #adjusts the relative base
                arg1 = cmd.getParam(0)
                self.relativeBase = self.relativeBase + arg1
                
                if debug:
                    print("[" + self.name + "] " + str(self.ip) + " - adjusts-relative-base " +  str(arg1) + " (relative base=" + str(self.relativeBase) + ")" + " - cmd:" + cmd.toString())
                
                self.ip = self.ip + 2
                
            else:
                print("Errore!")
                break;
                
        if not pause:
            self.ended = True
            
            
def loadFromFile(fileName, name="", inputs=None):
    f = open(fileName, "r")    
    progStr = f.read()
    f.close()      
    return Program(progStr, name, inputs)