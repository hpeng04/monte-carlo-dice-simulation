import matplotlib.pyplot as plt
import random
import time
import multiprocessing as mp

win_probability = []
end_balance = []

# Dice roll function
def roll_dice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)

    if die1==die2: 
        same_num = True
    else:
        same_num = False
    return same_num  

def read_input():
    num_simulations = int(input("Number of simulations: "))
    max_num_rolls = int(input("Max number of rolls: "))
    bet = int(input("Bet amount: "))

    return num_simulations, max_num_rolls, bet

def simulate(args):
    simulation, num_simulations, max_num_rolls, bet = args

    #Tracking

    balance = [1000]
    num_rolls = [0]
    num_wins = 0
    # Run until the player has rolled 1,000 times
    while num_rolls[-1] < max_num_rolls:
        same = roll_dice()
        # Result if the dice are the same number
        if same:
            balance.append(balance[-1] + 4 * bet)
            num_wins += 1
        # Result if the dice are different numbers
        else:
            balance.append(balance[-1] - bet)

        num_rolls.append(num_rolls[-1] + 1)
    # Store tracking variables and add line to figure
    win_probability.append(num_wins/num_rolls[-1])
    end_balance.append(balance[-1])
    # plt.plot(num_rolls, balance)
    if simulation == num_simulations:
        overall_win_probability = sum(win_probability)/len(win_probability)
        overall_end_balance = sum(end_balance)/len(end_balance)
        print("Average win probability after " + str(num_simulations) + " runs: " + str(overall_win_probability))
        print("Average ending balance after " + str(num_simulations) + " runs: $" + str(overall_end_balance))
    return [num_rolls, balance]

if __name__ == "__main__":
    num_simulations, max_num_rolls, bet = read_input()
    #Plotting

    plt.figure()
    plt.title("Monte Carlo Dice Game [" + str(num_simulations) + " simulations]")
    plt.xlabel("Roll Number")
    plt.ylabel("Balance [$]")
    plt.xlim(0, max_num_rolls)

    processes = mp.cpu_count()
    start = time.time()
    simulations = range(1,num_simulations+1)

    with mp.Pool(processes=processes) as pool:
        results = pool.map(simulate, [(i, num_simulations, max_num_rolls, bet) for i in simulations])

    for result in results:
        num_rolls, balance = result
        plt.plot(num_rolls, balance)
    # for i in range(1, num_simulations+1):
    #     simulate(i, num_simulations, max_num_rolls, bet)
    end = time.time()
    # Averaging win probability and end balance
    print("Time taken: "+str(end-start))
    plt.show()
