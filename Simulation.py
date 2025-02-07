import numpy as np
import concurrent.futures
from simulation_functions import simple_environment, simple_randomized_agent, simple_reflex_agent, SpiralerAgent, run_parallel_simulations

def main():
    n = 100  # Adjust for the environment size
    p = 0.02

    # Run the simulations in parallel for each type of agent
    # randomized_agent_steps = run_parallel_simulations(simple_randomized_agent, n, p)
    # simple_reflex_agent_steps = run_parallel_simulations(simple_reflex_agent, n, p)
    model_based_reflex_agent_steps = run_parallel_simulations(SpiralerAgent, n, p)  # Assuming SpiralerAgent is correctly defined to accept n as init parameter

    # Output the average steps taken to clean the entire environment
    print(f"{n}x{n} Environment")
    # print("Randomized Agent: Average Steps =", np.mean(randomized_agent_steps))
    # print("Simple Reflex Agent: Average Steps =", np.mean(simple_reflex_agent_steps))
    print("Model-based Reflex Agent: Average Steps =", np.mean(model_based_reflex_agent_steps))

if __name__ == "__main__":
    main()

