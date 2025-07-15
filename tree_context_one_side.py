#THIS SCRIPT IS A WORK IN PROGRESS
#DO NOT CONSIDER

import pyautogui
import keyboard
import numpy as np
import random
import time
import magicpy as mp
from Components.arduino_connection import ArduinoConnection
from Components.update_navigation import UpdateNavigationInfo
from Components import constants as consts, txt_configs as txt

''' CHOOSE EXPERIMENTS SETTINGS '''

mode = "pp" #either pp or intensity
target_status = False
debug_arduino_ppTMS = False # True if you want just to check arduino connection
rmt_intensity = 31 # Resint motor treshold of the subject

'For pp mode:'
ISI_inib = 2.5  # Inter Stimuli Interval [ms]. Ex: ISI=10 refers to 10 ms.
ISI_exci = 12

pp_mode = {0: "inibitorio",
           1: "single",
           2: "excitatorio"}

'For intensity mode:'
intensity_0 = int(0.8 * rmt_intensity)
intensity_1 = int(rmt_intensity)
intensity_2 = int(1.2 * rmt_intensity)

intensities = {0: "intensity_0",
               1: "intensity_1",
               2: "intensity_2"}

''' LOAD PULSE TREE CONTEXT SEQUENCE '''
sequence = np.loadtxt('Sequences/tree_sequence_300_LP.txt', delimiter=',', dtype='int')
print(sequence)

''' CONNECTION TO NAVIGATION UPDATES '''
updator = UpdateNavigationInfo(1)
updator.connect('169.254.100.20', [5000])

''' CONNECTION WITH MAGVENTURE'''
mp.list_serial_ports()                                              # imprime uma lista de portas disponíveis
input("Portas listadas. Certifique-se de que está conectando na porta correta. Pressione Enter para continuar...")         # Aguarda o usuário clicar Enter para continuar
stimulator = mp.MagVenture("COM1")                                  # Inicializa um objeto que se relaciona ao estimulador
stimulator.connect()
stimulator.set_page('Main', get_response=False)

''' PRESS S TO START EXPERIMENT WHEN EVERYTHING IS SET'''
print("Aperte a tecla s para iniciar os pulsos...")
while True:
    if keyboard.is_pressed('s'):
        break

print("start sequence")
pulse_index = 0
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

while True:
    if updator.target_status:
        try:
            if mode == "pp":
                start = time.time()
                tipo_estimulo = pp_mode[sequence[pulse_index]]
                print(tipo_estimulo)

                if tipo_estimulo == "single":
                    stimulator.set_mode(mode='Standard', current_dir='Normal', n_pulses_per_burst=2, ipi=5, baratio=80)
                    time.sleep(1)
                    stimulator.arm(get_response=False)
                    time.sleep(1)
                    stimulator.set_amplitude(int(1.2 * rmt_intensity), b_amp=None)
                    time.sleep(1)

                elif tipo_estimulo == "inibitorio":
                    stimulator.set_mode(mode='Dual', current_dir='Normal', n_pulses_per_burst=2, ipi=ISI_inib, baratio=80)
                    time.sleep(1)
                    stimulator.arm(get_response=False)
                    time.sleep(1)
                    stimulator.set_amplitude(int(0.8 * rmt_intensity), b_amp=int(1.2 * rmt_intensity), get_response=False)
                    time.sleep(1)

                elif tipo_estimulo == "excitatorio":
                    stimulator.set_mode(mode='Dual', current_dir='Normal', n_pulses_per_burst=2, ipi=ISI_exci, baratio=80)
                    time.sleep(1)
                    stimulator.arm(get_response=False)
                    time.sleep(1)
                    stimulator.set_amplitude(int(0.8 * rmt_intensity), b_amp=int(1.2 * rmt_intensity), get_response=False)
                    time.sleep(1)

                while not updator.target_status[0]:
                    time.sleep(0.01)

                with updator.status_lock:
                    stimulator.fire()
                    if consts.create_navigation_marker:
                        updator.send_trigger_to_navigation()

            elif mode == "intensity":
                intensidade = intensities[sequence[pulse_index]]
                print(intensidade)

                stimulator.set_mode(mode='Standard', current_dir='Normal', n_pulses_per_burst=2, ipi=5, baratio=80)
                time.sleep(1)
                stimulator.arm(get_response=False)
                time.sleep(1)

                if intensidade == "intensity_0":
                    stimulator.set_amplitude(intensity_0, b_amp=None)
                elif intensidade == "intensity_1":
                    stimulator.set_amplitude(intensity_1, b_amp=None)
                elif intensidade == "intensity_2":
                    stimulator.set_amplitude(intensity_2, b_amp=None)
                time.sleep(1)

                with updator.status_lock:
                    stimulator.fire()
                    if consts.create_navigation_marker:
                        updator.send_trigger_to_navigation()

            print("disparando")
            time.sleep(random.uniform(consts.IPI[0], consts.IPI[1]))

            print("Index do pulso", pulse_index+1)
            pulse_index += 1  # Só incrementa se tudo deu certo

        except Exception as e:
            print(f"\n⚠️ ERRO no pulso {pulse_index}: {e}")
            print("Tentando novamente o mesmo pulso...\n")
            time.sleep(2)  # pequena pausa antes de tentar de novo

    # Tecla B ou fim da sequência
    if keyboard.is_pressed('b') or pulse_index >= len(sequence):
        print("Encerrando sequência.")
        break

    time.sleep(0.01)
