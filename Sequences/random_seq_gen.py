import random
import numpy as np
import pandas as pd

fixed_number_of_stimuli =  False

if fixed_number_of_stimuli:
    #from trigger_tree_context_ppTMS import number_of_stimuli
    stimuli_mode = [0,1, 2]
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

else:
    #LOAD SEQUENCE TREE
    sequence_tree = np.loadtxt('sequence_100.txt', delimiter=',', dtype='int')
    contagem = pd.Series(sequence_tree).value_counts().sort_index()
    sequence = np.array([key for key, val in contagem.items() for _ in range(val)])
    np.random.shuffle(sequence)
    print(sequence)
    print(contagem)
    sequence_array = np.array(sequence)
    np.savetxt('random_sequence_'+'.txt', sequence_array, delimiter=',', fmt='%d')