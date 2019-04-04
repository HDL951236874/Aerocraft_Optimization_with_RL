from RL_GA.maze_env import Maze
from RL_GA.RL_brain import DeepQNetwork
import math
from RL_GA.RL import transition
from RL_GA.interpolation import *
from RL_GA.RK4 import *

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

def normalization(ob,env):

    a=(ob[0] - env.x) / (env.xt - env.x)
    b=(ob[1] - env.y) / (13000 - env.y)
    c=(ob[2] - env.xt) / (env.x - env.xt)
    d=(ob[3] - env.yt) / (13000 - env.y)
    e=(ob[4] - 0) / (math.pi / 2)

    return np.array([a,b,c,d,e])

def test(RL):
    env_test = env()
    al = []
    done = False
    ob = env_test.reset()

    while not done:
        ob = ob[np.newaxis, :]


        actions_value = RL.sess.run(RL.q_eval, feed_dict={RL.s: ob})
        action = np.argmax(actions_value)

        print(str(actions_value)+'最大的是'+str(action+2))
        al.append(action + 2)
        ob, R, done = env_test.step(action)

    print(al)
    print(np.mean(env_test.SS[:, 0]))


def run_maze():
    step = 0
    for episode in range(5000):
        print(episode)
        # initial observation
        observation = env_real.reset()
        # observation = normalization(observation,env())
        while True:

            # print(env.t)
            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done = env_real.step(action)

            # reward = (reward-700)/(800-700)
            # observation_ = normalization(observation_,env())

            RL.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                RL.learn()


            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
            step += 1

        test(RL)



    # end of game
    print('game over')


if __name__ == "__main__":
    # maze game
    env_real = env()
    RL = DeepQNetwork(env_real.n_actions, env_real.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      output_graph=True
                      )

    run_maze()
    RL.plot_cost()


    RL.epsilon = 1
    al = []
    done = False
    ob = env_real.reset()

    while not done:
        a = RL.choose_action(ob)
        al.append(a+2)
        ob, R, done = env_real.step(a)

    print(al)
    print(np.mean(env_real.SS[:,0]))
