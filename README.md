# trigger-rosalius-tms
This repository holds the code for triggering tms pulses and equipments with the robotic neuronavigated system Rosalius. 

## Controling TMS pulses is done in two ways:
1) MagicPy: directly controls MagVenture systems through COM2 port.
2) Arduino/ESP: controls through the input/output port.

## General organization:

### Components: general controls and settings.  
1) *arduino_connection* :  functions for connecting to Arduino. It can be through regular cable or bluetooth module
2) *constants* : experiment config constants. Should be edited before experiment
3) *remote_control* : remote control configuration for future connection
4) *txt_configs* :
5) *update_navigation* : updates info from relay server buffer for trigerring pulses

### INO-files:   
1) *TMS_trigger_clean* :  controls single and paired-pulse TMS via serial commands. It triggers pulses on two output pins with configurable ISI and duration. Check pin configuration for each TMS system

### Markers-sequence:   

### Sequences:   Useful for creating stimulus order depending on experimental configuration
1) *context_tree_gen* :  generates context tree sequence
2) *random_seq_gen* : generates random stimuli sequence

### Experiments scripts:   
1) *ppTMS_dual_side* :  
2) *tree_context_one_side* :
3) *trigger_oneside* :


## Advises for bluetooth connection with Arduino:
If the Bluetooth device is not showing up in your search, follow these steps: <br>
Bluetooth  >  Configurações do dispositivo  >  Descoberta de dispositivos bluetooth  >  Avançado

PIN connection > 1234

When you start the code, the possible connection ports will appear in the terminal plot. Simply test which one is responsible for communication with the trigger.
Alternatively, you can also directly check which port is correct by accessing: <br>
Bluetooth > Mais configurações de bluetooth > Portas COM <br>
The COM port of interest should be the one that shows "direction = output."

When the Bluetooth module stops blinking, it means the connection has been established.
