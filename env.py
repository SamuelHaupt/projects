import numpy as np
import pandas as pd
import gymnasium as gym
from gymnasium import spaces
from typing import Any


class AssetTradingEnv(gym.Env):
    metadata = {'render_modes': ['human']}

    def __init__(
            self,
            data_df: pd.DataFrame,
            initial_balance: float = 100_000.00,
            per_trade_weight: float = 0.5,
            render_mode: str = 'human'
            ) -> None:
        super(AssetTradingEnv, self).__init__()
        self.data_df = data_df.copy()
        self.positions = [-1, 0, 1]
        self.sell = self.positions[0]
        self.hold = self.positions[1]
        self.buy = self.positions[2]
        self.initial_balance = initial_balance
        self.per_trade_weight = per_trade_weight
        self.render_mode = render_mode

        self.data_df['date'] = self.data_df.index
        self._features_cols = [col for col in self.data_df.columns
                               if 'feature' in col]
        info_cols = set(self.data_df.columns) - set(self._features_cols)
        extras_cols = {key: index for index, key in enumerate(info_cols)}
        extras_array = np.array(self.data_df[extras_cols.keys()])
        self.history_info_obj = HistoryInfo(extras_cols, extras_array)

        self._step = 0
        self._termination_balance = self.initial_balance * 0.05
        self._max_episode_steps = len(self.data_df) - 1
        self._obs_array = np.array(self.data_df[self._features_cols],
                                   dtype=np.float32)
        self._asset_price_array = np.array(self.data_df['close'])

        shape = len(self._features_cols)
        self.observation_space =\
            spaces.Box(low=0, high=1,
                       shape=(shape,))
        self.action_space = spaces.Discrete(len(self.positions))

    def reset(self, seed=None, options=None):
        # super().reset(seed=seed, options=options)
        # self.current_trade_position = self.np_random.choice(self.positions)
        # If randomized, ensure purchase price is updated correctly.

        self.current_trade_position = 0.
        self._step = 0
        self.history_info_obj.add_info(
            step=self._step,
            portfolio_balance=self.initial_balance,
            available_funds=self.initial_balance,
            unrealized_trade=0.,
            position=0.,
            purchase_close_price=0.,
            step_reward=0.,
            total_reward=0.)

        observation = self._get_obs()
        info = self._get_info()
        return observation, info

    def step(self, action):
        self._step += 1
        portfolio_balance, available_funds, unrealized_trade, position, \
            purchase_close_price = self._update_portfolio(action)
        self.history_info_obj.add_info(
            step=self._step,
            portfolio_balance=portfolio_balance,
            available_funds=available_funds,
            unrealized_trade=unrealized_trade,
            position=position,
            purchase_close_price=purchase_close_price,
            step_reward=0.,
            total_reward=0.)

        # reward function here

        observation = self._get_obs()
        reward = self._get_reward()
        terminated = False if portfolio_balance > self._termination_balance\
            else True
        truncated = False if self._step < self._max_episode_steps else True
        info = self._get_info()
        return observation, reward, terminated, truncated, info

    def render(self):
        pass

    def close(self):
        pass

    def _update_portfolio(self, action: int):
        previous_step = self._step - 1
        portfolio_balance = self.history_info_obj.get_step_and_col(
            previous_step, 'portfolio_balance')
        available_funds = self.history_info_obj.get_step_and_col(
            previous_step, 'available_funds')
        unrealized_trade = self.history_info_obj.get_step_and_col(
            previous_step, 'unrealized_trade')
        purchase_close_price = self.history_info_obj.get_step_and_col(
            previous_step, 'purchase_close_price')
        position = self.history_info_obj.get_step_and_col(
            previous_step, 'position')
        _close_price = self._asset_price_array[self._step]

        if position >= 1:
            if action == self.hold:
                unrealized_trade = round(_close_price * position, 2)
                portfolio_balance = round(available_funds
                                          + unrealized_trade, 2)
            if action == self.sell:
                unrealized_trade = round(_close_price * position, 2)
                portfolio_balance = round(available_funds
                                          + unrealized_trade, 2)
                available_funds = round(available_funds + unrealized_trade, 2)
                unrealized_trade = 0.
                position = 0.
                purchase_close_price = 0.
        elif action == self.buy:
            unrealized_trade = round(self.per_trade_weight
                                     * available_funds, 2)
            purchase_close_price = round(_close_price, 2)
            position = round(unrealized_trade / purchase_close_price, 2)
            available_funds = round(available_funds - unrealized_trade, 2)
            portfolio_balance = round(available_funds + unrealized_trade, 2)

        return portfolio_balance, available_funds, unrealized_trade, \
            position, purchase_close_price

    def _get_obs(self):
        obs = self._obs_array[self._step]
        return obs

    def _get_info(self):
        info = self.history_info_obj.get_step(self._step)
        return info

    def _get_reward(self):
        return None


class HistoryInfo():
    def __init__(self, extras_cols: dict, extras_array: np.array) -> None:
        self._extras_cols = extras_cols
        self._extras_array = extras_array
        self._history_info_dict = dict()

    def get_extras_data_col(self, step: int, col_name: str):
        row_index = self._extras_cols[col_name]
        return self._extras_array[step, row_index]

    def add_info(
            self,
            step: int,
            portfolio_balance: float,
            available_funds: float,
            unrealized_trade: float,
            position: float,
            purchase_close_price: float,
            step_reward: float,
            total_reward: float
            ) -> None:

        date = self.get_extras_data_col(step, 'date')
        close = self.get_extras_data_col(step, 'close')
        open = self.get_extras_data_col(step, 'open')
        low = self.get_extras_data_col(step, 'low')
        high = self.get_extras_data_col(step, 'high')
        volume = self.get_extras_data_col(step, 'volume')

        step_info = {'step': step,
                     'date': date,
                     'portfolio_balance': portfolio_balance,
                     'available_funds': available_funds,
                     'unrealized_trade': unrealized_trade,
                     'position': position,
                     'purchase_close_price': purchase_close_price,
                     'step_reward': step_reward,
                     'total_reward': total_reward,
                     'close': close,
                     'open': open,
                     'low': low,
                     'high': high,
                     'volume': volume}

        self._history_info_dict[step] = step_info

    def get_step(self, step: int) -> dict:
        return self._history_info_dict[step]

    def get_step_and_col(self, step: int, col_name: str) -> Any:
        step_dict = self.get_step(step)
        return step_dict[col_name]


if __name__ == '__main__':
    from data_processor import DataProcessor
    import random
    dp = DataProcessor()
    symbol = 'TQQQ'
    start_date = '2010-02-11'
    stop_date = '2023-11-30'
    tqqq = dp.download_data_df_from_yf(symbol, start_date, stop_date)
    preprocessed_df = dp.preprocess_data(tqqq)
    env = AssetTradingEnv(preprocessed_df)
    obs, info = env.reset()
    print(info)
    random.seed(1)
    for index in range(15):
        choice = random.choice([-1, 0, 1])
        print()
        print(f"Choice: {choice}")
        observation, reward, terminated, truncated, info = env.step(choice)
        for key, value in info.items():
            print(key, ": ", value)
