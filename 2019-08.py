import numpy as np
import matplotlib.pyplot as plt

"""
--- Day 8: Space Image Format ---

The Elves' spirits are lifted when they realize you have an opportunity to reboot one of their Mars rovers, and so they are curious if you would spend a brief sojourn on Mars. You land your ship near the rover.

When you reach the rover, you discover that it's already in the process of rebooting! It's just waiting for someone to enter a BIOS password. The Elf responsible for the rover takes a picture of the password (your puzzle input) and sends it to you via the Digital Sending Network.

Unfortunately, images sent via the Digital Sending Network aren't encoded with any normal encoding; instead, they're encoded in a special Space Image Format. None of the Elves seem to remember why this is the case. They send you the instructions to decode it.

Images are sent as a series of digits that each represent the color of a single pixel. The digits fill each row of the image left-to-right, then move downward to the next row, filling rows top-to-bottom until every pixel of the image is filled.

Each image actually consists of a series of identically-sized layers that are filled in this way. So, the first digit corresponds to the top-left pixel of the first layer, the second digit corresponds to the pixel to the right of that on the same layer, and so on until the last digit, which corresponds to the bottom-right pixel of the last layer.

The image you received is 25 pixels wide and 6 pixels tall.

To make sure the image wasn't corrupted during transmission, the Elves would like you to find the layer that contains the fewest 0 digits. On that layer, what is the number of 1 digits multiplied by the number of 2 digits?

--- Part Two ---

Now you're ready to decode the image. The image is rendered by stacking the layers and aligning the pixels with the same positions in each layer. The digits indicate the color of the corresponding pixel: 0 is black, 1 is white, and 2 is transparent.

The layers are rendered with the first layer in front and the last layer in back. So, if a given position has a transparent pixel in the first and second layers, a black pixel in the third layer, and a white pixel in the fourth layer, the final image would have a black pixel at that position.

What message is produced after decoding your image?
"""

w = 25
h = 6

f = open("puzzle08.txt", "r")    
data = list(map(int, f.read().strip()))
f.close()

#Divide l'array monodimensionale data in un array di array monodimensionali contenenti ciascuno un layer
layers = np.array([data[i:i+w*h] for i in range(0, len(data), w*h)])

#Individua il layer con il minor numero di zeri
min_zeros_layer = -1
min = -1
k = 0
for l in layers:
    n_zeros = len(l[l==0])
    if n_zeros<min or min==-1:
        min = n_zeros
        min_zeros_layer = k
    k = k + 1

print("layer con meno zeri: " + str(k) + " (" + str(min) + ")")

#Elabora la risposta al primo quesito
layer = layers[min_zeros_layer]

print(len(layer[layer==1])*len(layer[layer==2]))


#Parte 2-----------------------------------------------------------------------

#reshape dei singoli layer nelle dimensioni h x w in modo da creare un immagine (righe x colonne)
images = np.array([np.reshape(l, (h, w)) for l in layers])

#Sovrappone i vari layer considerando che il pixel che vale 2 è trasparente
for img in reversed(images):
    img = np.ma.masked_equal(img, 2)  #Maschera i pixel==2 (traspaenti)
    plt.imshow(img)

plt.show()   #JYZHF


