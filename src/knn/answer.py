from PIL import Image

from src.knn.cores import cores


def answer(image,path_dst,
        classes=4,
        near=100):

    image = image.convert('RGB')
    pxl_src = list(image.getdata())
    spots = cores(pxl_src,0,255,classes,near=near)

    pxl_new = []
    for pxl in pxl_src:

        dist = (255,0)
        for i in range(classes):

            aux = 0
            for rgb in range(3):
                aux += abs(spots[i][rgb]-pxl[rgb])

            aux = (aux,i)
            if aux < dist:
                dist = aux

        pxl_new.append((dist[1],dist[1],dist[1]))

    image.putdata(pxl_new)
    return image
