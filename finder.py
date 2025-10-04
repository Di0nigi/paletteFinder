import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from PIL import Image
from sklearn.mixture import GaussianMixture

import plotter as p



import os


def extractPaletteKM(imagePath, nColors=5):
   
    image = cv2.imread(imagePath)

    image = cv2.GaussianBlur(image, (5,5), 0)
   # plt.imshow(image_bgr)
   # plt.axis("off")
   # plt.show()
   # image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
   # plt.imshow(image_rgb)
   # plt.axis("off")
   # plt.show()

    
    imageLab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

   # plt.imshow(image_lab)
   # plt.axis("off")
   # plt.show()

    pixels = imageLab.reshape(-1, 3)

    scaler = StandardScaler()
    pixels = scaler.fit_transform(pixels)

    idx = np.random.choice(len(pixels), size=10000, replace=False)
    sampledPixels = pixels[idx]

    #plt.imshow(sampledPixels)
    #plt.axis("off")
    #plt.show()


    kmeans = KMeans(n_clusters=nColors, random_state=42)
    kmeans.fit(sampledPixels)

    paletteLab = kmeans.cluster_centers_

    paletteLab= scaler.inverse_transform(paletteLab).astype("uint8")

    paletteLabImg = paletteLab[np.newaxis, :, :]  # shape (1, n_colors, 3)
    paletteRgbImg = cv2.cvtColor(paletteLabImg, cv2.COLOR_Lab2RGB)
    colorsRgb = paletteRgbImg[0]

    return colorsRgb


def extractPaletteGMM(imagePath, nColors=5):
    # Load and blur image
    image = cv2.imread(imagePath)
    image = cv2.GaussianBlur(image, (5,5), 0)

   

    
    #plt.imshow(image)
    #plt.show()

    imageLab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)


    pixels = imageLab.reshape(-1, 3)


    scaler = StandardScaler()
    pixels = scaler.fit_transform(pixels)


    idx = np.random.choice(len(pixels), size=10000, replace=False)
    sampledPixels = pixels[idx]

    gmm = GaussianMixture(n_components=nColors, random_state=42)
    gmm.fit(sampledPixels)

    paletteLab = gmm.means_

    paletteLab = scaler.inverse_transform(paletteLab).astype('uint8')


    # Convert to RGB for visualization
    paletteLabImg = paletteLab[np.newaxis, :, :] # shape (1, n_colors, 3)
    paletteRgbImg = cv2.cvtColor(paletteLabImg, cv2.COLOR_Lab2RGB)
    colorsRgb = paletteRgbImg[0]

    return colorsRgb










def dirToList(dirPath):

    l=os.listdir(dirPath)

    out=[]

    for elem in l:
        f= os.path.join(dirPath,elem)
        if os.path.isfile(f):
            out.append(f)


    return out

def savePaletteData(colorList,name):
    with open(name,mode="w",encoding="utf-8") as f:
        for elem in colorList:
            #l = list(elem)
            s=""
            for color in elem:
                s+=f"{color[0]} {color[1]} {color[2]} |"
            f.write(s+"\n")
    return

def saveNames(files,file):

    with open(file,mode="w",encoding="utf-8") as f:
        for elem in files:
            f.write(elem+"\n")


        return



def main():
    imgpath = "D:\\dionigi\\Desktop\\x100 prov\\edchives\\templateinstam90.jpg"  

    #images = dirToList("D:\\dionigi\\Desktop\\x100 prov\\edchives\\tutte")+dirToList("D:\\dionigi\\Desktop\\x100 prov\\edchives")
    #print(images)
    #saveNames(images,"data\\names.txt")
    allColors=[]
    
    nColors = 10

    images=[imgpath]

    for imageP in images:

        colors = extractPaletteKM(imageP, nColors)
        colors=sorted(colors,key= lambda x: (x[0],x[1],x[2]))
        allColors.append(colors)

    #p.plotPaletteAndImage(allColors[0],imgpath,borderThickness=10)
    
    #p.saveGraph(100,"sofPalette")
    #savePaletteData(allColors,"data\\paletteData.txt")
    #print(colors)
    #print(allColors)
    #p.plotPalettesGrid(allColors,40)
    
    #plotPalette(colors)
    #plt.show()
    #########
    return "done"


print(main())
