"""
Author: Zach Morgan
Title: State-based Analysis
"""

from collections import defaultdict
from display_complaints import *
from utilities import *

def add_missing(states):
    abbreviations = ["UNK", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN","IA", "KS",
                     "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY","NC", "ND",
                     "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
                     "AS", "MP", "GU", "PR", "VI", "UM", "FM", "MH", "PW", "AA", "AE", "AP", "CM", "CZ", "NB", "PI", "TT"]
    for abbrev in abbreviations:
        if not abbrev in states:
            states[abbrev] = []
    return states

def make_state_map(dataset):
    """

    In the project discussion page professor Steele mentioned that the state map only needs the states present in the dataset, but one of the test program tests for guam with a value of zero in one of the files
    so I was unsure which to do so i included every state abbreviations in order to pass the test. I wrote it so the missing states are added in the other function add_missing so it is easy to comment it out
    if the tests are updated to what professor Steele said on mycourses


    Purpose: creates a dictionary of complaints keyed by the state value
    :param dataset: dictionary of complaints keyed by complaint ID
    :return: state keyed dictionary
    """
    states = defaultdict(list)
    for key in dataset:
        states[dataset[key].State].append(dataset[key])
    states = add_missing(states)
    return states

def list_state_complaints(statemap):
    """
    Purpose: Prints the state dictionary with each state and the amount of entries that state has
    :param statemap: dictionary keyed by states
    :return: NONE
    """
    lst = []
    for key in statemap:
        lst.append((key, len(statemap[key])))
    lst.sort(key = lambda tup: tup[1])
    for index in range(len(lst) - 1,0, -1):
        print(lst[index][0] + ": " + str(lst[index][1]) + " entries")

def query_state_complaints(statemap, statelist, max_count = 10):
    """
    Purpose: Pretty Prints complaint information based on requested parameters
    :param statemap: state dictionary
    :param statelist: list of state abbreviations inputted by the user
    :param max_count: amount of complaints from each state listed
    :return: NONE
    """
    for state in statelist:
        if not state in statemap:
            print("\n" + state + " : no entries ==============================")
        else:
            if len(statemap[state]) < max_count:
                for index in range(len(statemap[state])):
                    print("\n" + "[ " + str(index + 1) + " ]" + state + " ==============================")
                    display_complaint(statemap[state][index])
                print("\n" + "No More Entries for " + state + "==============================")
            else:
                for index in range(max_count):
                    print("\n" + "[ " + str(index + 1) + " ]" + state + " ==============================")
                    display_complaint(statemap[state][index])


def main():
    statemap = make_state_map(read_complaint_data("data/" + input("Enter Consumer Complaints file:")))
    list_state_complaints(statemap)
    state_lst = []
    input_loop = True
    while input_loop:
        state = (input("Enter a State's uppercase US Postal Code (ex. NY) or press ENTER to stop:"))
        state_lst.append(state)
        if state == '':
            input_loop = False
            state_lst.pop(-1)
    count = int(input("Enter how many complaints from each state to display or press ENTER for default value (10):"))
    if count == '':
        query_state_complaints(statemap, state_lst)
    else:
        query_state_complaints(statemap, state_lst, count)

if __name__ == "__main__":
    main()








