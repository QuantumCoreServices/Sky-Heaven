import gym
import numpy as np
import torch
from stable_baselines3 import PPO
from trading_bot import execute_trade

class TradingEnv(gym.Env):
    def __init__(self, historical_data):
        super(TradingEnv, self).__init__()
        self.historical_data = historical_data
        self.current_step = 0

    def step(self, action):
        reward = 0
        if action == 1:
            execute_trade(self.historical_data["symbol"][self.current_step], "BUY")
            reward = self.historical_data["profit"][self.current_step]
        elif action == 2:
            execute_trade(self.historical_data["symbol"][self.current_step], "SELL")
            reward = -self.historical_data["loss"][self.current_step]

        self.current_step += 1
        done = self.current_step >= len(self.historical_data)
        return np.array([self.current_step]), reward, done, {}

    def reset(self):
        self.current_step = 0
        return np.array([self.current_step])

def train_rl_model(data):
    env = TradingEnv(data)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    return model

# Train the model
if __name__ == "__main__":
    data = {
        "symbol": ["BTCUSDT", "ETHUSDT", "ADAUSDT"],
        "profit": [10, 5, 3],
        "loss": [-5, -2, -1]
    }
    trained_model = train_rl_model(data)
    trained_model.save("ai_trading_model")
