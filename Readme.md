# Stock Position Strategy Simulation

This project simulates stock market gains and losses to determine the optimal investment position strategy, particularly focusing on what percentage of assets should be allocated to the stock market.

This program is a re-implementation inspired by: https://www.youtube.com/watch?v=9FlsmNJRSr0

## Getting Started

### Prerequisites
- Python 3.x
- Required packages: Install using `pip install -r requirements.txt`

### Running the Simulation
1. Modify parameters in `simu.py`
2. Run the simulation: `python simu.py`

## Configuration Parameters

- **Win Rate**: Multiplier for winning scenarios (e.g., 2.0 means doubling the investment)
- **Loss Rate**: Multiplier for losing scenarios (e.g., 0.5 means halving the investment)
- **NUM_EXPERIMENTS**: Number of simulation runs, fixed at 100000, no need to change this
- **Flip Range Parameters**: Specifies the range of flips
  - Example: `(100, 501, 100)` runs experiments with flip counts [100, 200, 300, 400, 500]

## Results

The graph below demonstrates a scenario with the following parameters:
- Win Rate: 2.0 (double on win)
- Loss Rate: 0.5 (half on loss)
- Number of Flips: 200

![Percentage Results](results_2.0_0.5/percentage_200.png)

Additional visualizations for different parameter combinations can be found in the `results` folder. The median results are particularly significant for analysis as they provide a more stable measure of central tendency compared to mean values.

## Key Findings

### General Case (Win Rate × Loss Rate = 1.0)
Examples: 1.25 × 0.8 = 1.0, 2.0 × 0.5 = 1.0

- 50% asset allocation maximizes median results (mathematically proven)
- Higher win rates yield better returns (e.g., (2.0, 0.5) outperforms (1.25, 0.8))
- More experiments lead to higher gains (e.g., 400 trials > 200 trials)

### Profitable Scenario (Win Rate × Loss Rate > 1.0)
Example: 1.3 × 0.8 > 1.0

Recommendations:
- Reduce percentage of assets allocated to each bet
- Increase number of trading rounds

### Loss Scenario (Win Rate × Loss Rate < 1.0)
Example: 1.2 × 0.8 < 1.0

Recommendations:
- Minimize percentage of assets per bet
- Reduce number of trading rounds

## Technology Stack
- Python
- NumPy
- [Cursor AI](https://www.cursor.com/)
