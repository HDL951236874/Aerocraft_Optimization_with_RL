import main


# x,y,xt,yt,l1,V,l2,ny = main.main(9.81,0,10000,20/180,400,40000,10000,0,-100,100,15000,0,240,0,4,0,0,3)

import random
import time

"""
生成n个在low_b,到up_b之间的数据
"""
def init(n, low_b, up_b):
    S = []
    for i in range(n):
        S.append(random.randint(low_b, up_b))
    return S

"""

"""
def fitness(S):
    S_new = []
    for i in range(len(S)):
        S_new += [float(S[i])]*50
    num = main.main(9.81,0,10000,20/180,400,40000,10000,0,-100,100,15000,0,240,0,4,0,0,S_new)
    return num / 100


def crossover(ma, pa, k):
    off1 = ma[:k] + pa[k:]
    off2 = pa[:k] + ma[k:]
    return (off1, off2)


def mutation(S, low_b, up_b):
    n = len(S)
    ind = random.randint(0, n - 1)
    mark = random.randint(low_b, up_b)
    L = list(S)
    L[ind] = mark
    return L


def roulette(Population):
    pn = len(Population)
    line = [0.0]
    for i in range(pn):
        line.append(line[-1] + Population[i][1])
    total = float(line[-1])
    for i in range(pn):
        line[i + 1] /= total

    sel1 = random.random()
    sel2 = random.random()
    Parents = []
    for i in range(pn):
        if line[i] < sel1 <= line[i + 1]:
            Parents.append(Population[i][0])
        if line[i] < sel2 <= line[i + 1]:
            Parents.append(Population[i][0])
        if len(Parents) == 2:
            break
    return Parents


def GA(pn, maxiter, Pc, Pm, low_b, up_b):
    n = 25
    Population = []
    for i in range(pn):
        S = init(n, low_b, up_b)
        fit = fitness(S)
        print((S,fit))
        Population.append((S, fit))

    ite = 0
    while ite < maxiter:
        ite += 1
        for i in range(int(pn / 2)):
            if random.random() > Pc:
                ma, pa = roulette(Population)
                k = random.randint(1, n - 2)
                off1, off2 = crossover(ma, pa, k)
                if random.random() > Pm:
                    off1 = mutation(off1, low_b, up_b)
                    off2 = mutation(off2, low_b, up_b)
                Population.append((off1, fitness(off1)))
                Population.append((off2, fitness(off2)))

        Population.sort(key=lambda xx: xx[1])
        Population.reverse()
        Population = Population[:pn]
        Solutions = []
        # for i in range(pn):
        #     if Population[i][1] == n * (n - 1) / 2 and Population[i][0] not in Solutions:
        #         Solutions.append(Population[i][0])
        #     else:
        #         break
        # if len(Solutions) > 0:
        #     return (Solutions, ite)
        print(ite, Population[0])
    return Population[0], ite


t0 = time.time()
pn = 40
maxiter = 200
Pc = 0.4
Pm = 0.1
low_b = 2
up_b = 4
Solutions, k = GA(pn, maxiter, Pc, Pm, low_b, up_b)
t1 = time.time()
print ('After %d generations with %.3f seconds' % (k, t1 - t0))
print ('One solution is:', Solutions)
# k=[3.0]*1300
# max_v = 0
# ret = eng.daodan(k)
# print(ret)
