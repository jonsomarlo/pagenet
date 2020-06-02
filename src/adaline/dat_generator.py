from PIL import Image

def dat_generator(src_path,ans_path,dst_path,classes):

    file = open(dst_path,"w")
    file.write("3 1\n")

    img_src = Image.open(src_path).convert('RGB')
    img_ans = Image.open(ans_path).convert('RGB')

    pxl_src = list(img_src.getdata())
    pxl_ans = list(img_ans.getdata())

    aux = classes-1
    for i in range(len(pxl_src)):
        for d in pxl_src[i]:
            file.write(str(d/255)+' ')
        file.write(str(pxl_ans[i][0]/aux)+'\n')
