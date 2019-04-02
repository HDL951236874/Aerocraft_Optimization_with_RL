import math
import numpy as np

def RK4(t,h,S_i,P,X,ny,alpha,vt,Tp1,P1,g):
    def fun(t,S_i,P,X,ny,alpha,vt,Tp1,P1,g):
        Ip1 = 240 * g  # 比冲
        V = S_i[0]
        theta = S_i[1]
        x = S_i[2]
        y = S_i[3]
        m = S_i[4]
        thetat = S_i[5]
        xt = S_i[6]
        yt = S_i[7]
        #平飞目标
        vtx = vt * math.cos(thetat)
        vty = vt * math.sin(thetat)
        dV = (P * math.cos(alpha) - X) / m - g * math.sin(theta)
        dtheta = ny * g / V - g * math.cos(theta) / V
        dx = V * math.cos(theta)
        dy = V * math.sin(theta)
        dm = -P1 / Ip1 * (t <= Tp1) + 0 * (t > Tp1)
        dthetat = 0  #平飞目标
        dxt = vtx
        dyt = vty
        dS = np.array([float(dV),float(dtheta),float(dx),float(dy),dm,dthetat,dxt,dyt])
        return dS

    K1 =h*fun(t,S_i,P,X,ny,alpha,vt,Tp1,P1,g)
    K2 = h * fun(t + h / 2, S_i+ K1 / 2,P,X,ny,alpha,vt,Tp1,P1,g)
    K3 = h * fun(t + h / 2, S_i + K2 / 2,P,X,ny,alpha,vt,Tp1,P1,g)
    K4 = h * fun(t + h, S_i+ K3,P,X,ny,alpha,vt,Tp1,P1,g)
    S_j = S_i+ 1 / 6 * (K1 + 2 * K2 + 2 * K3 + K4)
    return S_j

