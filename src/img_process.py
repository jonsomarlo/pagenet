from PIL import Image

from src.knn.answer import answer

def img_process(path_src,path_dst,path_ans,
        path_pxl='media/pixel.png',
        path_cls='media/class.png',
        full_color=False,
        classes=10,
        size=(32,32)):

    img_src = Image.open(path_src)
    src_heigth, src_width = img_src.size
    new_heigth, new_width = size

    if not full_color:
        img_src = img_src.convert("L")

    img_src = img_src.resize((new_heigth,new_width))
    img_src.save(path_dst)

    img_pxl = img_src.resize((src_heigth,src_width))
    img_pxl.save(path_pxl)

    img_src = answer(img_src,path_ans,classes=classes)

    img_cls = img_src.resize((src_heigth,src_width))
    img_cls.save(path_ans)
