import json
import os
import random
import time

import numpy as np
import torch
import torch.nn as nn
from collections import namedtuple, deque


USE_GPU = True
if USE_GPU and torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')

Transition = namedtuple("Transition", field_names=["state", "action", "reward", "next_state", "done"])

class ReplayMemory(object):
    """ 记忆存储器
        采用状态压缩json存储，每个单元约6kb
    """
    def __init__(self, capacity):
        """Replay memory class

        Args:
            capacity (int): Max size of this memory
        """
        self.capacity = capacity
        self.cursor = 0
        self.memory = []
        print("******************************")
        print("       正在加载学习经验")
        st = time.time()
        self.load()
        ed = time.time()
        print("加载成功, 用时{:.3f}s".format(ed - st))
        print("******************************\n")

    def push(self, state, action, reward, next_state, done):
        """Creates `Transition` and insert

        Args:
            state (np.ndarray): 3-D tensor of shape (input_dim,)
            action (int): action index (0 <= action < output_dim)
            reward (int): reward value
            next_state (np.ndarray): 3-D tensor of shape (input_dim,)
            done (bool): whether this state was last step
        """
        if len(self) < self.capacity:
            self.memory.append(None)

        self.memory[self.cursor] = Transition(state, action, reward, next_state, done)
        self.cursor = (self.cursor + 1) % self.capacity

    def pop(self, batch_size):
        """Returns a minibatch of `Transition` randomly

        Args:
            batch_size (int): Size of mini-bach

        Returns:
            List[Transition]: Minibatch of `Transition`
        """
        return random.sample(self.memory, batch_size)

    def load(self):
        """json读取"""
        with open("assist_data/Q_memory.json", "r") as f:
            dic = json.loads(f.read())
            if(dic is None):
                return
            dic = eval(dic)
            tdic = {}
            maxn = 0
            for ni, dic2 in dic.items():
                if dic2 is None:
                    continue
                i = int(ni)
                maxn = max(maxn, i)
                dic2 = eval(dic2)
                tmpdic = {}
                for ni2, v2 in dic2.items():
                    if v2 is None:
                        continue
                    i2 = int(ni2)
                    if i2 == 0 or i2 == 3:
                        v2 = eval(v2)
                        v2 = self.build(v2)
                    elif i2 == 1:
                        v2 = int(v2)
                    elif i2 == 2:
                        v2 = float(v2)
                    elif i2 == 4:
                        v2 = bool(v2)
                    tmpdic[i2] = v2
                tdic[i] = Transition(tmpdic[0], tmpdic[1], tmpdic[2], tmpdic[3], tmpdic[4])
            self.memory = []
            for i in range(maxn + 1):
                if i in tdic and tdic[i] is not None:
                    self.push(tdic[i].state, tdic[i].action, tdic[i].reward, tdic[i].next_state, tdic[i].done)
            print("已成功加载记忆数量:", maxn + 1)

    def save(self):
        """json存储"""
        with open("assist_data/Q_memory.json", "w") as f:
            dic = {}
            for i, v in enumerate(self.memory):
                if v is None:
                    continue
                dic2 = {}
                for i2, v2 in enumerate(v):
                    if i2 == 0 or i2 == 3:
                        v2 = self.plain(v2)
                    v2 = json.dumps(v2)
                    ni2 = str(i2)
                    dic2[ni2] = v2
                ni = str(i)
                dic2 = json.dumps(dic2)
                dic[ni] = dic2
            dic = json.dumps(dic)
            json.dump(dic, f)
            print("已成功存储记忆数量:{}  文件Q_memory.json大小:{:.3}MB".format(len(self.memory), os.path.getsize("assist_data/Q_memory.json") / 1048576.))

    def plain(self, v):
        """state 编码器"""
        ret = {}
        idx = 0
        for i in v:
            for j in i:
                x = 0
                for k in j:
                    if k > 0:
                        x += 1
                    x *= 2
                ret[str(idx)] = str(x)
                idx += 1
        return ret

    def build(self, ret):
        """state 解码器"""
        v = np.empty([10, 16, 16], dtype=int)
        idx = 0
        for i in range(10):
            for j in range(16):
                nidx = str(idx)
                x = int(ret[nidx])
                idx += 1
                for k in range(15, -1, -1):
                    x //= 2
                    v[i][j][k] = x & 1
        return v

    def __len__(self):
        """Returns the length """
        return len(self.memory)

    def __del__(self):
        print("******************************")
        print("       正在存储学习经验")
        st = time.time()
        self.save()
        ed = time.time()
        print("存储成功, 用时{:.3f}s".format(ed - st))
        print("******************************")
        print("")


