# TEST SCRIPT FOR CLEANING TESTING

import pyautogui
import keyboard
import numpy as np
import random
import time
import magicpy as mp
from Components.update_navigation import UpdateNavigationInfo
from Components.arduino_connection import ArduinoConnection
from Components.update_navigation import UpdateNavigationInfo
from Components import constants as consts, txt_configs as txt

#either pp or intensity
mode = "intensity"
target_status = False
create_navigation_marker = True
debug_arduino_ppTMS = False

ISI_inib = 2.5  # Inter Stimuli Interval [ms]. Ex: ISI=10 refers to 10 ms. Currently is defined by the arduino script, this is only valid for the Arduino Debug option
ISI_exci = 12  # Inter Stimuli Interval [ms]. Ex: ISI=10 refers to 10 ms. Currently is defined by the arduino script, this is only valid for the Arduino Debug option

rmt_intensity = 30

intensity_0 = int(rmt_intensity - rmt_intensity * 0.1)
intensity_1 = int(rmt_intensity)
intensity_2 = int(rmt_intensity + rmt_intensity * 0.1)

intensities = {0: intensity_0,
               1: intensity_1,
               2: intensity_2}

pp_mode = {0: "inibitorio",
           1: "single",
           2: "excitatorio"}

target_intensity = 659, 189
target_stimuli = 490, 60
target_status = False

''' LOAD PULSE TREE CONTEXT SEQUENCE '''
sequence = np.loadtxt('Sequences/random_sequence_300.txt', delimiter=',', dtype='int')
print(sequence)

''' CONNECTION TO NAVIGATION UPDATES '''
updator = UpdateNavigationInfo(1)
updator.connect('169.254.100.20', [5000])

''' CONNECTION WITH MAGVENTURE'''
mp.list_serial_ports()                                              # imprime uma lista de portas disponíveis
input("Portas listadas. Certifique-se de que está conectando na porta correta. Pressione Enter para continuar...")         # Aguarda o usuário clicar Enter para continuar
stimulator = mp.MagVenture("COM1")                                  # Inicializa um objeto que se relaciona ao estimulador
stimulator.connect()
stimulator.set_page('Main', get_response=True)

while True:
    if keyboard.is_pressed('s'):
        break
print("start sequence")
pulse_index = 0
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

print("Pressione 's' para iniciar a sequência ou 'b' para parar a qualquer momento.")

while True:
    if keyboard.is_pressed('s'):
        break
    time.sleep(0.01)

print("Sequência iniciada.")
pulse_index = 0
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

while True:
    # Condições de parada
    if keyboard.is_pressed('b') or pulse_index >= len(sequence):
        print("Sequência parada ou finalizada.")
        break

    # Flag para controlar se o pulso foi bem-sucedido
    pulse_delivered = False

    # O loop principal só roda se o alvo estiver OK.
    if updator.all_target_status:

        start_time = time.time()
        current_pulse_type = pp_mode[sequence[pulse_index]]
        print(f"Alvo detectado. Preparando pulso tipo: {current_pulse_type}")

        params = {}
        if current_pulse_type == "single":
            params = {
                'mode': 'Standard',
                'ipi': 5,  # Valor de exemplo, ajuste se necessário
                'amp_a': int(1.2 * rmt_intensity),
                'amp_b': None
            }
        elif current_pulse_type == "inibitorio":
            params = {
                'mode': 'Dual',
                'ipi': ISI_inib,
                'amp_a': int(0.8 * rmt_intensity),
                'amp_b': int(1.2 * rmt_intensity)
            }
        elif current_pulse_type == "excitatorio":
            params = {
                'mode': 'Dual',
                'ipi': ISI_exci,
                'amp_a': int(0.8 * rmt_intensity),
                'amp_b': int(1.2 * rmt_intensity)
            }

        if params:
            stimulator.set_mode(mode=params['mode'], current_dir='Normal', n_pulses_per_burst=2, ipi=params['ipi'],
                                baratio=80)
            time.sleep(1)

            stimulator.arm(get_response=False)
            time.sleep(1)

            stimulator.set_amplitude(params['amp_a'], b_amp=params['amp_b'], get_response=False)
            time.sleep(1)


            with updator.status_lock:
                if updator.all_target_status:
                    stimulator.fire()
                    pulse_delivered = True

        if pulse_delivered:
            print(f"Pulso {pulse_index + 1}/{len(sequence)} disparado com sucesso!")
            print(f"Tempo de processamento: {(time.time() - start_time):.2f}s")
            pulse_index += 1  # Incrementa o índice APENAS se o pulso foi disparado

            # Pausa entre os estímulos (Inter-Trial Interval)
            print("Aguardando próximo intervalo...")
            time.sleep(random.uniform(3, 5))
        else:
            print("Alvo perdido antes do disparo. Tentando novamente...")
            # Não incrementa o pulse_index, vai tentar o mesmo pulso novamente
            time.sleep(0.1)  # Pequena pausa para não sobrecarregar a CPU

    else:
        # Se o target_status for False, apenas aguarde um pouco
        time.sleep(0.01)

stimulator.disconnect()
print("Script finalizado.")