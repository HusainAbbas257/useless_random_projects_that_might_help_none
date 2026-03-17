import math,time,os
size=10

wave=["" for i in range(size)]
def init(phase):
    global wave
    for i in range(size):
        wave[i]=' '*int((math.sin(phase)+1)*size/2)+'*'
        phase+=0.5

def printwave():
    t=time.time()
    while (time.time()-t<10):   
        init(time.time()%(2*math.pi))
        for part in wave:
            print(part)
        time.sleep(0.1)
        os.system('cls' )

if __name__=="__main__":
    printwave()

