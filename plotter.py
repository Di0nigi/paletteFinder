import cv2 
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def parseData(path):
    out=[]

    with open(path, mode="r",encoding="utf-8") as f:
        for line in f:
            palette=[]
            line=line.replace("\n",'').split("|")[:-1]
            for elem in line:
                e = elem.split(" ")
                palette.append([int(e[0]),int(e[1]),int(e[2])])
            out.append(palette)
            #print(palette)
    return out

def parseNames(path):
    out=[]
    with open(path, mode="r",encoding="utf-8") as f:
        for line in f:
            line=line.replace("\n",'')
            out.append(line)

    return out

def writeMat(size,backColor=[0,0,0]):

    back=np.zeros(shape=size)+backColor



    return back

def drawColors(palettes,slotSize,colNum,backColor=[125,125,125],imageLike=None):

    colHeight=(len(palettes)//colNum) * slotSize[1]

    imwidth= slotSize[0] * 11 * colNum

    #for ind,palette in enumerate(palettes):
    #    palMat=[]
    #    colSlot=[]
    #    for col in palette:
    #        colSlot+= np.zeros(shape=slotSize)+col
    #        palMat.append(colSlot)
    #palMat=np.array(palMat)
    #plt.imshow(palMat)

    for ind in range(imwidth):
        for i in range(ind):
            pass


    return

def plotPalette(colors):
    palette = np.zeros((50, 300, 3), dtype=np.uint8)
    step = 300 // len(colors)
    for i, color in enumerate(colors):
        palette[:, i * step:(i + 1) * step, :] = color
    plt.imshow(palette)
    plt.axis("off")
    #plt.show()


def plotPalettes(listOfPalettes):

    nPalettes = len(listOfPalettes)
    height = 50 * nPalettes 
    width = 300


    combinedPalette = np.zeros((height, width, 3), dtype=np.uint8)


    for idx, colors in enumerate(listOfPalettes):
        step = width // len(colors)
        for i, color in enumerate(colors):
            combinedPalette[idx*50:(idx+1)*50, i*step:(i+1)*step, :] = color


    plt.imshow(combinedPalette)
    plt.axis("off")
    #plt.show()


def plotPalettesGrid(listOfPalettes, palettesPerColumn=10, colGap=20,borderThickness=10,borderColor=(0, 0, 0),backGround=[255,255,255]):
    nPalettes = len(listOfPalettes)
    paletteHeight = 50
    paletteWidth = 300

    
    nCols = (nPalettes + palettesPerColumn - 1) // palettesPerColumn  # ceiling division
    nRows = min(palettesPerColumn, nPalettes)

    

    canvasHeight = nRows * paletteHeight
    canvasWidth = nCols * paletteWidth + (nCols - 1) * colGap
    combinedPalette = np.zeros((canvasHeight, canvasWidth, 3), dtype=np.uint8)+backGround

    


    for idx, colors in enumerate(listOfPalettes):
        row = idx % palettesPerColumn
        col = idx // palettesPerColumn
        step = paletteWidth // len(colors)

        xOff = col * (paletteWidth + colGap)
        yOff = row * paletteHeight
        for i, color in enumerate(colors):
            combinedPalette[yOff:yOff + paletteHeight,
                            xOff + i*step:xOff + (i+1)*step, :] = color
    
    if borderThickness != 0:
        combinedPalette = addBorder(combinedPalette,borderThickness=borderThickness,borderColor=borderColor)


    plt.figure(figsize=(nCols * 3, nRows * 0.5))
    plt.imshow(combinedPalette)
    plt.axis("off")
    #plt.show()

def addBorder(img, borderColor=(0, 0, 0), borderThickness=5, palette=None):
    
    bordered = img.copy()
    t = borderThickness

    # top + bottom
    if palette == None:
        bordered[:t, :, :] = borderColor
        bordered[-t:, :, :] = borderColor
    else:
        if palette:
            bordered[:t//2, :, :] = borderColor
            bordered[-t:, :, :] = borderColor
        else:
            bordered[:t, :, :] = borderColor
            bordered[-t//2:, :, :] = borderColor
    
        
    # left + right
    bordered[:, :t, :] = borderColor
    bordered[:, -t:, :] = borderColor
    return bordered

def plotPaletteAndImage(colors, im, borderColor=(0, 0, 0), borderThickness=5):
    im=np.array(Image.open(im))
    imgHeight, imgWidth = im.shape[:2]
    paletteHeight = 300

    palette = np.zeros((paletteHeight, imgWidth, 3), dtype=np.uint8)
    step = imgWidth // len(colors)

    for i, color in enumerate(colors):
        startX = i * step
        endX = (i + 1) * step if i < len(colors) - 1 else imgWidth
        palette[:, startX:endX, :] = color

    imWithBorder = addBorder(im, borderColor, borderThickness,palette=False)
    paletteWithBorder = addBorder(palette, borderColor, borderThickness,palette=True)

    combined = np.vstack((imWithBorder, paletteWithBorder))

    plt.figure(figsize=(imgWidth/100, (imgHeight+paletteHeight)/100))
    plt.imshow(combined)
    plt.axis("off")
    #plt.show()

    return combined





def saveGraph(quality,name):
    plt.savefig(f"out\\{name}.png",dpi=quality)
    return



def main():

    data=parseData("data\\paletteData.txt")#[259]

    dataNames=parseNames("data\\names.txt")[259]
    #print(len(data))
    #print(len(dataNames))


    #plotPaletteAndImage(data,dataNames,borderThickness=10)
    #plotPalette(data)

    plotPalettesGrid(data,palettesPerColumn=50,backGround=[255,255,255],borderThickness=0)

    saveGraph(300,name="all palettes")
    #plt.show()
    

    return "done"

print(main())