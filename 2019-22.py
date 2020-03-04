# -*- coding: utf-8 -*-
"""
--- Day 22: Slam Shuffle ---

There isn't much to do while you wait for the droids to repair your ship. At least you're drifting in the right direction. You decide to practice a new card shuffle you've been working on.

Digging through the ship's storage, you find a deck of space cards! Just like any deck of space cards, there are 10007 cards in the deck numbered 0 through 10006. The deck must be new - they're still in factory order, with 0 on the top, then 1, then 2, and so on, all the way through to 10006 on the bottom.

You've been practicing three different techniques that you use while shuffling. Suppose you have a deck of only 10 cards (numbered 0 through 9):

To deal into new stack, create a new stack of cards by dealing the top card of the deck onto the top of the new stack repeatedly until you run out of cards:

Top          Bottom
0 1 2 3 4 5 6 7 8 9   Your deck
                      New stack

  1 2 3 4 5 6 7 8 9   Your deck
                  0   New stack

    2 3 4 5 6 7 8 9   Your deck
                1 0   New stack

      3 4 5 6 7 8 9   Your deck
              2 1 0   New stack

Several steps later...

                  9   Your deck
  8 7 6 5 4 3 2 1 0   New stack

                      Your deck
9 8 7 6 5 4 3 2 1 0   New stack

Finally, pick up the new stack you've just created and use it as the deck for the next technique.

To cut N cards, take the top N cards off the top of the deck and move them as a single unit to the bottom of the deck, retaining their order. For example, to cut 3:

Top          Bottom
0 1 2 3 4 5 6 7 8 9   Your deck

      3 4 5 6 7 8 9   Your deck
0 1 2                 Cut cards

3 4 5 6 7 8 9         Your deck
              0 1 2   Cut cards

3 4 5 6 7 8 9 0 1 2   Your deck

You've also been getting pretty good at a version of this technique where N is negative! In that case, cut (the absolute value of) N cards from the bottom of the deck onto the top. For example, to cut -4:

Top          Bottom
0 1 2 3 4 5 6 7 8 9   Your deck

0 1 2 3 4 5           Your deck
            6 7 8 9   Cut cards

        0 1 2 3 4 5   Your deck
6 7 8 9               Cut cards

6 7 8 9 0 1 2 3 4 5   Your deck

To deal with increment N, start by clearing enough space on your table to lay out all of the cards individually in a long line. Deal the top card into the leftmost position. Then, move N positions to the right and deal the next card there. If you would move into a position past the end of the space on your table, wrap around and keep counting from the leftmost card again. Continue this process until you run out of cards.

For example, to deal with increment 3:


0 1 2 3 4 5 6 7 8 9   Your deck
. . . . . . . . . .   Space on table
^                     Current position

Deal the top card to the current position:

  1 2 3 4 5 6 7 8 9   Your deck
0 . . . . . . . . .   Space on table
^                     Current position

Move the current position right 3:

  1 2 3 4 5 6 7 8 9   Your deck
0 . . . . . . . . .   Space on table
      ^               Current position

Deal the top card:

    2 3 4 5 6 7 8 9   Your deck
0 . . 1 . . . . . .   Space on table
      ^               Current position

Move right 3 and deal:

      3 4 5 6 7 8 9   Your deck
0 . . 1 . . 2 . . .   Space on table
            ^         Current position

Move right 3 and deal:

        4 5 6 7 8 9   Your deck
0 . . 1 . . 2 . . 3   Space on table
                  ^   Current position

Move right 3, wrapping around, and deal:

          5 6 7 8 9   Your deck
0 . 4 1 . . 2 . . 3   Space on table
    ^                 Current position

And so on:

0 7 4 1 8 5 2 9 6 3   Space on table

Positions on the table which already contain cards are still counted; they're not skipped. Of course, this technique is carefully designed so it will never put two cards in the same position or leave a position empty.

Finally, collect the cards on the table so that the leftmost card ends up at the top of your deck, the card to its right ends up just below the top card, and so on, until the rightmost card ends up at the bottom of the deck.

The complete shuffle process (your puzzle input) consists of applying many of these techniques. Here are some examples that combine techniques; they all start with a factory order deck of 10 cards:

deal with increment 7
deal into new stack
deal into new stack
Result: 0 3 6 9 2 5 8 1 4 7

cut 6
deal with increment 7
deal into new stack
Result: 3 0 7 4 1 8 5 2 9 6

deal with increment 7
deal with increment 9
cut -2
Result: 6 3 0 7 4 1 8 5 2 9

deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
Result: 9 2 5 8 1 4 7 0 3 6

Positions within the deck count from 0 at the top, then 1 for the card immediately below the top card, and so on to the bottom. (That is, cards start in the position matching their number.)

After shuffling your factory order deck of 10007 cards, what is the position of card 2019?

Your puzzle answer was 7545.


--- Part Two ---

After a while, you realize your shuffling skill won't improve much more with merely a single deck of cards. You ask every 3D printer on the ship to make you some more cards while you check on the ship repairs. While reviewing the work the droids have finished so far, you think you see Halley's Comet fly past!

When you get back, you discover that the 3D printers have combined their power to create for you a single, giant, brand new, factory order deck of 119315717514047 space cards.

Finally, a deck of cards worthy of shuffling!

You decide to apply your complete shuffle process (your puzzle input) to the deck 101741582076661 times in a row.

You'll need to be careful, though - one wrong move with this many cards and you might overflow your entire ship!

After shuffling your new, giant, factory order deck that many times, what number is on the card that ends up in position 2020?
"""