class GameLoader(object):
    def __init__(self, model, env):
        self.model = model
        self.n_episode = 32
        self.stats = {}
        self.env = env

    def __iter__(self):
        # Adapted from https://gist.github.com/kkweon/52ea1e118101eb574b2a83b933851379
        self.stats = {}
        self.stats['mean_reward'] = 0

        # Max size of the replay buffer
        capacity = 2000

        # After max episode, eps will be `min_eps`
        max_eps_episode = 28

        # eps will never go below this value
        min_eps = 0.05

        # Number of transition samples in each minibatch update
        batch_size = 64

        # Discount parameter
        gamma = 0.95

        # Max number of episodes to run
        n_episode = self.n_episode

        # Win if you average at least this much reward (max reward is 200) for
        # num_episodes_to_average consecutive episodes
        reward_threshold = 180
        reward_threshold_small = 100
        num_episodes_to_average = 32

        # If set (an integer), clip the absolute difference between Q_pred and
        # Q_target to be no more than this
        td_error_clipping = None

        episode_print_interval = 1

        self.stats['reward_threshold'] = reward_threshold
        self.stats['reward_threshold_small'] = reward_threshold_small

        rewards = deque(maxlen=num_episodes_to_average)
        replay_memory = ReplayMemory(capacity)

        def getQValue(model, states, device=None):
            states = torch.from_numpy(states).float()
            if device is not None:
                states = states.to(device)
            q = model.forward(states)
            return q.detach().cpu().numpy()

        def train_helper(minibatch):
            """Prepare minibatches

            Args:
                minibatch (List[Transition]): Minibatch of `Transition`

            Returns:
                float: Loss value
            """
            states = np.vstack([x.state[np.newaxis, :] for x in minibatch])
            actions = np.array([x.action for x in minibatch])
            rewards = np.array([x.reward for x in minibatch])
            next_states = np.vstack([x.next_state[np.newaxis, :] for x in minibatch])
            done = np.array([x.done for x in minibatch])

            Q_predict = getQValue(self.model, states, device)
            Q_target = np.copy(Q_predict)
            Q_target[np.arange(len(Q_target)), actions] = (
                    rewards + gamma * np.max(getQValue(self.model, next_states, device), axis=1) * ~done)

            if td_error_clipping is not None:
                Q_target = Q_predict + np.clip(
                    Q_target - Q_predict, -td_error_clipping, td_error_clipping)

            return Q_predict, Q_target

        annealing_slope = (min_eps - 1.0) / max_eps_episode

        for episode in range(n_episode):
            eps = max(annealing_slope * episode + 1.0, min_eps)

            s = self.env.reset()
            done = False
            total_reward = 0

            while not done:
                a = self.model.get_action(torch.from_numpy(s[np.newaxis, :]).float(), eps)
                s2, r, done = self.env.step(a)

                total_reward += r

                replay_memory.push(s, a, r if not done else -1, s2, done)

                if len(replay_memory) > batch_size:
                    minibatch = replay_memory.pop(batch_size)
                    Q_predict, Q_target = train_helper(minibatch)
                    states = np.vstack([x.state[np.newaxis, :] for x in minibatch])
                    yield torch.from_numpy(states).float(), torch.from_numpy(Q_target).float()

                s = s2
                '''
            rewards.append(total_reward)
            if (episode + 1) % episode_print_interval == 0:
                print("[Episode: {:3}] Reward: {:5} Mean Reward of last {} episodes: {:5.1f} epsilon: {:5.2f}".format(
                    episode + 1, total_reward, num_episodes_to_average, np.mean(rewards), eps))

            if len(rewards) == rewards.maxlen:
                self.stats['mean_reward'] = np.mean(rewards)
                if np.mean(rewards) >= reward_threshold:
                    print("Completed in {} episodes with mean reward {}".format(
                        episode + 1, np.mean(rewards)))
                    self.stats['reward_threshold_met'] = True
                    break
        else:
            # reward threshold not met
            print("Aborted after {} episodes with mean reward {}".format(episode + 1, np.mean(rewards)))

'''