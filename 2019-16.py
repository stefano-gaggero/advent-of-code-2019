# -*- coding: utf-8 -*-
"""
--- Day 16: Flawed Frequency Transmission ---

You're 3/4ths of the way through the gas giants. Not only do roundtrip signals to Earth take five hours, but the signal quality is quite bad as well. You can clean up the signal with the Flawed Frequency Transmission algorithm, or FFT.

As input, FFT takes a list of numbers. In the signal you received (your puzzle input), each number is a single digit: data like 15243 represents the sequence 1, 5, 2, 4, 3.

FFT operates in repeated phases. In each phase, a new list is constructed with the same length as the input list. This new list is also used as the input for the next phase.

Each element in the new list is built by multiplying every value in the input list by a value in a repeating pattern and then adding up the results. So, if the input list were 9, 8, 7, 6, 5 and the pattern for a given element were 1, 2, 3, the result would be 9*1 + 8*2 + 7*3 + 6*1 + 5*2 (with each input element on the left and each value in the repeating pattern on the right of each multiplication). Then, only the ones digit is kept: 38 becomes 8, -17 becomes 7, and so on.

While each element in the output array uses all of the same input array elements, the actual repeating pattern to use depends on which output element is being calculated. The base pattern is 0, 1, 0, -1. Then, repeat each value in the pattern a number of times equal to the position in the output list being considered. Repeat once for the first element, twice for the second element, three times for the third element, and so on. So, if the third element of the output list is being calculated, repeating the values would produce: 0, 0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1.

When applying the pattern, skip the very first value exactly once. (In other words, offset the whole pattern left by one.) So, for the second element of the output list, the actual pattern used would be: 0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1, ....

After using this process to calculate each element of the output list, the phase is complete, and the output list of this phase is used as the new input list for the next phase, if any.

Given the input signal 12345678, below are four phases of FFT. Within each phase, each output digit is calculated on a single line with the result at the far right; each multiplication operation shows the input digit on the left and the pattern value on the right:

Input signal: 12345678

1*1  + 2*0  + 3*-1 + 4*0  + 5*1  + 6*0  + 7*-1 + 8*0  = 4
1*0  + 2*1  + 3*1  + 4*0  + 5*0  + 6*-1 + 7*-1 + 8*0  = 8
1*0  + 2*0  + 3*1  + 4*1  + 5*1  + 6*0  + 7*0  + 8*0  = 2
1*0  + 2*0  + 3*0  + 4*1  + 5*1  + 6*1  + 7*1  + 8*0  = 2
1*0  + 2*0  + 3*0  + 4*0  + 5*1  + 6*1  + 7*1  + 8*1  = 6
1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*1  + 7*1  + 8*1  = 1
1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*0  + 7*1  + 8*1  = 5
1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*0  + 7*0  + 8*1  = 8

After 1 phase: 48226158

4*1  + 8*0  + 2*-1 + 2*0  + 6*1  + 1*0  + 5*-1 + 8*0  = 3
4*0  + 8*1  + 2*1  + 2*0  + 6*0  + 1*-1 + 5*-1 + 8*0  = 4
4*0  + 8*0  + 2*1  + 2*1  + 6*1  + 1*0  + 5*0  + 8*0  = 0
4*0  + 8*0  + 2*0  + 2*1  + 6*1  + 1*1  + 5*1  + 8*0  = 4
4*0  + 8*0  + 2*0  + 2*0  + 6*1  + 1*1  + 5*1  + 8*1  = 0
4*0  + 8*0  + 2*0  + 2*0  + 6*0  + 1*1  + 5*1  + 8*1  = 4
4*0  + 8*0  + 2*0  + 2*0  + 6*0  + 1*0  + 5*1  + 8*1  = 3
4*0  + 8*0  + 2*0  + 2*0  + 6*0  + 1*0  + 5*0  + 8*1  = 8

--- Part Two -----------------------------------------------------------------

Now that your FFT is working, you can decode the real signal.

The real signal is your puzzle input repeated 10000 times. Treat this new signal as a single input list. Patterns are still calculated as before, and 100 phases of FFT are still applied.

The first seven digits of your initial input signal also represent the message offset. The message offset is the location of the eight-digit message in the final output list. Specifically, the message offset indicates the number of digits to skip before reading the eight-digit message. For example, if the first seven digits of your initial input signal were 1234567, the eight-digit message would be the eight digits after skipping 1,234,567 digits of the final output list. Or, if the message offset were 7 and your final output list were 98765432109876543210, the eight-digit message would be 21098765. (Of course, your real message offset will be a seven-digit number, not a one-digit number like 7.)

Here is the eight-digit message in the final output list after 100 phases. The message offset given in each input has been highlighted. (Note that the inputs given below are repeated 10000 times to find the actual starting input lists.)

    03036732577212944063491565474664 becomes 84462026.
    02935109699940807407585447034323 becomes 78725270.
    03081770884921959731165446850517 becomes 53553731.

After repeating your input signal 10000 times and running 100 phases of FFT, what is the eight-digit message embedded in the final output list?

"""

