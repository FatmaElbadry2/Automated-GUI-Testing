# no of unique states---> in image_states
# no of repeated states---> in image_states[0]
# array of unique states
# coverage
# action count
# no. of bugs
# runtime
# time untill first bug
from global_imports import *

def GetUniqueStatesNum(image_states):
    return len(image_states)

def GetStateOccurences(image_states):
    repitition=[]
    for state in image_states:
        repitition.append(image_states[state][0])
    return repitition

def GetActionVsStateNum(unique_states):
    action_vs_state = {}
    for key in unique_states:
        action_vs_state[key]=len(unique_states[key][0])
    return action_vs_state

def GetCoverage(unique_states):
    all_states=0
    discovered_states=0
    for key in unique_states:
        all_states+=len(unique_states[key][1])
        discovered_states+=len(np.array(unique_states[key][1])[np.array(unique_states[key][1]) >0])
    coverage = (discovered_states/all_states)*100
    return coverage





