from pathlib import Path

# Directory and name of the sequence file
sequence_file_name = 'test.txt'
sequence_file = Path('../Markers-sequence') / sequence_file_name

# If file exists, append, else, create
if sequence_file.exists():
    mode = 'a'
else:
    mode = 'w'

# Start file
file = sequence_file.open(mode)
file.write('\n')