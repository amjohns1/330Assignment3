"""
CS 330 Programming Assignment 4
The purpose of this program is to code a state machine as seen in lecture 18 with the additional details provided
in the assignment details page on canvas
Authors: Adam Johnson and Erik Overberg
"""
import random
import os
import datetime

scenario = 1  # Should be 1 or 2
global scenario_iterations, scenario_trace
scenario_trace = True
scenario_iterations = 100
scenario_interval = [1, 10000][scenario - 1]
transition_probability = [[0.8, 0.4, 0.3, 0.4, 0.3, 0.3, 0.8, 0.8, 0.8],
                          [0.9, 0.6, 0.3, 0.2, 0.2, 0.4, 0.7, 0.9, 0.7]][scenario - 1]
state_sequence = [[1, 2, 3, 4, 5, 6, 7], [7, 1, 2, 3, 4, 5, 6]][scenario - 1]
transition_sequence = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [9, 1, 2, 3, 4, 5, 6, 7, 8]][scenario - 1]


# Define support functions.

def write_text(textfile, msg, first=False):
    with open(textfile, 'a') as f:
        if first:
            f.write(msg)
        else:
            f.write(msg + "\n")


def num_width(x, left, right):
    return "{:>{width}.{prec}f}".format(round(x, right), width=left + right + int(right > 0), prec=right)


# Initialize output file and report program begin to output file.


output_file = f"CS 330, State machines, Scenario {scenario} {datetime.date.today()}.txt"

write_text(output_file, f"CS 330, State machines, Begin {datetime.datetime.now()} \n", True)

# Initialize constants used for states.

FOLLOW = 1
PULL_OUT = 2
ACCELERATE = 3
PULL_IN_AHEAD = 4
PULL_IN_BEHIND = 5
DECELERATE = 6
DONE = 7

# Initialize program state and transition counters.

state_count = [0] * 7
transition_count = [0] * 9


# Define state "action" functions (stubs).

def follow_action():
    if scenario_trace:
        write_text(output_file, "state= 1 Follow")

        state_count[FOLLOW - 1] += 1


def pull_out_action():
    if scenario_trace:
        write_text(output_file, "state= 2 Pull out")

        state_count[PULL_OUT - 1] += 1


def accelerate_action():
    if scenario_trace:
        write_text(output_file, "state= 3 Accelerate")

        state_count[ACCELERATE - 1] += 1


def pull_in_ahead_action():
    if scenario_trace:
        write_text(output_file, "state= 4 Pull in ahead")

        state_count[PULL_IN_AHEAD - 1] += 1


def pull_in_behind_action():
    if scenario_trace:
        write_text(output_file, "state= 5 Pull in behind")

        state_count[PULL_IN_BEHIND - 1] += 1


def decelerate_action():
    if scenario_trace:
        write_text(output_file, "state= 6, Decelerate")

        state_count[DECELERATE - 1] += 1


def done_action():
    if scenario_trace:
        write_text(output_file, "state= 7. Done")

        state_count[DONE - 1] += 1


def write_scenario_info(file, scenario_num, trace, iterations, transition_probabilities, state_counts, state_freqs,
                        transition_counts, transition_freqs):
    with open(file, 'a') as f:
        # Write scenario number, trace, and iterations.
        f.write(f"scenario = {scenario_num}\n")
        f.write(f"trace = {trace}\n")
        f.write(f"iterations = {iterations}\n")

        # Write transition probabilities.
        f.write("transition probabilities= ")
        for prob in transition_probabilities:
            f.write(f"{prob} ")
        f.write("\n")

        # Write state counts and frequencies.
        f.write("state counts = ")
        for count in state_counts:
            f.write(f"{count} ")
        f.write("\n")

        f.write("state frequencies = ")
        for freq in state_freqs:
            f.write(f"{freq:.3f} ")
        f.write("\n")

        # Write transition counts and frequencies.
        f.write("transition counts = ")
        for count in transition_counts:
            f.write(f"{count} ")
        f.write("\n")

        f.write("transition frequencies = ")
        for freq in transition_freqs:
            f.write(f"{freq:.3f} ")
        f.write("\n")


def main():
    global scenario_iterations, scenario_trace
    if scenario == 2:
        scenario_trace = False
        scenario_iterations = 1000000
    for i in range(1, scenario_iterations + 1):
        if scenario_trace:
            write_text(output_file, "iteration=" + str(i))

        state = FOLLOW
        follow_action()

        while state != DONE:

            # Get random number between 0 and 1.

            R = random.uniform(0.0, 1.0)

            # Check transitions.

            if state == FOLLOW:
                if R < transition_probability[0]:
                    transition_count[0] += 1
                    state = PULL_OUT
                    pull_out_action()
                else:
                    state = FOLLOW
                    follow_action()

            elif state == PULL_OUT:
                if R < transition_probability[1]:
                    transition_count[1] += 1
                    state = ACCELERATE
                    accelerate_action()
                elif R < sum(transition_probability[1:3]):
                    transition_count[3] += 1
                    state = PULL_IN_BEHIND
                    pull_in_behind_action()
                else:
                    state = PULL_OUT
                    pull_out_action()

            elif state == ACCELERATE:
                if R < transition_probability[2]:
                    transition_count[2] += 1
                    state = PULL_IN_AHEAD
                    pull_in_ahead_action()
                elif R < sum(transition_probability[2:4]):
                    transition_count[4] += 1
                    state = PULL_IN_BEHIND
                    pull_in_behind_action()
                elif R < sum(transition_probability[2:5]):
                    transition_count[5] += 1
                    state = DECELERATE
                    decelerate_action()
                else:
                    state = ACCELERATE
                    accelerate_action()

            elif state == PULL_IN_AHEAD:
                if R < transition_probability[8]:
                    transition_count[8] += 1
                    state = DONE
                    done_action()
                else:
                    state = PULL_IN_AHEAD
                    pull_in_ahead_action()

            elif state == PULL_IN_BEHIND:
                if R < transition_probability[6]:
                    transition_count[6] += 1
                    state = FOLLOW
                    follow_action()
                else:
                    state = PULL_IN_BEHIND
                    pull_in_behind_action()

            elif state == DECELERATE:
                if R < transition_probability[7]:
                    transition_count[7] += 1
                    state = PULL_IN_BEHIND
                    pull_in_behind_action()
                else:
                    state = DECELERATE
                    decelerate_action()

            elif state == DONE:
                print("Error, unexpected state value=", state)
                raise ValueError

            else:
                print("Error, unexpected state value=", state)
                raise ValueError

        if (i % scenario_interval) == 0:
            print("_", end="")

    print("\n")
    state_frequencies = []
    transition_frequencies = []
    for state in state_count:
        state_frequencies.append(state / sum(state_count))
    for transition in transition_count:
        transition_frequencies.append(transition / sum(transition_count))
    write_scenario_info(output_file, scenario, scenario_trace, scenario_iterations, transition_probability, state_count,
                        state_frequencies,
                        transition_count, transition_frequencies)


if __name__ == '__main__':
    # Clear file before writing to it again
    with open(output_file, 'w') as file:
        pass
    main()
    scenario = 2
    main()
