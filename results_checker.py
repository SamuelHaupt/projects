import csv
import matplotlib.pyplot as plt
import numpy as np

def calculate_beat(csv_file_path):
    market_returns = []
    agent_returns = []
    rewards = []
    row_count=0

    # Read the CSV file
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            market_returns.append(float(row['Market Return']))
            agent_returns.append(float(row['Agent Return']))
            rewards.append(float(row['Reward']))
            row_count+=1

    # Calculate the number of times agent return beats market return
    beats_count = sum(agent > market for agent, market in zip(agent_returns, market_returns))

    # Calculate the average beat
    positive_beats = [agent - market for agent, market in zip(agent_returns, market_returns) if agent > market]
    average_beat = sum(positive_beats) / len(positive_beats) if positive_beats else 0

    scatter_plot(agent_returns, market_returns, rewards)
    histogram(agent_returns, market_returns)

    return beats_count, average_beat, row_count

def scatter_plot(agent_returns, market_returns, rewards):
    create_annotation(plt, market_returns[0])

    plt.scatter(agent_returns, rewards, color='blue', marker='o')
    plt.title('Agent Returns vs Rewards')
    plt.xlabel('Agent Returns')
    plt.ylabel('Rewards')
    plt.show()

def histogram(agent_returns, market_returns):
    create_annotation(plt, market_returns[0])
    custom_bins = np.linspace(500, 5000, 20)

    plt.hist(agent_returns, custom_bins, alpha=0.5, label='Agent Returns')
    plt.legend()
    plt.title('Distribution of Returns')
    plt.xlabel('Returns')
    plt.ylabel('Frequency')
    plt.show()

def create_annotation(plt, note):
    note = f"market return = {note}"
    note_x = 0.8  # X-coordinate of the note (adjust as needed)
    note_y = 0.8  # Y-coordinate of the note (adjust as needed)

    plt.annotate(
        note,
        xy=(note_x, note_y),
        xycoords="axes fraction",
        ha="center",
        va="center",
        bbox=dict(boxstyle="round", alpha=0.1),
    )

if __name__ == '__main__':
    # paste path to results csv here
    beats_count, average_beat, row_count = calculate_beat('./results/results_20231118152518')
    
    print(f"Number of times agent return beats market return: {beats_count}/{row_count}")
    if average_beat > 0:
        print(f"Average beat of agent return over market return: {average_beat}")
    else:
        print("Agent beat the market zero times")