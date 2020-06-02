from PIL import Image

from src.adaline.neuralnet import Adaline
from src.adaline.dat_generator import dat_generator

def datagen(src_path,asw_path,dat_path,CLASSES):
    return dat_generator(src_path,asw_path,dat_path,CLASSES)

def train(filename):

    neuralnet = Adaline((3,1),sesgo=1,alpha=0.1)

    try:
        weigth = open("net/weigth.txt","r").read().split()
        neuralnet.weigth = [float(w) for w in weigth]

    except Exception as e:
        trainfile = open(filename,"r").read().split('\n')
        input,output = [int(i) for i in trainfile[0].split()]

        data = []
        for line in trainfile[1:-1]:
            words = [float(i) for i in line.split()]
            data.append([words[:input],words[input:]])

        neuralnet.train(data,num_epocas=2000,tol=0.001)
        weigth = open("net/weigth.txt","w")
        for w in neuralnet.weigth:
            weigth.write(str(w)+' ')

    return neuralnet

def process(net,src_path,dst_path):
    umbral = 0.72

    img_src = Image.open(src_path).convert('RGB')
    pxl_src = list(img_src.getdata())

    white = 0
    black = 0
    for i in range(len(pxl_src)):
        result = net.process([c/255 for c in pxl_src[i]],umbral=umbral)
        if sum(result)==0:
            white+=1
        elif sum(result)==765:
            black+=1

    diff = 0 if white==0 else white/black
    umbral = abs(umbral+(diff-1)*0.05)
    if umbral > 1:
        umbral = 0.72

    pxl_net = []
    for i in range(len(pxl_src)):
        result = net.process([c/255 for c in pxl_src[i]],umbral=umbral)
        pxl_net.append(result)

    img_src.putdata(pxl_net)
    img_src.save(dst_path)
    print(dst_path)