"""
-------------------------------------------------------------
Nota per "deal with argument":
    
c'[i] = c[x] con x t.c. nx%N = i

Dunque occorre risolvere l'equazione  n x = i (mod N), in quanto sicuramente i<N

Nota: tale equazione ha soluzione solo se n e N sono primi tra loro 
ref: https://www.expii.com/t/solving-linear-congruence-ax-b-mod-n-3389

Indicando con m l'inverso moltiplicativo di n, ovvero m t.c.  m n = 1 (mod N), moltiplicando per m si ha che:
    
x = i * m (mod N)

Ad esempio l'inverso moltiplicativo di 3 (mod 10) è 7, dunque:
    
    x = i*7 (mod N)
    
    i=0 --> x=0
    i=1 --> x=7
    i=2 --> x=4
    ....
    
"""

import numpy as np
import re
import sympy as sym
import math

class ShuffleVM:

    CUT = 1
    DEAL_NEW_STACK = 2
    DEAL_WITH_INCREMENT = 3
    
    #Restituisce un dictionary con gli inversi moltiplicativi di tutti i parametri delle istruzioni DEAL_WITH_INCREMENT del programma 
    @staticmethod
    def getMultiplicativeInverse(N, n):
        for i in range(1, n):            
            if (i*N+1)%n==0:
                return int((i*N+1)/n)
    
    def __init__(self, fileName, N, cards=None):
        self.fileName = fileName
        self.N = N
        self.cards = cards

    def dealNewStack(self):
        # c'[x] = c[N-x-1]
        self.cards = [self.cards[self.N-i-1] for i in range(0, self.N)]
    
    def cut(self, n):    
        # c'[x] = c[ (x+n)%N ]
        self.cards = [self.cards[(i+n)%self.N] for i in range(0, self.N)]
    
    def dealWithIncrement(self, mulInv):  
        # c'[i] = c[x] con x t.c. nx%N = i
        self.cards = [self.cards[i*mulInv%self.N] for i in range(0, self.N)]

    #------
        
    def reverseDealIntoNewStack(self, d):
        return self.N-d-1
    
    def reverseCut(self, n,  d):
        return d + n
    
    def reverseDealWithArgument(self, mulInv, d):
        return int(d*mulInv)   #int() serve per evitare l'overflow

    
    #-------
            
    def execute(self):
        for i in range(0, len(self.program), 2):
            inst = self.program[i]    
            if inst==ShuffleVM.DEAL_NEW_STACK:
                self.dealNewStack()
                
            elif inst==ShuffleVM.CUT:            
                self.cut(self.program[i+1])

            elif inst==ShuffleVM.DEAL_WITH_INCREMENT: 
                self.dealWithIncrement(self.program[i+1])
        
    
    def executeInverse(self, d):
        for i in range(len(self.program)-2, -1, -2):
            inst = self.program[i]    
            if inst==ShuffleVM.DEAL_NEW_STACK:
                d = self.reverseDealIntoNewStack(d)
                
            elif inst==ShuffleVM.CUT:            
                d = self.reverseCut(self.program[i+1], d)
                
            elif inst==ShuffleVM.DEAL_WITH_INCREMENT: 
                d = self.reverseDealWithArgument(self.program[i+1], d)
                            
        return d%self.N

    
    def compile(self):
        self.program = []
        reg = re.compile("^([A-Za-z ]+) ?([-0-9]+)?$")
        with open(self.fileName, "r") as f:
            for line in f:                
                match = reg.match(line)
                if not match:
                    print("Errore: " + line)
                    continue
                
                cmd = match.group(1)
                
                if cmd.find("deal into new stack") != -1:
                    self.program.append(ShuffleVM.DEAL_NEW_STACK)
                    self. program.append(0)
                    
                elif cmd.find("cut") != -1:            
                    val = int(match.group(2))
                    if val<0: val = self.N + val  #Ininfluente
                    self.program.append(ShuffleVM.CUT)
                    self.program.append(val)
                    
                elif cmd.find("deal with increment") != -1:
                    val = int(match.group(2))
                    self.program.append(ShuffleVM.DEAL_WITH_INCREMENT)
                    self.program.append(ShuffleVM.getMultiplicativeInverse(self.N, val))


    def getExpression(self):
        res = "x"
        for i in range(0, len(self.program), 2):
            inst = self.program[i]    
            if inst==ShuffleVM.DEAL_NEW_STACK:
                val = "(" + str(self.N-1) + "-x)"
                
            elif inst==ShuffleVM.CUT:            
                val = "(x+" + str(self.program[i+1]) + ")"
                
            elif inst==ShuffleVM.DEAL_WITH_INCREMENT:                 
                val = str(self.program[i+1]) + "*x"

            res = res.replace("x", val)                
                
            #r = eval(res,{'x':1})
            #print(str(i) + "-->" + str(r%self.N) + " " + res)
        return res


