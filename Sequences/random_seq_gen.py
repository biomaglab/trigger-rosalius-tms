import random
import numpy as np

stimuli_mode = [0, 1, 2, 3]
number_of_stimuli_per_mode = 5
total_number_of_stimuli = number_of_stimuli_per_mode * len(stimuli_mode)

if __name__ == "__main__":
    sequence = []
    for i in range(len(stimuli_mode)):
        for j in range(number_of_stimuli_per_mode):
            sequence.append(stimuli_mode[i])

    random.shuffle(sequence)
    sequence_array = np.array(sequence)
    print('Generated random sequence:', sequence_array)

    np.savetxt('random_sequence_' + str(total_number_of_stimuli) + '.txt', sequence_array, delimiter=',', fmt='%d')
