from src.img_process import img_process
from src.net_process import train, process, datagen
from src.img_cut import basic_cut,advance_cut

SRC_PATH = 'img'
DST_PATH = 'pre'
ASW_PATH = 'asw'
DAT_PATH = 'dat'

COLOR = True
CLASSES = 5

HEIGTH = 128
WIDTH = 128

TRAIN = '0001'
src_path = 'media/src_img/'+SRC_PATH+'-'+TRAIN+'.png'
dst_path = 'media/dst_img/'+DST_PATH+'-'+TRAIN+'.png'
asw_path = 'media/asn_img/'+ASW_PATH+'-'+TRAIN+'.png'
dat_path = 'media/dat_txt/'+DAT_PATH+'-'+TRAIN+'.txt'

# print(src_path)
# img_process(src_path,dst_path,asw_path,
#         full_color=COLOR,
#         classes=CLASSES,
#         size=(WIDTH,HEIGTH))
#
# datagen(src_path,asw_path,dat_path,CLASSES)
net = train("media/dat_txt/dat-"+TRAIN+".txt")

for i in range(1,10):
    num = str(i)
    num = '0'*(4-len(num))+num

    # process(net,"media/src_img/img-"+num+".png","media/net_img/img-"+num+".png")
    advance_cut("media/net_img/img-"+num+".png","media/cut-"+num+".png")
