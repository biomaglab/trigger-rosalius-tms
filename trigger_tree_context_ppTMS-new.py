import time
import keyboard
import random
from Components.arduino_connection import ArduinoConnection
from Components.update_navigation import UpdateNavigationInfo
from Components import constants as consts, txt_configs as txt

'''Connection to Arduino'''
arduino = ArduinoConnection()
arduino.connect('COM3', 9600)

'''Connection to Updator'''
updator = UpdateNavigationInfo(2)
updator.connect('192.168.200.201', [5000, 1000])

pulse_index = 0
target_status = False
create_navigation_marker = True
debug_arduino_ppTMS = False
ISI_measurements = []
ISI =  100 #Inter Stimuli Interval [ms]. Ex: ISI=10 refers to 10 ms. Currently is defined by the arduino script, this is only valid for the Arduino Debug option

start_sequence = True #Futuramente vai ser o botão

while True:

    # This one sends the pulses directly to Arduino, without need of the navigation
    if consts.DEBUG_ARDUINO:
        while pulse_index < consts.STIMULI_NUMBER:
            arduino.send_to_arduino(2)
            time.sleep(2)
            measurements = arduino.read_from_arduino()
            ISI_measurements.append(measurements)
            print(ISI_measurements)
            txt.file.write(f'{measurements}\n')

            #arduino.read_from_arduino()
            pulse_index += 1

        txt.file.close()

    else:
        if not arduino.arduino_connected:
            break

        if consts.START_SEQUENCE or keyboard.is_pressed('s'):
            print("Sequence Started")
            while pulse_index < consts.STIMULI_NUMBER:  #Esse while vai mudar para algo do tipo delivering target on, para poder pausar a sequencia
                print(updator.target_status)
                # if updator.target_status[0] and updator.target_status[1]:
                #     arduino.send_to_arduino(1) #A mensagem se mofifica a partir da escolha do tipo de pulso (Simples, pareado, etc)
                #     print("disparando 1")
                #     time.sleep(random.uniform(4, 6))

                if updator.target_status[0] and updator.target_status[1]:
                    arduino.send_to_arduino(2) #A mensagem se mofifica a partir da escolha do tipo de pulso (Simples, pareado, etc)
                    print("disparando 2")
                    measurements = arduino.read_from_arduino()
                    ISI_measurements.append(measurements)
                    print(ISI_measurements)
                    txt.file.write(f'{measurements}\n')
                    time.sleep(random.uniform(4, 6))


                # if updator.target_status[0] and updator.target_status[1]:
                #     arduino.send_to_arduino(3) #A mensagem se mofifica a partir da escolha do tipo de pulso (Simples, pareado, etc)
                #     print("disparando 3")
                    #time.sleep(random.uniform(4, 6))

                    pulse_index += 1

            txt.file.close()
            arduino.disconnect()
        #hold b key to stop sequence
        if keyboard.is_pressed('b') or pulse_index >= consts.STIMULI_NUMBER:
            break
        time.sleep(0.01)