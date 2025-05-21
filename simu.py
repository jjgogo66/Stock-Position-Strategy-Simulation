import numpy as np
import matplotlib.pyplot as plt
import os
from multiprocessing import Pool, cpu_count
from functools import partial

# Simulation parameters
NUM_EXPERIMENTS = 100000  # Number of experiments to run
INITIAL_AMOUNT = 1.0   # Starting amount for both experiments
MAX_AMOUNT = 1e10     # Maximum allowed amount
MIN_AMOUNT = 1e-10    # Minimum allowed amount
BET_PERCENTAGES = np.arange(0, 1.1, 0.1)  # From 0% to 100% in steps of 10%
NUM_PROCESSES = cpu_count()  # Use all available CPU cores
WIN_RATE = 1.25
LOSE_RATE = 0.8

# Flip range parameters
FLIPS_START = 100     # Starting number of flips
FLIPS_END = 501       # Ending number of flips (exclusive)
FLIPS_STEP = 100      # Step size for number of flips

# Create results directory with rates in the name
RESULTS_DIR = f"results_{WIN_RATE}_{LOSE_RATE}"
os.makedirs(RESULTS_DIR, exist_ok=True)

def run_single_experiment(bet_percentage, num_flips):
    """Run a single experiment with given betting percentage"""
    total_amount = INITIAL_AMOUNT
    flips = np.random.choice([True, False], size=num_flips)
    
    for flip in flips:
        bet_amount = total_amount * bet_percentage
        total_amount -= bet_amount
        if flip:  # Positive outcome
            bet_amount *= WIN_RATE
        else:  # Negative outcome
            bet_amount *= LOSE_RATE
        total_amount += bet_amount
    
    return total_amount

def run_experiment_batch(bet_percentage, num_experiments, num_flips):
    """Run a batch of experiments with the same betting percentage"""
    # Set different random seed for each process
    np.random.seed()
    return np.array([run_single_experiment(bet_percentage, num_flips) for _ in range(num_experiments)])

def run_all_experiments(num_flips):
    """Run all experiments in parallel"""
    print(f"Running simulations for {num_flips} flips using {NUM_PROCESSES} CPU cores...")
    
    # Create a partial function with fixed num_experiments and num_flips
    run_batch = partial(run_experiment_batch, num_experiments=NUM_EXPERIMENTS, num_flips=num_flips)
    
    # Run experiments in parallel
    with Pool(processes=NUM_PROCESSES) as pool:
        results_list = pool.map(run_batch, BET_PERCENTAGES)
    
    # Convert results to dictionary
    return {percentage: results for percentage, results in zip(BET_PERCENTAGES, results_list)}

def plot_results(results, num_flips):
    """Create and save the visualization"""
    # Create figure with subplots in 16:9 ratio
    num_rows = 3
    num_cols = 4
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(32, 18))  # 16:9 ratio

    # Add main title with parameters
    main_title = f'Investment Simulation Results\nFlips per Experiment: {num_flips} | Number of Experiments: {NUM_EXPERIMENTS:,} | Initial Amount: ${INITIAL_AMOUNT:.2f}\nWin Rate: {WIN_RATE:.2f} | Lose Rate: {LOSE_RATE:.2f}'
    fig.suptitle(main_title, fontsize=20, y=0.95)

    # Plot histograms for each percentage
    for idx, percentage in enumerate(BET_PERCENTAGES):
        row = idx // num_cols
        col = idx % num_cols
        if row < num_rows:  # Only plot if we have space in the grid
            plot_histogram(axes[row, col], results[percentage], percentage)

    # Remove empty subplot
    fig.delaxes(axes[2, 3])  # Remove the last subplot (we only need 11, not 12)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92, hspace=0.3, wspace=0.2)  # Adjust spacing
    plt.savefig(f'{RESULTS_DIR}/percentage_{num_flips}.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_histogram(ax, data, percentage):
    """Plot a single histogram"""
    # Ensure data is within bounds
    data = np.maximum(data, MIN_AMOUNT)
    data = np.minimum(data, MAX_AMOUNT)
    
    # Create bins at exact powers of 10
    min_exp = int(np.floor(np.log10(MIN_AMOUNT)))
    max_exp = int(np.ceil(np.log10(MAX_AMOUNT)))
    bins = [10**i for i in range(min_exp, max_exp + 1)]
    
    # Plot histogram
    ax.hist(data, bins=bins, edgecolor='black', weights=np.ones_like(data) * 100 / len(data))
    ax.set_xscale('log')
    ax.set_title(f'Betting {percentage*100:.0f}% of Amount', pad=10, fontsize=16)
    ax.set_xlabel('Final Amount (Log Scale)', fontsize=12)
    ax.set_ylabel('Percentage of Experiments (%)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='both', which='major', labelsize=10)
    
    # Set x-axis ticks at powers of 10
    ax.set_xticks(bins)
    ax.set_xticklabels([f'1e{i}' for i in range(min_exp, max_exp + 1)], rotation=45)
    
    # Add statistics to the plot
    stats = f'Mean: {np.mean(data):.2e}\nMedian: {np.median(data):.2e}'
    ax.text(0.95, 0.95, stats, transform=ax.transAxes, 
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
            fontsize=12)

def print_statistics(results, num_flips):
    """Print statistics for all experiments"""
    print(f"\nStatistics for {num_flips} flips:")
    for percentage in BET_PERCENTAGES:
        data = results[percentage]
        print(f"\nBetting {percentage*100:.0f}% of Amount:")
        print(f"Average final amount: {np.mean(data):.2e}")
        print(f"Median final amount: {np.median(data):.2e}")
        print(f"Minimum final amount: {min(data):.2e}")
        print(f"Maximum final amount: {max(data):.2e}")

if __name__ == '__main__':
    # Run simulations for different numbers of flips
    for num_flips in range(FLIPS_START, FLIPS_END, FLIPS_STEP):
        # Run all experiments
        results = run_all_experiments(num_flips)
        
        # Create visualization
        plot_results(results, num_flips)
        
        # Print statistics
        print_statistics(results, num_flips)

'''
def h(total_amount, flip):
    total_amount /= 2.0
    bet_amount = total_amount
    if flip:  # Positive outcome
        bet_amount *= 2.0
    else:  # Negative outcome
        bet_amount /= 2.0
    total_amount += bet_amount  # Win bet_amount
    print(total_amount)
'''