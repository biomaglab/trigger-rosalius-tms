import time
import keyboard
import random
from Components.arduino_connection import ArduinoConnection
from Components.update_navigation import UpdateNavigationInfo
from Components import constants as consts, txt_configs as txt

'''Connection to Arduino'''
arduino = ArduinoConnection()
arduino.connect('COM5', 9600)

'''Connection to Updator'''
updator = UpdateNavigationInfo(1)
updator.connect('192.168.200.202', [5000])

pulse_index = 0

while True:

    #This one sends the pulses direclty to Arduino, without need of the navigation
    if consts.DEBUG_ARDUINO:
        arduino.send_to_arduino(4)
        time.sleep(5)
    else:
        if not arduino.arduino_connected:
            break

        if consts.START_SEQUENCE or keyboard.is_pressed('s'):
            print("Sequence Started")
            while pulse_index < consts.STIMULI_NUMBER:  #Esse while vai mudar para algo do tipo delivering target on, para poder pausar a sequencia
                print(updator.target_status)
                if updator.target_status[0]:
                    arduino.send_to_arduino(1) #A mensagem se mofifica a partir da escolha do tipo de pulso (Simples, pareado, etc)
                    txt.file.write(f'{updator.marker_label[0]}\n')
                    print("disparando "+ str(updator.marker_label[0]) + " __ "+ str(pulse_index))
                    time.sleep(random.uniform(7, 10))
                    pulse_index += 1

            txt.file.close()
            arduino.disconnect()
        #hold b key to stop sequence
        if keyboard.is_pressed('b') or pulse_index >= consts.STIMULI_NUMBER:
            break
        time.sleep(0.01)

