from pathlib import Path
import Components.constants as consts
from Components.constants import DIR_PATH, sequence_file_name

# Directory and name of the sequence file
DIR_PATH = Path(DIR_PATH)
DIR_PATH.mkdir(parents=True, exist_ok=True)
sequence_file = Path(consts.DIR_PATH) / sequence_file_name

# If file exists, append, else, create
if sequence_file.exists():
    mode = 'a'
else:
    sequence_file.touch()
    mode = 'w'

# Start file
file = sequence_file.open(mode)
file.write('')