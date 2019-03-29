import math
import numpy as np
import interpolation
import RK4


# 全局变量

def main(g, x0, y0, theta0, v0, xt0, yt0, thetat0, vt, m0, P1, P2, Ip1, Ip2, Tp1, Tp2, mzt, K):
    S = np.array([[v0, theta0, x0, y0, m0, thetat0, xt0, yt0]])
    i = 0
    h = 0.05
    t = 0
    if type(K) == list:
        P, X, ny, alpha = interpolation.interpolation(t, S[i], vt, Tp1, P1, K[0])
    else:
        P, X, ny, alpha = interpolation.interpolation(t, S[i], vt, Tp1, P1, K)
    P = np.array([[P]])
    X = np.array([[X]])
    ny = np.array([[ny]])
    alpha = np.array([[alpha]])
    S_temp = RK4.RK4(t, h, S[i], P, X, ny, alpha,vt,Tp1,P1,g)
    S_temp = np.array([S_temp])
    S = np.row_stack((S, S_temp))
    i = 1
    t = 0.05
    z = 1
    while t <= Tp1:
        if type(K) == list:
            P_temp, X_temp, ny_temp, alpha_temp = interpolation.interpolation(t, S[i], vt, Tp1, P1,K[z])
            z += 1
        else:
            P_temp, X_temp, ny_temp, alpha_temp = interpolation.interpolation(t, S[i], vt, Tp1, P1,K)

        P = np.row_stack((P, P_temp))
        X = np.row_stack((X, X_temp))
        ny = np.row_stack((ny, ny_temp))
        alpha = np.row_stack((alpha, alpha_temp))

        S_temp = RK4.RK4(t, h, S[i], P[i], X[i], ny[i], alpha[i],vt,Tp1,P1,g)
        S = np.row_stack((S, S_temp))

        i = i + 1
        t = t + 0.05

    S[i, 4] = S[i, 4] - mzt

    while Tp1< t <= 500:
        if type(K) == list:

            P_temp, X_temp, ny_temp, alpha_temp = interpolation.interpolation(t, S[i], vt,Tp1,P1,K[z])
            z += 1

        else:

            P_temp, X_temp, ny_temp, alpha_temp = interpolation.interpolation(t, S[i], vt,Tp1,P1,K)

        P = np.row_stack((P, P_temp))
        X = np.row_stack((X, X_temp))
        ny = np.row_stack((ny, ny_temp))
        alpha = np.row_stack((alpha, alpha_temp))

        S_temp = RK4.RK4(t, h, S[i], P[i], X[i], ny[i], alpha[i],vt,Tp1,P1,g)
        S = np.row_stack((S, S_temp))

        R = np.zeros(10000)
        R[i] = math.sqrt((S[i, 2] - S[i, 6]) ** 2 + (S[i, 3] - S[i, 7]) ** 2)

        if R[i] < 100:
            break

        i = i + 1
        t = t + 0.05

    V = S[:, 0]
    theta = S[:, 1]
    x = S[:, 2]
    y = S[:, 3]
    m = S[:, 4]
    thetat = S[:, 5]
    xt = S[:, 6]
    yt = S[:, 7]

    l1 = np.linspace(0, (i + 1) * h, num=i + 2)
    l2 = np.linspace(0, i * h, num=i + 1)

    print(np.mean(V))
    return x, y, xt, yt, l1, V, l2, ny
    # return  np.mean(V)