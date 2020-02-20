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