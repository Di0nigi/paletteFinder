import stats as st
import plotter as p
import finder as fd
import matplotlib.pyplot as plt

def main():
    img=[306,275,87,94,228,222]

    images=[]
    imagesName=[]

    data=p.parseData("data\\paletteData.txt")

    dataNames=p.parseNames("data\\names.txt")

    for elem in img:
        images.append(data[elem-1])
        imagesName.append(dataNames[elem-1])
    #print(images)
    
    for ind,im in enumerate(images):
        p.plotPaletteAndImage(im,imagesName[ind],borderThickness=10)
        p.saveGraph(100,f"ig/{ind}")
        p.ternaryPlot(im,marksize=100)
        p.saveGraph(300,f"ig/{ind}Ternary")



    




    return "done"

print(main())

