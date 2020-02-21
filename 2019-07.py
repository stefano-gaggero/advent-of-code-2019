from itertools import permutations 
from threading import Thread
import time

"""
--- Day 7: Amplification Circuit ---

Based on the navigational maps, you're going to need to send more power to your ship's thrusters to reach Santa in time. To do this, you'll need to configure a series of amplifiers already installed on the ship.

There are five amplifiers connected in series; each one receives an input signal and produces an output signal. They are connected such that the first amplifier's output leads to the second amplifier's input, the second amplifier's output leads to the third amplifier's input, and so on. The first amplifier's input value is 0, and the last amplifier's output leads to your ship's thrusters.

    O-------O  O-------O  O-------O  O-------O  O-------O
0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
    O-------O  O-------O  O-------O  O-------O  O-------O

The Elves have sent you some Amplifier Controller Software (your puzzle input), a program that should run on your existing Intcode computer. Each amplifier will need to run a copy of the program.

When a copy of the program starts running on an amplifier, it will first use an input instruction to ask the amplifier for its current phase setting (an integer from 0 to 4). Each phase setting is used exactly once, but the Elves can't remember which amplifier needs which phase setting.

The program will then call another input instruction to get the amplifier's input signal, compute the correct output signal, and supply it back to the amplifier with an output instruction. (If the amplifier has not yet received an input signal, it waits until one arrives.)

Your job is to find the largest output signal that can be sent to the thrusters by trying every possible combination of phase settings on the amplifiers. Make sure that memory is not shared or reused between copies of the program.

For example, suppose you want to try the phase setting sequence 3,1,2,4,0, which would mean setting amplifier A to phase setting 3, amplifier B to setting 1, C to 2, D to 4, and E to 0. Then, you could determine the output signal that gets sent from amplifier E to the thrusters with the following steps:

    Start the copy of the amplifier controller software that will run on amplifier A. At its first input instruction, provide it the amplifier's phase setting, 3. At its second input instruction, provide it the input signal, 0. After some calculations, it will use an output instruction to indicate the amplifier's output signal.
    Start the software for amplifier B. Provide it the phase setting (1) and then whatever output signal was produced from amplifier A. It will then produce a new output signal destined for amplifier C.
    Start the software for amplifier C, provide the phase setting (2) and the value from amplifier B, then collect its output signal.
    Run amplifier D's software, provide the phase setting (4) and input value, and collect its output signal.
    Run amplifier E's software, provide the phase setting (0) and input value, and collect its output signal.

The final output signal from amplifier E would be sent to the thrusters. However, this phase setting sequence may not have been the best one; another sequence might have sent a higher signal to the thrusters.

Here are some example programs:

    Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):

    3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0

    Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):

    3,23,3,24,1002,24,10,24,1002,23,-1,23,
    101,5,23,23,1,24,23,23,4,23,99,0,0

    Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):

    3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
    1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0

Try every combination of phase settings on the amplifiers. What is the highest signal that can be sent to the thrusters?

Your puzzle answer was 929800.
--- Part Two ---

It's no good - in this configuration, the amplifiers can't generate a large enough output signal to produce the thrust you'll need. The Elves quickly talk you through rewiring the amplifiers into a feedback loop:

      O-------O  O-------O  O-------O  O-------O  O-------O
0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
   |  O-------O  O-------O  O-------O  O-------O  O-------O |
   |                                                        |
   '--------------------------------------------------------+
                                                            |
                                                            v
                                                     (to thrusters)

Most of the amplifiers are connected as they were before; amplifier A's output is connected to amplifier B's input, and so on. However, the output from amplifier E is now connected into amplifier A's input. This creates the feedback loop: the signal will be sent through the amplifiers many times.

In feedback loop mode, the amplifiers need totally different phase settings: integers from 5 to 9, again each used exactly once. These settings will cause the Amplifier Controller Software to repeatedly take input and produce output many times before halting. Provide each amplifier its phase setting at its first input instruction; all further input/output instructions are for signals.

Don't restart the Amplifier Controller Software on any amplifier during this process. Each one should continue receiving and sending signals until it halts.

All signals sent or received in this process will be between pairs of amplifiers except the very first signal and the very last signal. To start the process, a 0 signal is sent to amplifier A's input exactly once.

Eventually, the software on the amplifiers will halt after they have processed the final loop. When this happens, the last output signal from amplifier E is sent to the thrusters. Your job is to find the largest output signal that can be sent to the thrusters using the new phase settings and feedback loop arrangement.

Here are some example programs:

    Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):

    3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
    27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5

    Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):

    3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10

Try every combination of the new phase settings on the amplifier feedback loop. What is the highest signal that can be sent to the thrusters?

Your puzzle answer was 15432220.
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
