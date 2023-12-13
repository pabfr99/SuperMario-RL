import os

from args import get_args
from agents.ddqn_per import DDQN


import gym
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace
from gym.wrappers import FrameStack
import numpy as np
import torch

from tensorboardX import SummaryWriter


args = get_args()

try:
    os.makedirs(args.log_dir)
except OSError:
    pass


def evaluate(algorithm: str='ddqn',
             episodes: int=5,
             icm: bool=False) -> None:
    """
    Evaluate the agent with the specified algorithm for the specified number of episodes.

    Args:
        - algorithm (str): The algorithm to use to train the agent. Available options are 'ddqn', 'ddqn_per', 'a3c', 'dueling_ddqn', and 'sarsa'. Defaults to 'ddqn'.
        - episodes (int): The number of episodes to train for. Defaults to 5.
    """
    with torch.no_grad():
        if algorithm == 'ddqn':
            agent = DDQN(episodes=episodes, 
                        prioritized=False,
                        icm=icm)
        elif algorithm == 'ddqn_per':
            agent = DDQN(episodes=episodes, 
                        prioritized=True,
                        icm=icm)
        else:
            raise ValueError("Invalid algorithm selected")
    
        agent.load(args.model)
        agent.evaluate(episodes)
    


def train(algorithm: str='ddqn', 
          episodes: int=20000,
          icm: bool=False) -> None:
    """
    Train the agent with the specified algorithm for the specified number of episodes.

    Args:
        - algorithm (str): The algorithm to use to train the agent. Available options are 'ddqn', 'ddqn_per', 'a3c', 'dueling_ddqn', and 'sarsa'. Defaults to 'ddqn'.
        - episodes (int): The number of episodes to train for. Defaults to 20000.
    """
    if algorithm == 'ddqn':
        agent = DDQN(episodes=episodes, 
                     prioritized=False,
                     icm=icm)
    elif algorithm == 'ddqn_per':
        agent = DDQN(episodes=episodes, 
                     prioritized=True,
                     icm=icm)
    else:
        raise ValueError("Invalid algorithm selected")
    
    if args.model != 'False':
        agent.load(args.model)
    agent.train()
    agent.save()

def main():
    tb_writer = SummaryWriter(log_dir=args.save_dir)
    if args.train:
        train(algorithm=args.algorithm,
              episodes=args.episodes,
              icm=args.icm)
    if args.evaluate:
        evaluate(algorithm=args.algorithm, 
                 episodes=args.episodes,
                 icm=args.icm)


if __name__ == '__main__':
    main()
