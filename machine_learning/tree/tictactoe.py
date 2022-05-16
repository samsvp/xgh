"""Module containing TicTacToeEnvironment class"""
import numpy as np
from gym import spaces


class TicTacToeEnvironment:
    """
    Class defining an environment where a player chooses actions randomly in a Tic Tac Toe game
    """ 
    def __init__(self):
        self.action_space = spaces.Discrete(9)
        self.observation_space = spaces.Discrete(3**9)
        self.state_ = np.array([0 for _ in range(9)])

    def reset(self):
        """Resets the game state"""
        self.state_ = np.array([0 for _ in range(9)])
        return 0

    def __horizontal_win(self):
        """Checks if a player won horizontally"""
        for i in range(0, 9, 3):
            if self.state_[i] != 0:
                if self.state_[i] == self.state_[i+1] and self.state_[i] == self.state_[i+2]:
                    if self.state_[i] == 1:
                        return True, 1
                    else:
                        return True, -1
        return False, 0

    def __vertical_win(self):
        """Checks if a player won vertically"""
        for i in range(0, 3):
            if self.state_[i] != 0:
                if self.state_[i] == self.state_[i+3] and self.state_[i] == self.state_[i+6]:
                    if self.state_[i] == 1:
                        return True, 1
                    else:
                        return True, -1
        return False, 0

    def __diagonal_win(self):
        """Checks if a player won diagonally"""
        if self.state_[0] != 0:
            if self.state_[0] == self.state_[4] and self.state_[0] == self.state_[8]:
                if self.state_[0] == 1:
                    return True, 1
                else:
                    return True, -1

        if self.state_[2] != 0:
            if self.state_[2] == self.state_[4] and self.state_[2] == self.state_[6]:
                if self.state_[2] == 1:
                    return True, 1
                else:
                    return True, -1
        return False, 0

    def __get_current_state_reward(self):
        """Returns the current state reward and checks if the game ended"""
        done, reward = self.__horizontal_win()
        if done:
            return done, reward

        done, reward = self.__vertical_win()
        if done:
            return done, reward

        done, reward = self.__diagonal_win()
        if done:
            return done, reward

        if len(self.get_valid_actions()) == 0:
            #Tie
            return True, 0
        return False, 0

    def __update_state_from_action(self, action):
        """Updates state based on performed action"""
        self.state_[action] = 1
        return self.__get_current_state_reward()

    def __perform_random_move(self):
        """Performs a random move for the random player"""
        random_action = np.random.choice(self.get_valid_actions())
        self.state_[random_action] = 2
        return self.__get_current_state_reward()

    def encode_state(self, state: np.ndarray) -> int:
        """Returns a numerical representation of a state"""
        base3_elements = [state[i]*3**(len(state)-i-1) for i in range(len(state)-1, -1, -1)]
        return np.sum(base3_elements)

    def decode_state(self, encoded_state: int) -> np.ndarray:
        """Returns a list representation of an encoded state"""
        state = []
        remaining_state = encoded_state
        for i in range(8, 0, -1):
            state.append(remaining_state // 3 ** i)
            remaining_state = remaining_state % 3 ** i
        state.append(remaining_state)
        return np.array(state)

    def get_valid_actions(self):
        """Returns a list with valid actions (possible moves for an agent)"""
        return np.where(self.state_ == 0)[0]

    def render(self, encoded_state=None) -> None:
        """
        Prints an environment state. If no state is passed as argument, prints the current state
        """
        if encoded_state is None:
            state = self.state_
        else:
            state = self.decode_state(encoded_state)

        board = np.array(['-' for _ in range(9)])
        agent_moves = np.where(state == 1)[0]
        board[agent_moves] = 'X'
        random_player_moves = np.where(state == 2)[0]
        board[random_player_moves] = 'O'
        print(board.reshape((3, 3)))

    def step(self, action):
        """Changes environment based on chosen action"""
        done, reward = self.__update_state_from_action(action)
        if done:
            return self.encode_state(self.state_), reward, done, {}

        done, reward = self.__perform_random_move()
        return self.encode_state(self.state_), reward, done, {}