import math
import numpy as np
import time
import matplotlib.pyplot as plt


def processPhase(inp, nPhases=1):
    pattern = [0,1,0,-1]
    out = []
    li = len(inp)
    lp = len(pattern)
    
    pt = np.array([np.array([np.repeat(pattern, k+1) for i in range(0, math.ceil(li/(lp*(k+1)))+1)]).flatten()[1:li+1] for  k in range(0, li)])
    
    tmp = inp.copy()
    for i in range(0, nPhases): 
        out = [abs(x)%10 for x in np.matmul(pt, tmp)]
        tmp = out
    
    return out
           

#inp è la stringa di ingresso già troncata 
def processPhase2(inp, nPhases=1):
    li = len(inp)
    tmp = np.array(inp)
    out = []    
    for i in range(0, nPhases):
        out = np.fromiter((abs(np.sum(tmp[i:]))%10 for i in range(0, li)), count=li, dtype=int)
        tmp = out
    
    return out       


#Versione altamente ottimizzata di processPhase2 con l'uso di cumsum
#A cumulative sum is a sequence of partial sums of a given sequence. For example, the cumulative sums of the sequence {a,b,c,...}, are a, a+b, a+b+c, .... 
def processPhase2Opt(inp, nPhases=1):
    tmp = np.array(inp[::-1].copy())  #Array in ordine invertito per utilizzare cumsum
    out = []    
    for i in range(0, nPhases):
        out = np.cumsum(tmp)%10  
        tmp = out
    
    return out[::-1].copy()

    
def convertToList(inStr, repeat=1, offset=0):    
    l = len(inStr)
    n = math.floor((l*repeat-offset)/l)  #Numero di ripetizioni della lista intera 
    m = (l*repeat-offset)%l #elementi residui di inStr con cui iniziare
    out = [int(c) for c in inStr[(l-m):]]
    for i in range(0,n):
        out.extend([int(c) for c in inStr])
    return np.array(out, dtype=int)    
    

def getLastDigits(list, n, skip=0):
    return ''.join(map(str, list[skip:skip+n]))
            
   
#------------------------------------------------------------------------------
 
f = open("puzzle16.txt", "r")    
inStr = f.read()
f.close()


#inStr = "80871224585914546619083218645595"  #24176176 dopo 100 fasi
#inStr = "03036732577212944063491565474664" #Nella parte 2 da 84462026
#inStr = "02935109699940807407585447034323" #Nella parte 2 da 78725270
#inStr = "03081770884921959731165446850517" #Nella parte 2 da 53553731

inList1 = convertToList(inStr)
out = processPhase(inList1, 100)

print("1----> " + getLastDigits(out, 8)) #40921727

#Parte 2 --------------------------------------------------------------------
#Per il risultato finale (fase=100) interessano solo le cifre dalla 5.970.807 (è l'offset, 0 based) in poi su 6.500.000. 
#per il calcolo di tale cifra i primi 5.970.807 moltiplicatori per la fase precedente (fase=99) sono nulli
#Dunque interessano solo le cifre dalla 5.970.807 per la fase 99 e così via
#In pratica per qualunque offset, la cifra in offset dipende solo dalle cifre>offset della fase precedente
#Tra l'altro, per i casi dati, i moltiplicatori per tali cifre, dopo gli zeri, sono tutti 1
#Per la versione ottimizzata uso di cumsum!!!!

offs = int(str(inStr[:7]))
print("offs: " + str(offs))
inList2 = convertToList(inStr, 10000, offs)
print("Lunghezza segnale input troncato: " + str(len(inList2)))
print("E' possibile applicare l'approssimazione: " + str(offs>len(inList2)))

out = processPhase2Opt(inList2, 100)
end = time.time()
print("2----> " + getLastDigits(out, 8)) #89950138 

#out = processPhase2(inList2, 100)
#print("3----> " + getLastDigits(out, 8)) 
