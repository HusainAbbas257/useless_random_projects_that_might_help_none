import math,time,os
size=40
speed=5
fps=30
amplitude=40
frequency=1.5
wave=["" for i in range(size)]
def init(phase):
    global wave
    for i in range(size):
        x = i/size
        y = (math.sin(phase + 2*math.pi*frequency*x)+1)*amplitude/2
        wave[i] = ' '*int(y) + '*'
def printwave(second):
    t=time.time()
    while (time.time()-t<=second):   
        init(time.time() * speed%(2*math.pi))
        for part in wave:
            print(part)
        time.sleep(1/fps)
        os.system('cls')

if __name__=="__main__":
    printwave(20)

