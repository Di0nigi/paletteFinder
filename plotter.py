import cv2 
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import ternary
import stats as st

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
    paletteHeight = 500

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


def ternaryPlot(colors):
   
    figure, tax = ternary.figure(scale=1.0)
    tax.boundary(linewidth=1.5)
    tax.gridlines(multiple=0.2, color="gray")  # every 20%
    tax.ticks(axis='lbr', multiple=0.2, linewidth=1)

    tax.left_axis_label("Green (0–255)")
    tax.right_axis_label("Blue (0–255)")
    tax.bottom_axis_label("Red (0–255)")

    rgb=np.array([[255,0,0],[0,255,0],[0,0,255]])

    colors=np.concat([rgb,colors])
    colors=sorted(colors,key= lambda x: x[0]+x[1]+x[2])


    colors2=normPalette(colors)

    for ind, (r, g, b) in enumerate(colors2):
        tax.scatter(
            [(r, g, b)],
            marker="o",
            color=[colors[ind]/255], 
            s=50,
            edgecolors="black",       
            linewidths=0,
        )
    tax.clear_matplotlib_ticks()
    #tax.show()

    return 

def normPalette(colors):
    normPalette=[]
    for elem in colors:
        elem = np.array(elem,dtype=float)
        elem = elem /np.sum(elem) 
        normPalette.append(elem)
    
    return normPalette

def plotColFreq(colorsAndFreq):

    #colors=sorted(colorsAndFreq,key= lambda x: x[0]+x[1]+x[2] (lambda y: y[0]) )

    col = list(map(lambda x: x[0], colorsAndFreq))

    col = sorted(col,key= lambda x: x[0]+x[1]+x[2])

    
    barColors= list(map(lambda x: x/255, col))
    #print(barColors)

    colLabel= list(map(lambda x: f"{x}", col))

    freq = list(map(lambda x: x[1], colorsAndFreq))

    plt.bar(colLabel, freq,color=barColors,edgecolor='none')
    plt.title('Bar Plot of Color Frequency')
    plt.xlabel('Colors')
    plt.ylabel('Frequency')
    plt.xticks([])

    return






def main():

    nPhoto=259

    data=parseData("data\\paletteData.txt")[nPhoto]

    dataNames=parseNames("data\\names.txt")[nPhoto]
    #print(len(data))
    #print(len(dataNames))

    #plot_palette_histogram(data)[0]

    
    #ternaryPlot([[255,255,0]])
    #plt.show()

    
    #dF = st.flattenData(data)
    #print(dF[0:1100])
    #ternaryPlot(dF)
    #saveGraph(400,"colorDistrib")

    #print(data)




    #plotPaletteAndImage(data,dataNames,borderThickness=10)
    #plotPalette(data)

    #plotPalettesGrid(data,palettesPerColumn=70,backGround=[255,255,255],borderThickness=0)

    #saveGraph(500,name="allPalettes")
    #plt.show()
    #ternaryPlot(data)

    return "done"

if __name__ == "__main__":
    print(main())