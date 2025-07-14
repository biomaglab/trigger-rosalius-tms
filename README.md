# trigger-rosalius-tms
This repository holds the code for triggering tms pulses and equipments with the robotic neuronavigated system Rosalius. 

### General organization:
The pulse delivery can be done trhought the Arduino or trhought MagicPy for MagVenture systems.

*Components*: general controls and settings. 

*INO-files*: holds the script for the Arduino control



### Advises for bluetooth connection with Arduino:
If the Bluetooth device is not showing up in your search, follow these steps: <br>
Bluetooth  >  Configurações do dispositivo  >  Descoberta de dispositivos bluetooth  >  Avançado

PIN connection > 1234

When you start the code, the possible connection ports will appear in the terminal plot. Simply test which one is responsible for communication with the trigger.
Alternatively, you can also directly check which port is correct by accessing: <br>
Bluetooth > Mais configurações de bluetooth > Portas COM <br>
The COM port of interest should be the one that shows "direction = output."

When the Bluetooth module stops blinking, it means the connection has been established.
