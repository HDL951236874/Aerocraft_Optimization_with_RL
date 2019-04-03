import math
import  numpy as np
import RL_GA.aero_parameter
import RL_GA.interp
#很坑的全局变量
# g=parameter.g
# Tp1=parameter.Tp1#发动机工作时间
# P1=parameter.P1 #推力
# Ip1=parameter.Ip1  #比冲

def interpolation(t,S,vt,Tp1,P1,K):


    v = S[0]
    theta = S[1]
    x = S[2]
    y = S[3]
    m = S[4]
    thetat = S[5]
    xt = S[6]
    yt = S[7]

    vtx = vt* math.cos(thetat)
    vty = vt* math.sin(thetat)

    #很坑的Parameter()
    AE = 0.01745329
    Aan = np.array([0 ,4 ,8 ,12 ,16 ,20 ,24 ,28 ,32 ,36 ,40 ,44])* AE
    Aax = np.array([0  ,4 , 8  ,12  ,16 , 20 , 30 , 40  ,45]) * AE
    AMa = np.array([0.4 , 0.9 , 1.2 , 2 , 3 , 4 , 5])
    AMa_CX = np.array([0.1  ,   0.4  ,0.9 , 1 , 1.2 , 2  ,3 , 4  ,  5])
    AH = np.array([0 , 15 , 30 , 35 , 40]) * 1000
    ACX = np.array([[0.42  ,  0.37  ,  0.42  ,  0.72  ,  0.63  ,  0.44  ,  0.34  ,  0.28  ,  0.24],
                    [0.43  ,  0.37  ,  0.44  ,  0.74  ,  0.64  ,  0.45  ,  0.36  ,  0.31  ,  0.27],
                    [0.40  ,  0.35  , 0.45  ,  0.75  ,  0.66  ,  0.48  ,  0.39  ,  0.33   , 0.29],
                    [0.36  ,  0.31  ,  0.44  ,  0.78  ,  0.69  ,  0.52  ,  0.41  ,  0.35   , 0.32],
                    [0.31  ,  0.26  ,  0.41  ,  0.80  ,  0.70  ,  0.50  ,  0.42  ,  0.37   , 0.35],
                    [0.26  ,  0.20  ,  0.47  ,  0.78  ,  0.69  ,  0.48  ,  0.45   , 0.41   , 0.40],
                    [0.28  ,  0.23  ,  0.44  ,  0.73  ,  0.64  ,  0.50  ,  0.51   , 0.51   , 0.51],
                    [0.24  ,  0.19  ,  0.19  ,  0.74  ,  0.65  ,  0.54  ,  0.57   , 0.58  ,  0.59],
                    [0.13  ,  0.08   , 0.09  ,  0.68  ,  0.58   , 0.55  ,  0.57  ,  0.62  ,  0.63]]).T#轴向力系数

    ACXH = np.array([[0.00  ,  0.00  ,  0.00  ,  0.00  ,  0.00  ,  0.00  ,  0.00  ,  0.00  ,  0.00],
            [0.06  ,  0.05  ,  0.05 ,   0.04  ,  0.05  ,  0.05  ,  0.04  ,  0.04  ,  0.03],
            [0.21  ,  0.19  ,  0.16  ,  0.14  ,  0.14  ,  0.13  ,  0.11  ,  0.09   , 0.07],
            [0.25  ,  0.23  ,  0.19  ,  0.17  ,  0.16  ,  0.15  ,  0.13  ,  0.11  ,  0.09],
            [0.37  ,  0.30  ,  0.25  ,  0.22  ,  0.21  ,  0.19  ,  0.15  ,  0.13  ,  0.10]]).T#轴向力高度修正

    ACXnac =np.array([0.10  ,  0.10  ,  0.19  ,  0.19  ,  0.19  ,  0.13  ,  0.08  ,  0.06  , 0.04])#被动段底阻系数
    ACN =np.array( [[0.00 ,   0.71  ,  1.61  ,  2.61  ,  3.46 ,   4.71 , 5.99 , 6.86  ,  7.71 ,   8.59  ,  9.26  ,  9.64],
           [0.00  ,  0.77  ,  1.75  ,  2.87  ,  3.85   , 5.08  , 6.51  ,  7.79  ,  9.01   , 10.21   , 11.45 ,   12.25],
           [0.00 ,   0.80  ,  1.85   , 2.97  ,  3.99  ,  5.25  , 6.70  ,  8.21  ,  9.74  ,  11.28   , 12.91  ,  14.58],
          [ 0.00  ,  0.76  ,  1.68  ,  2.63  ,  3.65  ,  5.02  , 6.51 ,   8.05 ,   9.62 ,   11.21 ,   12.75  ,  14.18],
           [0.00  ,  0.71  ,  1.50  ,  2.32  ,  3.29  ,  4.49  , 5.74  ,  7.05  ,  8.44 ,   9.92  ,  11.48  ,  13.16],
           [0.00  ,  0.63  ,  1.34  ,  2.13  ,  3.02  ,  4.08  , 5.23  ,  6.46  ,  7.81 ,   9.28  ,  10.89  ,  12.82],
           [0.00  ,  0.57  ,  1.22  ,  1.97  ,  2.83  ,  3.82  , 4.93  ,  6.13  ,  7.47 ,   8.95  ,  10.61  ,  12.49]]) #法向力系数
    AXD =np.array([[0.52  ,  0.55   , 0.58  ,  0.59  ,  0.56  ,  0.58 , 0.59  ,  0.56   , 0.55  ,  0.55  ,  0.56  ,  0.56],
          [ 0.55  ,  0.56  ,  0.59  ,  0.59  ,  0.57  ,  0.57  , 0.59  ,  0.59 ,   0.58 ,   0.56 ,   0.55 ,   0.53],
           [0.52  ,  0.56  ,  0.59  , 0.59  ,  0.57  ,  0.58 ,  0.58  ,  0.57  ,  0.57  ,  0.56  ,  0.56  ,  0.57],
           [0.49  ,  0.53  ,  0.56 ,   0.55  ,  0.54  ,  0.56  , 0.57   , 0.57   , 0.58  ,  0.58  ,  0.58  ,  0.58],
           [0.52  ,  0.53 ,   0.54  ,  0.53  ,  0.54   , 0.55  , 0.56  ,  0.56 ,   0.57  ,  0.57 ,   0.58   , 0.59],
           [0.52  ,  0.52  ,  0.53  ,  0.54  ,  0.54   , 0.55 ,  0.55   , 0.56  ,  0.56  ,  0.57 ,   0.58 ,   0.60],
           [0.52  ,  0.52  ,  0.53  ,  0.54  ,  0.55   , 0.55 ,  0.55  ,  0.55  ,  0.56  ,  0.57 ,   0.59  ,  0.60]]) #压心系数
    AE = 0.01745329
    g = 9.81


    P = P1 * (t <= Tp1) + 0 * (t > Tp1)
    #比例导引给出过载指令
    r = math.sqrt((x - xt) ** 2 + (y - yt) ** 2)
    qs = math.atan((y - yt) / (x - xt))
    vc = vt * math.cos(qs - thetat) - v* math.cos(qs - theta)
    vmx = v * math.cos(theta)
    vmy = v * math.sin(theta)
    qd = ((vmy - vty) * (x - xt) - (y - yt) * (vmx - vtx)) / (r ** 2)

    ny = -K * vc * qd / (g * math.cos(theta - qs)) + math.cos(theta) #ny为弹道系需用法向过载
    R0 = 6371000
    h = math.sqrt(x ** 2 + (y + R0) **2) - R0
    T0, SONIC, P0, RHO = RL_GA.aero_parameter.aero_parameter(h)
    Ma = v / SONIC  #计算马赫数
    q = 0.5 * RHO * v **2 # 动压
    s = 0.0201  #特征面积
    L = 2.000  #特征长度

    #平衡攻角
    i = 1
    a1 = -40 * AE
    a2 = 40 * AE

    XX = np.array([AMa_CX, ACXnac]).T
    while 1:
        na2 = (P * math.sin(a2) + (np.sign(a2) * RL_GA.interp.twointerp(Aan, AMa, ACN, abs(a2), Ma) * math.cos(a2) -
              (RL_GA.interp.twointerp(Aax, AMa_CX, ACX, abs(a2), Ma) + RL_GA.interp.twointerp(AH, AMa_CX, ACXH, h / 1000, Ma) +
               RL_GA.interp.oneinterp1(XX, Ma) * (t > Tp1)) * math.sin(a2)) * q * s) / m / g
        na1 = (P * math.sin(a1) + (np.sign(a1) * RL_GA.interp.twointerp(Aan, AMa, ACN, abs(a1), Ma) * math.cos(a1) -
              (RL_GA.interp.twointerp(Aax, AMa_CX, ACX, abs(a1), Ma) + RL_GA.interp.twointerp(AH, AMa_CX, ACXH, h / 1000, Ma) + RL_GA.interp.oneinterp1(XX, Ma) *
               (t > Tp1)) * math.sin(a1)) * q * s) / m / g
        am = (ny - na1) * (a2 - a1) / (na2 - na1) + a1
        # nam = (P * math.sin(am) + (np.sign(am) * interp.twointerp(Aan, AMa, ACN, abs(am), Ma) * math.cos(am) -
        # (interp.twointerp(Aax, AMa_CX, ACX, abs(am), Ma) + interp.twointerp(AH, AMa_CX, ACXH, h / 1000, Ma) + interp.oneinterp1(XX, Ma) *
        #  (t > Tp1)) * math.sin(am)) * q * s) / m / g
        nam = (P * math.sin(am) + (np.sign(am) * RL_GA.interp.twointerp(Aan, AMa, ACN, abs(am), Ma) * math.cos(am) - (
        RL_GA.interp.twointerp(Aax, AMa_CX, ACX, abs(am), Ma) + RL_GA.interp.twointerp(AH, AMa_CX, ACXH, h / 1000, Ma) + RL_GA.interp.oneinterp1(XX, Ma) * (
        t > Tp1)) * math.sin(am)) * q * s) / m / g

        #nam_b=(interp.twointerp(Aan, AMa, ACN, abs(am), Ma) )
        #        - (interp.twointerp(Aax, AMa_CX, ACX, abs(am), Ma) + interp.twointerp(AH, AMa_CX, ACXH, h / 1000, Ma) + interp.oneinterp1(XX, Ma) * (
        # t > Tp1)) * math.sin(am))

        i = i + 1
        if abs(nam - ny) < 0.001 or i > 100:
            break

        if nam > ny:
            a2 = am
        else:
            a1 = am

    alpha = am
    ny = nam
    if alpha > 40 * AE:
        alpha = 40 * AE
        ny = (P * math.sin(alpha) + (np.sign(alpha) * RL_GA.interp.twointerp(Aan, AMa, ACN, abs(alpha), Ma) * math.cos(alpha) -
        (RL_GA.interp.twointerp(Aax, AMa_CX, ACX, abs(alpha), Ma) + RL_GA.interp.twointerp(AH, AMa_CX, ACXH, h / 1000, Ma) + RL_GA.interp.oneinterp1(XX, Ma) *
         (t > Tp1)) * math.sin(alpha)) * q * s) / m / g

    if alpha < -40 * AE:
        alpha = -40 * AE
        ny = (P * math.sin(alpha) + (np.sign(alpha) * RL_GA.interp.twointerp(Aan, AMa, ACN, abs(alpha), Ma) * math.cos(alpha) -
        (RL_GA.interp.twointerp(Aax, AMa_CX, ACX, abs(alpha), Ma) + RL_GA.interp.twointerp(AH, AMa_CX, ACXH, h / 1000, Ma) + RL_GA.interp.oneinterp1(XX, Ma) *
         (t > Tp1)) * math.sin(alpha)) * q * s) / m / g

    XF = (RL_GA.interp.twointerp(Aax, AMa_CX, ACX, abs(alpha), Ma) + RL_GA.interp.twointerp(AH, AMa_CX, ACXH, h / 1000, Ma) + RL_GA.interp.oneinterp1(XX,Ma) * (t > Tp1)) * q * s  #弹体系
    YF = np.sign(alpha) * RL_GA.interp.twointerp(Aan, AMa, ACN, abs(alpha), Ma) * q * s    #弹体系

    XF1 = XF* math.cos(alpha) + YF * math.sin(alpha)  # 弹道系
    YF1 = YF* math.cos(alpha) - XF* math.sin(alpha)   #弹道系

    return P,XF1,ny,alpha
