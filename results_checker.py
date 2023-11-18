import csv

def calculate_beat(csv_file_path):
    market_returns = []
    agent_returns = []
    row_count=0

    # Read the CSV file
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            market_returns.append(float(row['Market Return']))
            agent_returns.append(float(row['Agent Return']))
            row_count+=1

    # Calculate the number of times agent return beats market return
    beats_count = sum(agent > market for agent, market in zip(agent_returns, market_returns))

    # Calculate the average beat
    average_beat = sum(agent - market for agent, market in zip(agent_returns, market_returns)) / len(agent_returns)

    return beats_count, average_beat, row_count

if __name__ == '__main__':
    # paste path to results csv here
    beats_count, average_beat, row_count = calculate_beat('./results/risk_only_reward_training')
    
    print(f"Number of times agent return beats market return: {beats_count}/{row_count}")
    print(f"Average beat of agent return over market return: {average_beat}")