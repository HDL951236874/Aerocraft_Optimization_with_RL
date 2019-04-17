import torch
from torch import nn
from torch import optim
import numpy as np
from torch.autograd import Variable
import torch.nn.functional as F
import matplotlib.pyplot as plt


class simpleNet(nn.Module):
    """
    定义了一个简单的三层全连接神经网络，每一层都是线性的
    """

    def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim, learning_rate=0.1, reward_decay=0.9, e_greedy=0.9, replace_target_iter=200,
                 memory_size=200, batch_size=32, e_greedy_increment=None):
        super(simpleNet, self).__init__()
        self.layer1 = nn.Sequential(nn.Linear(in_dim, n_hidden_1), nn.ReLU(True))
        self.layer2 = nn.Sequential(nn.Linear(n_hidden_1, n_hidden_2), nn.ReLU(True))
        self.layer3 = nn.Sequential(nn.Linear(n_hidden_2, out_dim))
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.memory = np.zeros((self.memory_size,8))
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max
        self.optimizer = torch.optim.SGD(self.parameters(), lr=self.lr)
        self.loss_func = torch.nn.MSELoss()  # this is for regression mean squared loss

        self.learn_step_counter = 0
        self.n_feature = 3
        self.cost_his = []


    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x

    def choose_action(self,x):

        return self(x)

    def store_transition(self, s, a, r, s_):
        '''
        这一步也不用更改，因为完全是数据存储结构
        :param s:
        :param a:
        :param r:
        :param s_:
        :return:
        '''
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0

        transition = np.hstack((s, [a, r], s_))

        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size
        self.memory[index] = transition

        self.memory_counter += 1

    def learn(self,net_):
        # check to replace target parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            torch.save(self, "net_params.pkl")
            net_ = torch.load('net_params.pkl')

        # sample batch memory from all memory
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]

        q_next = net_(torch.from_numpy(batch_memory[:,-self.n_feature:]).float())
        q_eval = self(torch.from_numpy(batch_memory[:,:self.n_feature]).float())

        # q_next, q_eval = self.sess.run(
        #     [self.q_next, self.q_eval],
        #     feed_dict={
        #         self.s_: batch_memory[:, -self.n_features:],  # fixed params
        #         self.s: batch_memory[:, :self.n_features],  # newest params
        #     })

        # change q_target w.r.t q_eval's action
        q_target = q_eval.clone()

        q_next = q_next.detach().numpy()
        q_eval = q_eval.detach().numpy()
        q_target = q_target.detach().numpy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_feature].astype(int)
        reward = batch_memory[:, self.n_feature + 1]

        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)

        q_target = Variable(torch.from_numpy(q_target).float(),requires_grad = True)
        q_eval = Variable(torch.from_numpy(q_eval).float(), requires_grad = True)


        loss = self.loss_func(q_target, q_eval)  # must be (1. nn output, 2. target)

        self.optimizer.zero_grad()  # clear gradients for next train
        loss.backward()  # backpropagation, compute gradients
        self.optimizer.step()  # apply gradients

        # train eval network
        # _, self.cost = self.sess.run([self._train_op, self.loss],
        #                              feed_dict={self.s: batch_memory[:, :self.n_features],
        #                                         self.q_target: q_target})

        # increasing epsilon
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1