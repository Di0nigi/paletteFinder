import numpy as np
from skimage.color import rgb2lab 
import plotter as p
import matplotlib.pyplot as plt

def findKMostPopular(palettes,k,sensibility=4):
    res=[]

    for p1 in palettes:
        sim=0
        for p2 in palettes:
            p1C=clipEnds(p1)
            p2C=clipEnds(p2)
            #print(p1C)
            s=0
            for ind, col in enumerate(p1C):
                dE=compareCol(col,p2C[ind])
                if dE<=10:
                    s+=1
            if s>=sensibility:
                sim+=1
        res.append((p1,sim))

    res=sorted(res,key= lambda x: x[1],reverse=True)

    return res[0:k]

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
    palette = palette[1:-1]
    return palette

def flattenPalette(data):

    data=np.array(data)
    dF=np.reshape(data,shape=(data.shape[0]*data.shape[1],data.shape[2]))

    return dF

def averagePalette(data):

    data=np.array(data)

    out=data.mean(axis=1) 
    
    return out


def main():

    #p=[0,1,2,3,4,5,6,7,8,9]

    #print(clipEnds(p))
    data=p.parseData("data\\paletteData.txt")#[nPhoto]
    data2 = list(map(clipEnds,data))
    #data = averagePalette(data)
    data = list(map(clipEnds,data2))
    #print(data)
    data= flattenPalette(data)
    col=mostKcolors(data,k=len(data))

    p.plotColFreq(col)

    #print(col)
    #col = list(map(lambda x: x[0], col))
    
    #print(col)
    #p.plotPalette(col)
    #p.saveGraph(550,"ColorBarHD")
    plt.show()

    return "done"

if __name__ == "__main__":
    print(main())
    