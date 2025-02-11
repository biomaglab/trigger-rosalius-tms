import random
import numpy as np

#from trigger_tree_context_ppTMS import number_of_stimuli
stimuli_mode = [0,1, 2, 3,4]
print(len(stimuli_mode))
number_of_stimuli_per_mode= 30
total_number_of_stimuli = number_of_stimuli_per_mode*len(stimuli_mode)
sequence = []

for i in range(len(stimuli_mode)):
    for j in range(number_of_stimuli_per_mode):
        sequence.append(stimuli_mode[i])

random.shuffle(sequence)
sequence_array = np.array(sequence)
print('Generated random sequence:',sequence_array)


np.savetxt('random_sequence_'+str(total_number_of_stimuli)+'.txt', sequence_array, delimiter=',', fmt='%d')
