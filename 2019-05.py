"""
Int Computer
"""

program = "3,225,1,225,6,6,1100,1,238,225,104,0,2,106,196,224,101,-1157,224,224,4,224,102,8,223,223,1001,224,7,224,1,224,223,223,1002,144,30,224,1001,224,-1710,224,4,224,1002,223,8,223,101,1,224,224,1,224,223,223,101,82,109,224,1001,224,-111,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1102,10,50,225,1102,48,24,224,1001,224,-1152,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,1102,44,89,225,1101,29,74,225,1101,13,59,225,1101,49,60,225,1101,89,71,224,1001,224,-160,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1101,27,57,225,102,23,114,224,1001,224,-1357,224,4,224,102,8,223,223,101,5,224,224,1,224,223,223,1001,192,49,224,1001,224,-121,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,1102,81,72,225,1102,12,13,225,1,80,118,224,1001,224,-110,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,7,677,226,224,102,2,223,223,1005,224,329,101,1,223,223,108,226,226,224,102,2,223,223,1006,224,344,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,359,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,374,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,389,1001,223,1,223,107,677,226,224,1002,223,2,223,1005,224,404,101,1,223,223,8,226,677,224,102,2,223,223,1005,224,419,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,434,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,449,1001,223,1,223,107,226,226,224,1002,223,2,223,1006,224,464,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,479,1001,223,1,223,1008,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,7,677,677,224,102,2,223,223,1005,224,509,1001,223,1,223,108,677,226,224,102,2,223,223,1005,224,524,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,539,101,1,223,223,1108,677,677,224,102,2,223,223,1005,224,554,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,569,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,584,101,1,223,223,1107,226,226,224,102,2,223,223,1006,224,599,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,614,101,1,223,223,1008,677,226,224,1002,223,2,223,1005,224,629,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,644,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,659,101,1,223,223,1007,677,226,224,1002,223,2,223,1005,224,674,1001,223,1,223,4,223,99,226".split(",")
#program = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(",")
#program = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1".split(",")
#Oprogram = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(",")
program =  list(map(int, program))

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
        val = program[self.ip + idx + 1]
        if self.paramsMode[idx]==0:
            return self.program[val]
        else:
            return val
        
               
    
#-----------------------------------------------------------------------------

ip = 0
ip0 = -1
debug = True

while(True):
    
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
        if debug:
            print(str(ip) + " - add " +  str(cmd.getParam(0)) + ", " + str(cmd.getParam(1)) + " --> " + str(res)) 
            print(program[ip:ip+4])
        program[res] = cmd.getParam(0) + cmd.getParam(1)
        ip = ip + 4
        
    elif cmd.code==2:        
        res = program[ip+3]
        if debug:
            print(str(ip) + " - mul " +  str(cmd.getParam(0)) + ", " + str(cmd.getParam(1)) + " --> " + str(res))                
            print(program[ip:ip+4])
        program[res] = cmd.getParam(0) * cmd.getParam(1)
        ip = ip + 4
        
        
    elif cmd.code==3:        
        if debug:
            print(str(ip) + " - input --> " +  str(cmd.getParam(0)))                        
            print(program[ip:ip+2])
        arg1 = int(input("Input: "))
        res = program[ip+1]
        program[res] = arg1
        ip = ip + 2
        
    elif cmd.code==4:
        if debug:
            print(str(ip) + " - output " +  str(cmd.getParam(0)))                                
            print(program[ip:ip+2])
        print("---> " + str(cmd.getParam(0)))
        ip = ip + 2
        
    elif cmd.code==5: #jump-if-true
        if debug:
            print(str(ip) + " - jump-if-true " +  str(cmd.getParam(0)) +  " --> " + str(cmd.getParam(1)))        
            print(program[ip:ip+3])
        if cmd.getParam(0) != 0:
            ip =  cmd.getParam(1)
        else:
            ip = ip + 3
            
    elif cmd.code==6: #jump-if-false
        if debug:
            print(str(ip) + " - jump-if-false " +  str(cmd.getParam(0)) + " --> " + str(cmd.getParam(1)))        
            print(program[ip:ip+3])
        if cmd.getParam(0) == 0:
            ip = cmd.getParam(1)
        else:
            ip = ip + 3
            
    elif cmd.code==7: #less-then
        res = program[ip+3]
        if debug:
            print(str(ip) + " - less-then " +  str(cmd.getParam(0)) + ", " + str(cmd.getParam(1)) +  " --> " + str(res))        
            print(program[ip:ip+4])
        if cmd.getParam(0) < cmd.getParam(1):            
            program[res] = 1
        else:
            program[res] = 0
        ip = ip + 4
            
    elif cmd.code==8: #equals
        res = program[ip+3]
        if debug:
            print(str(ip) + " - equals " +  str(cmd.getParam(0)) + ", " + str(cmd.getParam(1)) +  " --> " + str(res))        
            print(program[ip:ip+4])
        if cmd.getParam(0) == cmd.getParam(1):            
            program[res] = 1
        else:
            program[res] = 0
        ip = ip + 4
        
    else:
        print("Errore!")
        break;
      
