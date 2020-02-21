"""
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle answer was 1048.
--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

    112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

How many different passwords within the range given in your puzzle input meet all of the criteria?

Your puzzle answer was 677.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, you should return to your Advent calendar and try another puzzle.

Your puzzle input was 246515-739105.
"""

def digits(num):
    numStr = str(num)
    return np.array(list(numStr)).astype("int")

i1 = 246515
i2 = 739105


k = 0
for i in range(i1, i2):
    ds = digits(i)
    d0 = 0
    double = False
    valid = True
    for d in ds:
        if d < d0: #Cifre decrescenti, non valido
            valid = False
            break
        elif d==d0: #c'è una cifra doppia
            double=True
        else: #ok, si prosegue
            d0 = d
    if valid and double:
        k = k + 1
      
print("Part 1: " + str(k))

#------------------------------------------------------------------------------

k = 0
for i in range(i1, i2):
    ds = digits(i)
    
    double = False    
    valid = True
    d0 = 0    
    doubleCount =1
    
    for d in ds:
        if d < d0: 
            valid = False
            break
        elif d==d0: #c'è una cifra doppia
            doubleCount = doubleCount + 1
        else: #ok, si prosegue
            d0 = d
            if doubleCount==2:
                double = True   #C'è una coppia esatta di cifre
            doubleCount = 1    
        
    #Se le ultime cifre sono una coppia esatta, il controllo va fatto anche fuori dal ciclo
    if doubleCount==2:
        double = True
        
    if valid and double:
        print(i)
        k = k + 1
        
print("Part 2: " + str(k))        