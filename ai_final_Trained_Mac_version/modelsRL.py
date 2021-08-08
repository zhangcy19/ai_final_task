import json
import os
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

import gameLoaderRL

USE_GPU = True
if USE_GPU and torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')


class DeepQModel(nn.Module):
    """
        DQL强化学习
        仿照VggNet
        数据存储与读取
    """

    def __init__(self, env):
        super(DeepQModel, self).__init__()
        self.data_loader = gameLoaderRL.GameLoader(self, env)
        self.env = env

        self.num_actions = 16
        self.state_layer_size = 10
        self.state_row_size = 16
        self.state_col_size = 16
        self.units_size = 64 * 4

        self.net1 = nn.Sequential(
            nn.Conv2d(self.state_layer_size, 64, kernel_size=3, stride=1, padding=2),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=2),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=0),
            nn.ReLU(),
            nn.MaxPool2d(2, stride=2),
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=0),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=0),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=0),
            nn.ReLU(),
            nn.MaxPool2d(2, stride=2)
        )
        self.net2 = nn.Sequential(
            nn.Linear(self.units_size, 200),
            nn.ReLU(),
            nn.Linear(200, 100),
            nn.ReLU(),
            nn.Linear(100, self.state_col_size)
        )

        flag = 0
        with open("assist_data/Q_state.json", "r") as f:
            dic = json.loads(f.read())
            if dic is not None and "net_state" in dic:
                if dic["net_state"] is not None and dic["net_state"] == 1:
                    flag = 1
        if flag:
            print("******************************")
            print("       正在加载神经网络")
            st = time.time()
            self.net1.load_state_dict(torch.load('./assist_data/Q_net1.pkl'))
            self.net2.load_state_dict(torch.load('./assist_data/Q_net2.pkl'))
            ed = time.time()
            print("加载成功, 用时{:.3f}s".format(ed - st))
            print("******************************")
            print("")

        self.optimizer = torch.optim.SGD(self.parameters(), lr=0.005)
        self.loss_fn = nn.MSELoss()

    def forward(self, states, Q_target=None):
        """
        TODO: Reinforcement Learning

        Runs the DQN for a batch of states.

        The DQN takes the state and computes Q-values for all possible actions
        that can be taken. That is, if there are two actions, the network takes
        as input the state s and computes the vector [Q(s, a_1), Q(s, a_2)]

        When Q_target == None, return the tensor of Q-values currently computed
        by the network for the input states.

        When Q_target is passed, it will contain the Q-values which the network
        should be producing for the current states. You must return a PyTorch scalar
        which computes the training loss between your current Q-value
        predictions and these target values, using mse loss.

        Inputs:
            states: a (batch_size x layer_size x row_size x col_size) PyTorch tensor
            Q_target: a (batch_size x col_size) PyTorch tensor, or None
        Output:
            (if Q_target is not None) The loss for optimizing the network
            (if Q_target is None) A (batch_size x 2) PyTorch tensor of Q-value
                scores, for the two actions
        """
        x = states
        x = self.net1(x)
        x = x.view(x.shape[0], -1)
        x = self.net2(x)

        if Q_target is not None:
            return self.loss_fn(x, Q_target)
        else:
            return x

    def get_action(self, state, eps):
        """
        Select an action for a single state using epsilon-greedy.

        Inputs:
            state: a (1 x 10 x 16 x 16) PyTorch tensor or numpy array
            eps: a float, epsilon to use in epsilon greedy
        Output:
            the index of the action to take (0～15)
        """
        if isinstance(state, np.ndarray):
            state = torch.from_numpy(state).float().to(device)
        if np.random.rand() < eps:
            # ret = int(np.random.choice(self.num_actions))
            # ret = self.env.newHeuri()
            # if ret is None:
            ret = int(np.random.choice(self.num_actions))
            return ret
        else:
            scores = self.forward(state)
            ret = torch.argmax(scores).item()
            return ret

    def train_model(self, num):
        t = 0
        for x, y in self.data_loader:
            t += 1
            if t > num:
                break
            x, y = x.to(device), y.to(device)
            self.optimizer.zero_grad()
            loss = self.forward(x, y)
            loss.backward()
            self.optimizer.step()

            print("******************************")
            print("batch {}训练成功，正在保存神经网络".format(t))
            st = time.time()
            self.save()
            ed = time.time()
            print("保存成功, 用时{:.3f}s  文件Q_net1.pkl大小:{:.3}MB  文件Q_net2.pkl大小:{:.3}MB".format(ed - st,
                os.path.getsize("assist_data/Q_net1.pkl") / 1048576.,
                os.path.getsize("assist_data/Q_net2.pkl") / 1048576.))
            print("******************************")
            print("")

    def save(self):
        torch.save(self.net1.state_dict(), './assist_data/Q_net1.pkl')
        torch.save(self.net2.state_dict(), './assist_data/Q_net2.pkl')
        with open("assist_data/Q_state.json", "w+") as f:
            c = f.read()
            if f.readline() != "":
                dic = json.loads(c)
                if dic is None:
                    dic = {}
            else:
                dic = {}
            dic["net_state"] = 1
            json.dump(dic, f)
