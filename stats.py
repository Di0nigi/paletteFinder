import numpy as np
from skimage.color import rgb2lab 

def findKMostPopular(palettes,k):

    
    return

def mostKcolors(colors, k):
    res=[]
    for col1 in colors:
        sim=0
        for col2 in colors:
            dE= compareCol(col1,col2)
            if dE<=5:
                sim+=1
        res.append((col1,sim-1))

    res=sorted(res,key= lambda x: x[1],reverse=True)

    return res[0:k]

def compareCol(col1, col2):
    col1 = np.array(col1, dtype=float) / 255
    col2 = np.array(col2, dtype=float) / 255

    lab1 = rgb2lab(col1.reshape(1, 1, 3))
    lab2 = rgb2lab(col2.reshape(1, 1, 3))

    dE = np.linalg.norm(lab1 - lab2)

    return dE

def clipEnds(palette):
    palette= palette[1:-1]
    return palette


def main():

    #p=[0,1,2,3,4,5,6,7,8,9]

    #print(clipEnds(p))


    return "done"

if __name__ == "__main__":
    print(main())
    