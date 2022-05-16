#%%
import random
import gym
import numpy as np
from tictactoe import TicTacToeEnvironment
from collections import deque
from sklearn.multioutput import MultiOutputRegressor
from lightgbm import LGBMRegressor

GAMMA = 0.5
LEARNING_RATE = 0.01

MEMORY_SIZE = 5000
BATCH_SIZE = 20

EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.05
EXPLORATION_DECAY = 0.96


class DQNSolver:

    def __init__(self, observation_space, action_space):
        self.exploration_rate = EXPLORATION_MAX

        self.action_space = action_space
        self.memory = deque(maxlen=MEMORY_SIZE)

        self.model = MultiOutputRegressor(LGBMRegressor(n_estimators=100, n_jobs=-1))
        self.isFit = False


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    def act(self, state):
        if np.random.rand() < self.exploration_rate:
            return random.randrange(self.action_space)
        if self.isFit == True:
            q_values = self.model.predict(np.array(state).reshape(1,-1))
        else:
            q_values = np.zeros(self.action_space).reshape(1, -1)
        return np.argmax(q_values[0])


    def experience_replay(self):
        if len(self.memory) < BATCH_SIZE:
            return
        batch = random.sample(self.memory, int(len(self.memory)/1))
        X = []
        targets = []
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            if not terminal:
                if self.isFit:
                    q_update = (reward + GAMMA * np.amax(
                        self.model.predict(
                            np.array(state_next).reshape(1,-1))[0]))
                else:
                    q_update = reward
            if self.isFit:
                q_values = self.model.predict(np.array(state).reshape(1,-1))
            else:
                q_values = np.zeros(self.action_space).reshape(1, -1)
            q_values[0][action] = q_update
            
            X.append(state)
            targets.append(q_values[0])

        #print(np.array(X).shape)
        self.model.fit(X, targets)
        self.isFit = True
        self.exploration_rate *= EXPLORATION_DECAY
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)


def evaluate_model(dqn_solver):
    """Função utilizada para avaliar modelo obtido"""
    env = TicTacToeEnvironment()

    num_episodes = 150
    total_steps = 0
    num_games_lost = 0
    num_games_won = 0
    num_games_tied = 0
    for _ in range(num_episodes):
        state = env.reset()
        done = False
        while not done:
            action = dqn_solver.act(env.decode_state(state))
            state, reward, done, info = env.step(action)

            if done and reward == -1:
                num_games_lost += 1
            elif done and reward == 1:
                num_games_won += 1
            elif done and reward == 0:
                num_games_tied += 1

            total_steps += 1


    print(u'Número médio de jogadas por episódio:', 
        total_steps / float(num_episodes))
    print(u'Fração de episódios em que agente perdeu:',
        num_games_lost / float(num_episodes), num_games_lost)
    print(u'Fração de episódios em que agente ganhou:', 
        num_games_won / float(num_episodes), num_games_won)
    print(u'Fração de episódios em que ocorreu empate:', 
        num_games_tied / float(num_episodes), num_games_tied)


def train_model(gamma=0.3):
    """
    Função utilizada para treinar o modelo. Você deve realizar 
    alterações nesta parte do código
    """

    env = TicTacToeEnvironment()
    env.render()
    #Você deve escolher o número de episódios para o treinamento aqui
    num_episodes = 300

    dqn_solver = DQNSolver(env.observation_space.n, env.action_space.n)

    for i in range(1, num_episodes):
        state = env.reset()
        done = False
        while not done:
            #Você deve escrever um procedimento para a escolha da ação aqui
            action = dqn_solver.act(env.decode_state(state))

            #Agente executa a ação escolhida por você. Variável next_state contém o estado obtido
            #após a ação, variável reward contém a recompensa recebida e variável done informa
            #se episódio acabou ou não
            next_state, reward, done, info = env.step(action)
            dqn_solver.remember(env.decode_state(state), 
                action, reward, 
                env.decode_state(next_state), 
                done)

            #Atualizando estado atual
            state = next_state
            dqn_solver.experience_replay()
        
        if i % 10 == 0: print(f"{i} games done")


    return dqn_solver



if __name__ == '__main__':
    #A matriz Q será determinada pelo treinamento que você implementará na função train_model
    dqn_solver = train_model()

    #Esta função avaliará os resultados da tabela Q obtida com o seu modelo.
    evaluate_model(dqn_solver)
    

# %%
