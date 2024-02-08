# This file contains the options that you should modify to solve Question 2

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    # In this case:
    # ==> we want the policy to seek the near terminal state (reward +1) via the short dangerous path (moving besides the row of -10 state)
    # ==> we will make the living reward -3 so that the agent will try to reach the terminal state as soon as possible
    # ==> we will make the discount factor 1 so that the agent will not care about the future rewards
    # ==> we will make the the environment stochastic so that the agent will not be able to reach the terminal state via the long safe path
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -3
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    # ==> we want the policy to seek the near terminal state (reward +1) via the long safe path (moving away from the row of -10 state)
    # ==> we will make the living reward -0.04 (small -ve number) 
    # ==> we will make the discount factor 0.2 so that the agent will care about the future rewards
    # ==> he will choose the small exit (reward +1) over the big exit (reward +10) because the small exit is closer to the terminal state
    return {
        "noise": 0.2,
        "discount_factor": 0.2,
        "living_reward": -0.04
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    # ==> we want the policy to seek the far terminal state (reward +10) via the short dangerous path (moving besides the row of -10 state)
    # ==> we will make the living reward -2 so that the agent will try to reach the terminal state as soon as possible
    # ==> we will make the discount factor 1 so that the agent will not care about the future rewards
    # ==> we will make the the environment stochastic so that the agent will not be able to reach the terminal state via the long safe path
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -2
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
    # ==> we want the policy to seek the far terminal state (reward +10) via the long safe path (moving away from the row of -10 state)
    # ==> we will make the living reward -0.1 (small -ve number)
    # ==> we will make the discount factor 1 so that the agent will not care about the future rewards
    # ==> he will choose the big exit (reward +10) over the small exit (reward +1) because the big exit is closer to the terminal state
        return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.1
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    # ==> we want the policy to avoid any terminal state and keep the episode going on forever
    # ==> we will make the living reward 0.1 (small +ve number)
    # ==> we will make the discount factor 1 so that the agent will not care about the future rewards
    # ==> we will make the the environment deterministic
    return {
        "noise": 0.0,
        "discount_factor": 1.0,
        "living_reward": 0.1
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    # ==> we want the policy to seek any terminal state (even ones with the -10 penalty) and try to end the episode in the shortest time possible
    # ==> we will make the living reward -20 (large -ve number)
    # ==> we will make the discount factor 1 so that the agent will not care about the future rewards
    # ==> we will make the the environment deterministic
    return {
        "noise": 0.0,
        "discount_factor": 1.0,
        "living_reward": -20
    }