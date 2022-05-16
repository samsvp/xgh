#%%
import gym
import numpy as np
from tictactoe import TicTacToeEnvironment


def get_best_action(env, q_table, state):
    """Retorna a melhor ação a ser tomada no estado state de acordo com a tabela Q"""
    max_value = np.NINF
    for possible_action in env.get_valid_actions():
        expected_reward = q_table[state][possible_action]
        if expected_reward > max_value:
            action = possible_action
            max_value = expected_reward
    return action


def evaluate_model(q_table):
    """Função utilizada para avaliar modelo obtido"""
    env = TicTacToeEnvironment()

    num_episodes = 5000
    total_steps = 0
    num_games_lost = 0
    num_games_won = 0
    num_games_tied = 0
    for _ in range(num_episodes):
        state = env.reset()
        done = False
        while not done:
            action = get_best_action(env, q_table, state)
            state, reward, done, info = env.step(action)

            if done and reward == -1:
                num_games_lost += 1
            elif done and reward == 1:
                num_games_won += 1
            elif done and reward == 0:
                num_games_tied += 1

            total_steps += 1

    print('Valor da tabela Q para estado inicial:')
    print(q_table[0])
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
    #A matriz Q é inicializada com valores iguais a zero. Você pode experimentar outros valores
    #de inicialização
    q_table = 0 * np.random.randn(env.observation_space.n, env.action_space.n)
    print("q_table: ", q_table)
    #Você deve escolher o número de episódios para o treinamento aqui
    num_episodes = 50_000_000
    for i in range(1, num_episodes):
        state = env.reset()
        done = False
        while not done:
            #Você deve escrever um procedimento para a escolha da ação aqui
            possible_actions = env.get_valid_actions()
            action = get_best_action(env, q_table, state)

            #Agente executa a ação escolhida por você. Variável next_state contém o estado obtido
            #após a ação, variável reward contém a recompensa recebida e variável done informa
            #se episódio acabou ou não
            next_state, reward, done, info = env.step(action)

            #Você deve realizar o treinamento do seu modelo aqui
            q_table[state,action] = reward + gamma * np.max(q_table[next_state])

            #Atualizando estado atual
            state = next_state
        
        if i % 5000 == 0: print(f"{i} games done")


    return q_table



if __name__ == '__main__':
    #A matriz Q será determinada pelo treinamento que você implementará na função train_model
    q_table = train_model()

    #Esta função avaliará os resultados da tabela Q obtida com o seu modelo.
    evaluate_model(q_table)
    
    # with open('q_table.npy', 'wb') as f: # last model
    #     np.save(f, q_table)
# %%
# run the new model
q_table = np.load("q_table.npy")
evaluate_model(q_table)
#%%
env = TicTacToeEnvironment()

state = env.reset()
env.render()
action = get_best_action(env, q_table, state)
state, reward, done, info = env.step(action)
env.render()
# %%
action = get_best_action(env, q_table, state)
state, reward, done, info = env.step(action)
env.render()
# %%
action = get_best_action(env, q_table, state)
state, reward, done, info = env.step(action)
env.render()
# %%
action = get_best_action(env, q_table, state)
state, reward, done, info = env.step(action)
env.render()
# %%
state = env.reset()
state, reward, done, info = env.step(0)
env.render()
action = get_best_action(env, q_table, state)
state, reward, done, info = env.step(action)
env.render()