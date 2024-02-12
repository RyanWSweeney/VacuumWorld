# Define a wrapper function for running a single simulation
# Your code and description goes here
import numpy as np
import random
import concurrent.futures

actions = ["north", "east", "west", "south", "suck"]
def create_environment(n, p):
    environment = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if random.random() < p:
                environment[i][j] = 1
    return environment


def print_environment(environment, position):
    n = len(environment)
    for i in range(n):
        for j in range(n):
            if (i, j) == position:
                print("X", end=" ")
            elif environment[i][j] == 1:
                print("D", end=" ")
            else:
                print("C", end=" ")
        print()


def simple_environment(agent, n, p, verbose=False):
    environment = create_environment(n, p)
    num_cleaned = 0
    steps = 0  # Initialize steps counter
    position = (random.randint(0, n - 1), random.randint(0, n - 1))
    total_dirty = np.sum(environment)  # Count total dirty cells initially

    if (verbose): print_environment(environment, position)

    while num_cleaned < total_dirty:  # Continue until all dirty cells are cleaned
        dirty = environment[position[0]][position[1]] == 1
        bumpers = {"north": position[0] == 0, "south": position[0] == n - 1, "west": position[1] == 0,
                   "east": position[1] == n - 1}

        action = agent(bumpers, dirty, n)
        if (verbose): print("step", steps, "- action:", action)

        if (action == "suck"):
            if dirty:  # Only increment num_cleaned if the cell was dirty
                environment[position[0]][position[1]] = 0
                num_cleaned += 1
        else:
            if action == "north" and not bumpers["north"]:
                position = (position[0] - 1, position[1])
            elif action == "south" and not bumpers["south"]:
                position = (position[0] + 1, position[1])
            elif action == "west" and not bumpers["west"]:
                position = (position[0], position[1] - 1)
            elif action == "east" and not bumpers["east"]:
                position = (position[0], position[1] + 1)

        steps += 1  # Increment steps for every action taken

    if (verbose): print_environment(environment, position)
    return steps  # Return the total number of steps taken as performance measure

def simple_randomized_agent(bumpers, dirty, n):
    return np.random.choice(actions)

def simple_reflex_agent(bumpers, dirty, n):
    #note I insert n but do not use it so all agents are compatible with the environment
    if dirty:
        return "suck"
    else:
        # Randomly choose a direction that is not blocked
        while True:
            action = np.random.choice(["north", "east", "west", "south"])
            if not bumpers[action]:
                return action


class SpiralerAgent:
    def __init__(self, n):
        self.n = n  # Environment size
        self.position = (random.randint(0, n - 1), random.randint(0, n - 1))  # Random start position
        self.orientation = 'North'
        self.visited = set()  # Keep track of visited cells
        self.mode = 'Find Wall'
        self.steps_since_last_turn = 0  # Steps taken in the current direction
        self.steps_allowed = n - 1  # Max steps allowed in the current spiral arm
        self.turns_made = 0  # Turns made since the last decrease in steps_allowed

    def update_orientation_for_spiral(self):
        # Adjust the agent's orientation for spiraling: turn right
        orientation_order = ['North', 'East', 'South', 'West']
        current_index = orientation_order.index(self.orientation)
        self.orientation = orientation_order[(current_index + 1) % 4]  # Turn right
        self.turns_made += 1
        # Every 2 turns, reduce the steps allowed in the current direction to tighten the spiral
        if self.turns_made % 3 == 0:
            self.steps_allowed -= 1
        self.steps_since_last_turn = 0  # Reset counter after each turn

    def can_move(self, bumpers):
        # Check if the agent can move forward in its current orientation without hitting a wall
        return not bumpers[self.orientation.lower()] and self.steps_since_last_turn < self.steps_allowed

    def decide_action(self, bumpers, dirty, n):
        if dirty:
            return "suck"

        if self.mode == 'Find Wall':
            if any(bumpers.values()):
                self.mode = 'Spiral Inwards'
                self.update_orientation_for_spiral()
            else:
                return self.orientation.lower()

        if self.mode == 'Spiral Inwards':
            if self.can_move(bumpers):
                self.steps_since_last_turn += 1  # Increment steps taken in the current direction
                return self.orientation.lower()
            else:
                self.update_orientation_for_spiral()  # Turn right when facing a wall or reaching steps limit
                return self.orientation.lower()

        # Default action if none above apply
        return "north"

    def __call__(self, bumpers, dirty, n):
        return self.decide_action(bumpers, dirty, n)

def run_simulation(agent_func, n, p):
    if agent_func.__name__ == 'SpiralerAgent':
        agent = agent_func(n)  # Instantiate SpiralerAgent for each simulation
    else:
        agent = agent_func
    return simple_environment(agent, n, p, verbose=False)

def run_parallel_simulations(agent_func, n, p, num_simulations=100):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Launch simulations in parallel
        futures = [executor.submit(run_simulation, agent_func, n, p) for _ in range(num_simulations)]
        # Collect the results as they complete
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    return results