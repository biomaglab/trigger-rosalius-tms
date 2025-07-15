import random
import numpy as np

values = [0, 1, 2]
sequence = [random.choice(values)]
number_of_stimuli = 300

def zero_decision():
    next_prob = random.randrange(100)
    if next_prob <= 30:  # 30% chance de ser 1
        sequence.append(1)
    else:                # 70% chance de ser 2
        sequence.append(2)

def sequence_generator():
    sequence_past = sequence[-2:].copy()
    if sequence_past[-1] == 2:
        sequence.append(1)
    elif sequence_past[-1] == 0:
        zero_decision()
    elif sequence_past[-2] == 0 and sequence_past[-1] == 1:
        sequence.append(1)
    elif sequence_past[-2] == 1 and sequence_past[-1] == 1:
        sequence.append(0)
    elif sequence_past[-2] == 2 and sequence_past[-1] == 1:
        sequence.append(0)
    else:
        print("bug")

if __name__ == "__main__":
    if sequence[0] == 0:
        zero_decision()
    elif sequence[0] == 1:
        sequence.append(1)
    elif sequence[0] == 2:
        sequence.append(1)

    for _ in range(number_of_stimuli - 2):
        sequence_generator()

    print(sequence)
    np.savetxt('tree_sequence_' + str(number_of_stimuli) + '_LP.txt', sequence, delimiter=',', fmt='%d')