# Function to find modulo inverse of b. It returns  
# -1 when inverse doesn't  
# modInverse works for prime m 
#Nettamente più efficiente di quella implementata nella classe ShuffleVM
def modInverse(b,m): 
    g = math.gcd(b, m)  
    if (g != 1): 
        # print("Inverse doesn't exist")  
        return -1
    else:  
        # If b and m are relatively prime,  
        # then modulo inverse is b^(m-2) mode m  
        return pow(b, m - 2, m)        

# Iterative Function to calculate 
# (x^y)%p in O(log y)          
def power(x, y, p) : 
    res = 1     # Initialize result 
    # Update x if it is more 
    # than or equal to p 
    x = x % p  
    while (y > 0) :          
        # If y is odd, multiply 
        # x with result 
        if ((y & 1) == 1) : 
            res = (res * x) % p   
                
        # y must be even now 
        y = y >> 1      # y = y/2 
        x = (x * x) % p          
    return res 


#Attenzione: la divisione modulare richiede di calcolare l'inverso moltiplicativo
# (1 - power(a, r, N)) // (1-a) non funziona!
#Al limite (1 - pow(a, r) // (1-a), ma per grandi a e r va in out-of-memory
#NOTA: potevo usare la funzione built-in pow()
def iterate(a, b, N, d, r):
    inv = modInverse((1-a), N)
    k5 = (1 - power(a, r, N)) *inv
    y = power(a, r, N)*d + b*(k5%N)
    return y%N


#Parte 1------------------------------------------------------------------    

N = 10007
cards = list(range(0,N))

vm = ShuffleVM("puzzle22.txt", N, cards)
vm.compile()
vm.execute()

idx = np.nonzero(np.array(vm.cards)==2019)[0][0]
print("1a--->" + str(idx)) #Metodo diretto con tutto il mazzo di carte (7545)

d = vm.executeInverse(idx)
print("1r---->" + str(d))  #Metodo inverso con solo la carta di interesse


print("Test con equazione ----------------------------")
esp = vm.getExpression()
x = sym.symbols('x')
p = sym.Poly(esp, x)
coeffs = p.coeffs()
esp2 = str(coeffs[0]%N) + "*x + " + str(coeffs[1]%N)
print("Equazione: " + esp2)

d = eval(esp2,{'x': idx})
print("1e---->" + str(d%N))   #Metodo con equazione

print("Test iterazioni ----------------------------")

#r iterazioni
d = 2020
r = 10
cards = list(range(0,N))
vm = ShuffleVM("puzzle22.txt", N, cards)
vm.compile()
for i in range(0,r):
    vm.execute()    
print("1 iter a --->" + str(vm.cards[2020])) 

#---
d1 = d
for i in range(0,r):
    d1 = vm.executeInverse(d1)      
print("1 iter r --->" + str(d1))     

#---
a = 288
b = 578
print("1 iter e1 --->" + str(iterate(a, b, N, d, r)))


print("Parte 2 ----------------------------------")

#Part 2-----------------------------------------------------------------------

N = 119315717514047
r = 101741582076661
d = 2020

vm2 = ShuffleVM("puzzle22.txt", N)
vm2.compile()
esp = vm2.getExpression()
x = sym.symbols('x')
p = sym.Poly(esp, x)
coeffs = p.coeffs()
esp2 = str((coeffs[0])%N) + "*x + " + str(coeffs[1]%N)
print("Equazione: " + esp2)  # 26783713188704*x + 28044338282903

a = 26783713188704
b = 28044338282903
print("2a---->" + str(iterate(a, b, N, d, r)))   #12706692375144
