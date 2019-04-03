def oneinterp1(t1,t2):
    x,y=t1.shape
    if t2 <= t1[0, 0]:  #时间小于或者等于最小给定时间值
        j = 0

    if t2 > t1[x-1, 0]:  #时间大于最大给定时间值
        j = x - 2

    else:
        j=0
    while t2 > t1[j , 0]:
        j = j + 1
    W = t1[j, 1] + (t1[j, 1] - t1[j + 1, 1]) * (t2 - t1[j, 0]) / (t1[j, 0] - t1[j + 1, 0])
    return W

def oneinterp2(t1,t3,t4,t6):
    x,y=t3.shape
    if t4 <= t1[0]:  #攻角小于或者等于最小给定攻角值
        j = 0

    if t4 > t1[y-1]: #攻角大于最大给定攻角值
        j = y - 2
    else:
        j=0

        while t4 > t1[j+1]:
            j = j + 1

    W = t3[t6, j] + (t3[t6, j] - t3[t6, j + 1]) * (t4 - t1[j]) / (t1[j] - t1[j + 1])
    return W


def twointerp(arg1,arg2,arg3,arg4,arg5):
    m,n=arg3.shape
    #确定要用到哪二行马赫数
    if arg5 <= arg2[0]:  #马赫数小于或者等于最小给定马赫数
        i = 0

    if arg5 > arg2[m-1]:  #马赫数大于最大给定马赫数#
        i = m - 2
    else:
        i=0
    while arg5 > arg2[i+1]:
        i = i + 1

    fy1 = oneinterp2(arg1, arg3, arg4, i)
    fy2 = oneinterp2(arg1, arg3, arg4, i + 1)
    F = fy1 + (fy1 - fy2) * (arg5 - arg2[i]) / (arg2[i] - arg2[i + 1])
    return F