#! /bin/env/pyhton3

import numpy as np
import matplotlib.pyplot as plt

N = 50
window = 3

x=np.linspace(0,100,N)
y=[]
for i in range(len(x)):
    y.append(np.random.rand())
somma_y = 0
for i in range(len(y)):
    somma_y = somma_y+y[i]

media_v = []
for i in range(len(y)):
    if i > 1 and i < N-1:
        print(f"i= {i}")
        media_v.append((y[i-1]+y[i]+y[i+1])/window)


print(f"media_v ha {len(media_v)} elementi")

plt.plot(x,y,'-*r',x[1:N-2],media_v)
plt.title('Un grafico')
plt.show()
