

def cores(data,min,max,classes,near=100,tol=5,start=[0,0,0]):

    # ordenamos todos los pixeles

    sort_data = []
    sort_data.append(sorted([d[0] for d in data]))
    sort_data.append(sorted([d[1] for d in data]))
    sort_data.append(sorted([d[2] for d in data]))

    # inciamos unos nucleos repartidos por todo el rango(min,max)
    if classes==1:
        spots = [start]
    else:
        spots = [[x,x,x] for x in range(min,max+1,(max-min)//(classes-1))]

    old_spots = [[abs(max-spots[0][0])]*3]*classes

    # mientras haya un cambio grande
    while tol < sum([abs(sum(old_spots[i])-sum(spots[i])) for i in range(classes)]):
        old_spots = [list(spots[i]) for i in range(classes)]

        for rgb in range(3):

            c = 0
            spots_nn = [[] for s in spots]

            for d in sort_data[rgb]:
                if c < classes and d > spots[c][rgb]:
                    c += 1

                if c > 0:
                    spots_nn[c-1].append(d)

                if c < classes:
                    spots_nn[c].append(d)

            for i in range(classes):
                aux = []
                for element in spots_nn[i]:
                    aux.append((abs(spots[i][rgb]-element),element))
                    if len(aux) > near:
                        aux.sort(reverse=True)
                        aux.pop(0)

                if len(aux)>0:
                    spots[i][rgb] = sum([a[1] for a in aux])//len(aux)
                else:
                    spots[i][rgb] = 0

    return spots


def reg(dots,lower,max,near=100,start=[0,0,0,0]):


    classes = len(dots)
    sel = []
    for i in range(classes):
        sel.append([])
        for dot in dots[i]:
            sel[i].append((abs(start[i]-dot[0]),dot))
            if len(sel[i]) > near:
                sel[i].sort(reverse=True)
                sel[i].pop(0)

    TIMES = 0
    line = [[0,0] for i in range(classes)]
    oldl = [[1,1] for i in range(classes)]
    while 1 < abs(sum([sum(line[i])-sum(oldl[i]) for i in range(classes)])) and TIMES<30:
        TIMES += 1
        oldl = [list(line[i]) for i in range(classes)]

        for i in range(classes):
            mx = 0; my = 0
            sxx = 0; sxy = 0
            for n,dot in sel[i]:
                x,y = dot
                mx += y
                my += x
                sxx += y*y
                sxy += x*y

            if len(sel[i])>0:
                mx /= len(sel[i])
                my /= len(sel[i])

                sxx = sxx/len(sel[i])-mx*mx
                sxy = sxy/len(sel[i])-mx*my

            if sxx > 0:
                line[i] = [sxy/sxx,my-(mx*sxy/sxx)]
            else:
                line[i] = [0,my]

        for i in range(classes):
            for n,d in sel[i]:
                diff = []

                if i//2 == 0:
                    v1,v2 = d
                else:
                    v1,v2 = reversed(d)

                for j in range(classes):
                    if j//2 == 0:
                        diff.append(int(abs(v2*line[j][0]+line[j][1]-v1)))
                    else:
                        diff.append(int(abs(v1*line[j][0]+line[j][1]-v2)))


                if diff.index(min(diff)) != i:
                    dots[i].remove(d)

            sel[i] = []
            for dot in dots[i]:
                pred = dot[0]*line[i][0]+line[i][1]
                sel[i].append((abs(pred-dot[0]),dot))
                if len(sel[i]) > near:
                    sel[i].sort(reverse=True)
                    sel[i].pop(0)

    return line,sel
