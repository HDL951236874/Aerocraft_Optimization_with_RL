from RL_GA.maze_env import Maze
from RL_GA.RL_brain import DeepQNetwork
import math
from RL_GA.RL import transition
from RL_GA.interpolation import *
from RL_GA.RK4 import *
from RL_GA.pytorch_RL import *
import torch
from torch.autograd import Variable

class env():
    def __init__(self):
        self.action_space = [2,3,4]
        self.n_actions = len(self.action_space)
        self.n_features = 3
        self.h = 0.05
        self.g = 9.81
        self.t = 0
        self.Tp1 = 4
        self.v = 400
        self.vt = -100
        self.P1 = 15000
        self.m0 = 100
        self.mzt = 0
        self.alpha = 20*math.pi/180
        self.x = 0
        self.y = 10000
        self.xt = 40000
        self.yt = 10000
        self.SS = np.array([[self.v, self.alpha, self.x, self.y, self.m0, self.mzt, self.xt, self.yt]])

    def reset(self):
        '''
        the parameter of the situation
        :return:
        '''
        self.__init__()
        return np.array([self.x,self.y,self.alpha])

    def step(self,action):
        K = 0
        if action == 0:
            K = 2
        if action == 1:
            K = 3
        if action == 2:
            K = 4
        flag = True
        R = 0
        #这一步其实是没有什么作用的，相对于导弹的重量，推进器再该模拟情况下的质量可以忽略不记
        if self.t >= self.Tp1:
            self.SS[-1,4] = self.SS[-1,4] - self.mzt

        P, X, ny, alpha = interpolation(self.t, self.SS[-1], self.vt, self.Tp1, self.P1, K)
        P = np.array([[P]])
        X = np.array([[X]])
        ny = np.array([[ny]])
        alpha = np.array([[alpha]])
        S_temp = RK4(self.t, self.h, self.SS[-1], P, X, ny, alpha, self.vt, self.Tp1, self.P1, self.g)
        S_temp = np.array([S_temp])
        self.SS = np.row_stack((self.SS, S_temp))
        self.t += 0.05

        try:
            # print('距离'+str(math.sqrt((self.SS[-1, 2] - self.SS[-1, 6]) ** 2 + (self.SS[-1, 3] - self.SS[-1, 7]) ** 2))+ '导弹位置'+str((self.SS[-1,2],self.SS[-1,3]))+'目标位置'+str((self.SS[-1,6],self.SS[-1,7]))+'K='+ str(K) + 'and'+ 't=' + str(self.t))
            if math.sqrt((self.SS[-1, 2] - self.SS[-1, 6]) ** 2 + (self.SS[-1, 3] - self.SS[-1, 7]) ** 2) < 100:
                flag = True
                R = np.mean(self.SS[:,0])
            else:
                flag = False
                R = np.mean(self.SS[:,0])
        except:
            print(' ')

        return np.array([self.SS[-1,2],self.SS[-1,3],self.SS[-1,1]]),R,flag



def run_maze(net,net_):
    step = 0
    for episode in range(50):
        print(episode)
        # initial observation
        observation = env_real.reset()
        # observation = normalization(observation,env())
        while True:
            observation = torch.from_numpy(observation).float()

            action = np.argmax(net.choose_action(observation).detach().numpy())

            # RL take action and get next observation and reward
            observation_, reward, done = env_real.step(action)


            net.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                net.learn(net_)

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
            step += 1

    # end of game
    print('game over')


if __name__ == "__main__":
    # maze game
    env_real = env()
    net = simpleNet(3,10,10,3)
    net_ = simpleNet(3,10,10,3)
    run_maze(net,net_)


    env_test = env()
    ob = env_test.reset()
    done = False
    al = []

    while done!=True:
        ob = torch.from_numpy(ob).float()

        action = np.argmax(net.choose_action(ob).detach().numpy())

        al.append(action+2)

        ob_ ,r,done= env_test.step(action)

        ob = ob_

    print(al)
    print(np.mean(env_test.SS[:,0]))

