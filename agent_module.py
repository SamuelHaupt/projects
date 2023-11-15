from sb3_contrib import RecurrentPPO
import torch
from datetime import datetime

import risk_management
from risk_management import RiskData
import os
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold


RENDER_DIR = 'render_logs'


class PPOAgentModule:
    def __init__(self, env, model_path=None):
        self.env = env
        self.model_path = model_path
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        if model_path:
            self.model = RecurrentPPO.load(model_path)
        else:
            self.model = RecurrentPPO('MlpLstmPolicy',
                                      env=self.env,
                                      verbose=0,
                                      gamma=0.7,
                                      n_steps=200,
                                      ent_coef=0.01,
                                      learning_rate=0.001,
                                      clip_range=0.1,
                                      batch_size=15,
                                      device=self.device)

    def train(self, total_timesteps):
        """
        Trains the agent for the given number of timesteps.
        Args:
            total_timesteps (int): Number of timesteps to train the agent for.

        Returns:
            None
        """
        print("Using device:", self.device)
        print("Training.")
        # Save model
        model_dir = './models/'
        os.makedirs(model_dir, exist_ok=True)
        curr_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

        # Setup Callback
        stop_callback = StopTrainingOnRewardThreshold(reward_threshold=4.8,
                                                      verbose=1)

        eval_callback = EvalCallback(self.env,
                                     callback_on_new_best=stop_callback,
                                     eval_freq=10000,
                                     best_model_save_path=self.model.save(f"models/{curr_datetime}_ppo_trading_agent")
                                     )

        self.model.learn(total_timesteps=total_timesteps,
                         callback=eval_callback)

        # Save model
        # model_dir = './models/'
        # os.makedirs(model_dir, exist_ok=True)
        # curr_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        # self.model.save(f"models/{curr_datetime}_ppo_trading_agent")
        print("Training complete.")
        print("Model saved at path:",
              f"models/{curr_datetime}_ppo_trading_agent")

    def test(self, test_env, testing_df):
        """
        Tests the agent on the given testing data.
        Args:
            test_env (TradingEnv): Trading environment to test the agent on.
            testing_df (pd.DataFrame): Testing data.
            render_dir (str): Directory to save the render in.

        Returns:
            None
        """
        risk_data = RiskData()
        lstm_states = None
        observation, info = test_env.reset()
        for _ in range(len(testing_df)):
            action, lstm_states = self.model.predict(observation=observation,
                                                     state=lstm_states,
                                                     deterministic=False)

            # If in buy state or hold state with assets held, run risk analysis
            if action == 1 or info["trade_duration"] > 0:
                risk_data.update_risk_data(info)

                # If analysis returns too much risk, change position to sell
                if risk_management.run_risk_analysis(info, risk_data)["too_much_risk"]:
                    print(risk_management.run_risk_analysis(info, risk_data)["risk_reward"])
                    action = -1

            observation, reward, terminated, truncated, info = test_env.step(action)
            if terminated or truncated:
                break

        # Save render
        # if not os.path.exists(RENDER_DIR):
        #     os.makedirs(RENDER_DIR)
        # test_env.get_wrapper_attr('save_for_render')(dir=RENDER_DIR)
        # print(f"Test finished. Render saved in {RENDER_DIR}")
