"""
A simple example for Reinforcement Learning using table lookup Q-learning method.
An agent "o" is on the left of a 1 dimensional world, the treasure is on the rightmost location.
Run this program and to see how the agent will improve its strategy of finding the treasure.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
import pandas as pd
import time
from RL_GA.interpolation import *
import RL_GA.RK4



N_STATES = 25   # the length of the 1 dimensional world
ACTIONS = [2, 3, 4]     # available actions
EPSILON = 0.9   # greedy police
ALPHA = 0.1     # learning rate
GAMMA = 0.9    # discount factor
MAX_EPISODES = 50   # maximum episodes
FRESH_TIME = 0.3    # fresh time for one move
h = 0.05
t = 0



def transition(t,SS,vt,Tp1,P1,K,g):
    flag = 0
    for i in range(50):#这里的50是因为程序没0.05秒核算一次，我们设定的是2.5秒改变一次k，所以2.5/0.05
        P, X, ny, alpha = interpolation(t, SS[-1], vt, Tp1, P1, K)
        P = np.array([[P]])
        X = np.array([[X]])
        ny = np.array([[ny]])
        alpha = np.array([[alpha]])
        S_temp = RL_GA.RK4.RK4(t, h, SS[-1], P, X, ny, alpha, vt, Tp1, P1, g)
        S_temp = np.array([S_temp])
        SS = np.row_stack((SS, S_temp))
        t += 0.05

        try:
            if math.sqrt((SS[-1, 2] - SS[-1, 6]) ** 2 + (SS[-1, 3] - SS[-1, 7]) ** 2) < 100:
                flag = 1
                break

            else:
                flag = 0
        except:
            print('some thing wrong in the transition process')
    return SS, t, flag

def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),     # q_table initial values
        columns=actions,    # actions's name
    )
    # print(table)    # show table
    return table


def choose_action(state, q_table):
    # This is how to choose an action
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):  # act non-greedy or state-action have no value
        action_name = np.random.choice(ACTIONS)
    else:   # act greedy
        action_name = state_actions.idxmax()    # replace argmax to idxmax as argmax means a different function in newer version of pandas
    return action_name


def get_env_feedback(S, A, SS,t):
    # This is how agent will interact with the environment

    S_ = 0
    R = 0
    if A == 2:    # move right
        SS,t,f = transition(t,SS,-100,4,15000,A,9.81)
        if f == 1:
            S_ = 'terminal'
            R = np.mean(SS[:, 0])
        if f == 0:
            S_ = S + 1
            R = 0

    if A == 3:    # move right
        SS,t,f = transition(t,SS,-100,4,15000,A,9.81)
        if f == 1:
            S_ = 'terminal'
            R = np.mean(SS[:, 0])
        if f == 0:
            S_ = S + 1
            R = 0

    if A == 4:    # move right
        SS,t,f = transition(t,SS,-100,4,15000,A,9.81)
        if f == 1:
            S_ = 'terminal'
            R = np.mean(SS[:, 0])
        if f == 0:
            S_ = S + 1
            R = 0

    return S_, R, SS, t

# 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2,4,4,2,2,4,3,2,3,2


def rl():
    # main part of RL loop
    q_table = build_q_table(N_STATES, ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        SS = np.array([[400, 20 / 180, 0, 10000, 100, 0, 40000, 10000]])
        t = 0
        S = 0
        is_terminated = False
        while not is_terminated:

            A = choose_action(S, q_table)
            S_, R, SS, t = get_env_feedback(S, A, SS, t)  # take action & get next state and reward
            q_predict = q_table.loc[S, A]
            if S_ != 'terminal':
                # print(q_table.iloc[S_].max())
                q_target = R + GAMMA * q_table.iloc[S_].max()   # next state is not terminal
            if S_ == 'terminal':
                q_target = R     # next state is terminal
                is_terminated = True    # terminate this episode

            q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # update
            S = S_  # move to next state

            step_counter += 1
    return q_table


if __name__ == "__main__":
    q_table = rl()
    print('\r\nQ-table:\n')
    print(q_table)

    # q = build_q_table(N_STATES,ACTIONS)
    # print(q.iloc[1249].max())
    # 
    # SS = np.array([[400, 20 / 180, 0, 10000, 100, 0, 40000, 10000]])
    # i=0
    # while True:
    #     SS,t = transition(t, SS, -100, 4, 15000, 2, 9.81)
    #     print(math.sqrt((SS[-1, 2] - SS[-1, 6]) ** 2 + (SS[-1, 3] - SS[-1, 7]) ** 2))
    #     i+=1
    #     print(i)
