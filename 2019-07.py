from itertools import permutations 
from threading import Thread
import time

"""
Int Computer
"""

#-----------------------------------------------------------------------------

class Command:   
    code = 0;
    paramsMode = [0,0,0]
    ip = 0;
    program = []
    
    def __init__(self, program, ip):
        val = program[ip]
        self.code = val%100
        self.paramsMode[0] = (val%1000 - self.code)/100
        self.paramsMode[1] = (val%10000 - val%1000)/1000
        self.paramsMode[2] = (val%100000 - val%10000)/10000
        self.program = program
        self.ip = ip
        
    def getParam(self, idx):
        val = self.program[self.ip + idx + 1]
        if self.paramsMode[idx]==0:
            return self.program[val]
        else:
            return val
        
               
class Program:
          
    def __init__(self, progStr, name, inputs):         
        self.program = list(map(int, progStr.split(",")))
        self.name = str(name)
        self.inputs = inputs
        self.output = None
        self.ended = False
        self.ic = 0 #Contatore degli input
        self.ip = 0 
        self.ip0 = -1
        

    def addInput(self, val):
        self.inputs.append(val)
        
    def getOutput(self):
        return self.output
    
    def isEnded(self):
        return self.ended
    
    def run(self, debug=False):
        ip = self.ip 
        ip0 = self.ip0
        program = self.program
        pause = False
        while not pause:
            
            if(ip >= len(program)):
                break;
                
            if ip==ip0:
                print("Endless loop!")
                break
            ip0 = ip
            
            cmd = Command(program, ip)
                              
            if cmd.code==99: break
                   
            if cmd.code==1:
                res = program[ip+3]
                program[res] = cmd.getParam(0) + cmd.getParam(1)
                ip = ip + 4
                
            elif cmd.code==2:        
                res = program[ip+3]
                program[res] = cmd.getParam(0) * cmd.getParam(1)
                ip = ip + 4
                
                
            elif cmd.code==3: #Input   
                #Se gli input non sono sufficienti il metodo run esce e il programma si mette in pausa
                #Per risvegliarlo rilanciare run
                if self.ic < len(self.inputs):
                    arg1 = self.inputs[self.ic]
                    if debug:
                        print(self.name + " input: " + str(arg1))                        
                    res = program[ip+1]
                    program[res] = arg1                        
                    self.ic = self.ic + 1
                    ip = ip + 2
                else:
                    if debug:
                        print(self.name + " is waiting for input.... " + "ic = " + str(self.ic))
                    pause = True

                
            elif cmd.code==4: #Output
                res = cmd.getParam(0)
                self.output = res
                if debug:
                    print(self.name + " output: " + str(res))                                        
                ip = ip + 2
                
            elif cmd.code==5: #jump-if-true
                if cmd.getParam(0) != 0:
                    ip =  cmd.getParam(1)
                else:
                    ip = ip + 3
                    
            elif cmd.code==6: #jump-if-false
                if cmd.getParam(0) == 0:
                    ip = cmd.getParam(1)
                else:
                    ip = ip + 3
                    
            elif cmd.code==7: #less-then
                res = program[ip+3]
                if cmd.getParam(0) < cmd.getParam(1):            
                    program[res] = 1
                else:
                    program[res] = 0
                ip = ip + 4
                    
            elif cmd.code==8: #equals
                res = program[ip+3]
                if cmd.getParam(0) == cmd.getParam(1):            
                    program[res] = 1
                else:
                    program[res] = 0
                ip = ip + 4
                
            else:
                print("Errore!")
                break;
        if not pause:
            self.ended = True
        self.ip = ip
        self.ip0 = ip0-1
        self.program = program

        
#------------------------------------------------------------------------------    

#Genera tutte le permutazioni di n elementi (poteva essere vatti con una funzione integrata in numpy)
def getNextDigit(n, ns, idx):
    if idx == len(n): 
        #print("save " + str(n))        
        ns.append(n.copy())
        return 
    
    for i in range(0,5):
        if i not in n:
            n[idx] = i
            getNextDigit(n, ns, idx + 1)
        else:
            continue
    n[idx] = -1

def getPermutations():
    ns = []
    n = [-1, -1, -1 , -1, -1]
    getNextDigit(n, ns, 0)
    return ns

#Part 1 -----------------------------------------------------------------------

progStr = "3,8,1001,8,10,8,105,1,0,0,21,30,51,76,101,118,199,280,361,442,99999,3,9,102,5,9,9,4,9,99,3,9,102,4,9,9,1001,9,3,9,102,2,9,9,101,2,9,9,4,9,99,3,9,1002,9,3,9,1001,9,4,9,102,5,9,9,101,3,9,9,1002,9,3,9,4,9,99,3,9,101,5,9,9,102,4,9,9,1001,9,3,9,1002,9,2,9,101,4,9,9,4,9,99,3,9,1002,9,2,9,1001,9,3,9,102,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,99"

ns = getPermutations()

#Prova tutte le combinazioni di ingresso
max = 0
for n in ns:
    #print("Try " + str(n))
    out = 0
    for i in range(0,5):
        inp = [n[i], out]
        #print("Inputs : " + str(inp))
        prog = Program(progStr, "pippo", inp)
        prog.run()
        out = prog.getOutput()
        if out>max:
            max = out

    
        
print("Max output: " + str(max))

print("Part 2 ---------")

#Part 2 -----------------------------------------------------------------------

      

#-----------------------------------------------------------------------------      
#Qui per semplicità si usa questa funzione
#progStr = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
progStr = "3,8,1001,8,10,8,105,1,0,0,21,30,51,76,101,118,199,280,361,442,99999,3,9,102,5,9,9,4,9,99,3,9,102,4,9,9,1001,9,3,9,102,2,9,9,101,2,9,9,4,9,99,3,9,1002,9,3,9,1001,9,4,9,102,5,9,9,101,3,9,9,1002,9,3,9,4,9,99,3,9,101,5,9,9,102,4,9,9,1001,9,3,9,1002,9,2,9,101,4,9,9,4,9,99,3,9,1002,9,2,9,1001,9,3,9,102,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,99"
ns = list(permutations(range(5, 10))) 
N = 5
max = 0
maxSeq = []
for n in ns:
    progs = []
    for i in range(0,N):
        if i==0:
            p = Program(progStr, str(i), [n[i], 0]) 
            p.run()
        else:
            p = Program(progStr, str(i), [n[i]])    
        progs.append(p)


    stopStatus = False
    first = True
    while not stopStatus:        
        for i in range(0,N):
            if i==0 and first:
                first = False
                continue
            out = progs[(i-1)%N].getOutput()
            progs[i].addInput(out)
            progs[i].run(debug = False)
        stopStatus = progs[N-1].isEnded()
    
    res = progs[N-1].getOutput()
    if res > max:
        max = res
        maxSeq = n
        
    
        
print("Max output: " + str(max))
print("Max sequence: " + str(maxSeq))
