


class Adaline():

    def __init__(self,size,sesgo=1,alpha=0.1):
        self.s = sesgo
        self.a = alpha
        self.input, self.output = size
        self.weigth = [0.0]*(self.input+1) # PESOS INCIALES
        self.update = [0.0]*(self.input+1) # PESOS INCIALES

    def train(self,data,num_epocas=5,tol=0.1):
        def upd_weigth(old,new):
            return [old[i]+new[i] for i in range(len(old))]

        def y_in(input,weigth):
            return sum([input[i]*weigth[i] for i in range(len(weigth))])

        for input, target in data:
            input.append(self.s)

        end = []
        epocas = 0
        while epocas < num_epocas:
            epocas+=1

            updates = 0
            for input, target in data:
                sumout = y_in(self.weigth,input)
                output = sumout
                for i in range(len(input)):
                    self.update[i] = self.a*(target[0]-sumout)*input[i]

                self.weigth = upd_weigth(self.weigth,self.update)
                updates += sum([abs(u) for u in self.update])

            end.append(updates)
            if len(end)>1 and tol > abs(end[-2]-end[-1]):
                break

            print(epocas,updates)

    def process(self,input,umbral=0.5):
        def y_in(input,weigth):
            return sum([input[i]*weigth[i] for i in range(len(weigth))])

        sumout = y_in(self.weigth,input)
        output = 0 if sumout<umbral else 255
        return (output,output,output)
