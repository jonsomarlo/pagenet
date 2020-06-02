from PIL import Image

from src.knn.cores import reg


def basic_cut(src_path,dst_path):
    img_src = Image.open(src_path).convert('RGB')

    width, heigth = img_src.size
    pxl_src = list(img_src.getdata())

    pxl_mtx = []
    for i in range(0,len(pxl_src),width):
        pxl_mtx.append(pxl_src[i:i+width])

    white = 0
    black = 0

    dots = [[],[],[],[]]
    for h in range(1,heigth-1):
        for w in range(1,width-1):
            if sum(pxl_mtx[h][w])==0 and sum(pxl_mtx[h][w+1])==765:
                dots[0].append((w+1,w+1,w+1))
            elif sum(pxl_mtx[h][w])==0 and sum(pxl_mtx[h+1][w])==765:
                dots[1].append((h+1,h+1,h+1))
            elif sum(pxl_mtx[h][w-1])==765 and sum(pxl_mtx[h][w])==0:
                dots[2].append((w-1,w-1,w-1))
            elif sum(pxl_mtx[h-1][w])==765 and sum(pxl_mtx[h][w])==0:
                dots[3].append((h-1,h-1,h-1))

            if sum(pxl_mtx[h][w])==0:
                black += 1
            else:
                white += 1

    near = 1000
    left = cores(dots[0],0,width,1,near=near,start=[0,0,0])[0][0]
    right = cores(dots[2],0,width,1,near=near,start=[width,width,width])[0][0]
    top = cores(dots[1],0,heigth,1,near=near,start=[0,0,0])[0][0]
    bot = cores(dots[3],0,heigth,1,near=near,start=[heigth,heigth,heigth])[0][0]

    if left>right:
        left = 0
        right = width

    if top>bot:
        top = 0
        bot = heigth

    img_src = img_src.crop((left, top, right, bot))
    img_src.save(dst_path)
    print(dst_path)


def advance_cut(src_path,dst_path):
    img_src = Image.open(src_path).convert('RGB')

    width, heigth = img_src.size
    pxl_src = list(img_src.getdata())

    pxl_mtx = []
    for i in range(0,len(pxl_src),width):
        pxl_mtx.append(pxl_src[i:i+width])

    white = 0
    black = 0

    dots = [[],[],[],[]]
    sums = [0,0,0,0]
    for h in range(1,heigth-1):
        for w in range(1,width-1):
            if sum(pxl_mtx[h][w-1])==0 and sum(pxl_mtx[h][w])==765:
                dots[0].append((w,h))
                sums[0]+=w
            elif sum(pxl_mtx[h][w])==765 and sum(pxl_mtx[h][w+1])==0:
                dots[1].append((w,h))
                sums[1]+=w
            elif sum(pxl_mtx[h-1][w])==0 and sum(pxl_mtx[h][w])==765:
                dots[2].append((h,w))
                sums[2]+=h
            elif sum(pxl_mtx[h][w])==765 and sum(pxl_mtx[h+1][w])==0:
                dots[3].append((h,w))
                sums[3]+=h

            if sum(pxl_mtx[h][w])==0:
                black += 1
            else:
                white += 1

    COLOR_R = [(255,0,0),(0,255,0),(255,255,0),(0,0,255)]
    COLOR_D = [(255,0,0),(0,255,0),(255,255,0),(0,0,255)]
    BORDER = [True,False,True,False]
    for i in range(4):

        if len(dots[i]) > 0:
            xmid = sums[i]/len(dots[i])
            aux = []
            if BORDER[i]:
                for dot in dots[i]:
                    if dot[0]<xmid:
                        aux.append(dot)
            else:
                for dot in dots[i]:
                    if dot[0]>xmid:
                        aux.append(dot)
            dots[i] = aux


    near = 500
    direction, sels = reg(dots,0,width,near=near,start=[0,width,0,heigth])

    for i in range(4):
        for n,element in sels[i]:
            x,y = element
            for m in range(x-2,x+2):
                for n in range(y-2,y+2):
                    if i//2 != 0:
                        if n < width and m < heigth:
                            if n >= 0 and m >= 0:
                                pxl_mtx[m][n] = COLOR_D[i]
                    else:
                        if m < width and n < heigth:
                            if m >= 0 and n >= 0:
                                pxl_mtx[n][m] = COLOR_D[i]

    done = []
    corners = []
    for i in [0,2,1,3]:
        if i//2 != 1:
            for h in range(heigth-1,0,-1):
                w = int(h*direction[i][0]+direction[i][1])
                if w < width and h < heigth:
                    if w >= 0 and h >= 0:
                        pxl_mtx[h][w] = COLOR_R[i]
                        if (h,w) in done:
                            corners.append((h,w))
                        done.append((h,w))
        else:
            for w in range(width-1,0,-1):
                h = int(w*direction[i][0]+direction[i][1])
                if w < width and h < heigth:
                    if w >= 0 and h >= 0:
                        pxl_mtx[h][w] = COLOR_R[i]
                        if (h,w) in done:
                            corners.append((h,w))
                        done.append((h,w))

    if len(corners) == 4:
        print(corners)
    img_src.putdata([w for h in pxl_mtx for w in h])
    img_src.save(dst_path)
    print(dst_path)
