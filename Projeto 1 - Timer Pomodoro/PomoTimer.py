from machine import Pin, ADC, PWM
import neopixel
import time

# === CONFIGURAÇÃO DE COMPONENTES ===

led_red = Pin(12, Pin.OUT)
led_green = Pin(13, Pin.OUT)
buzzer = PWM(Pin(21))
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

joy_y = ADC(Pin(26))
joy_button = Pin(22, Pin.IN, Pin.PULL_UP)
button = Pin(5, Pin.IN, Pin.PULL_UP)     # Botão A (iniciar/confirma)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)   # Botão B (interromper ciclo)

# === FUNÇÕES AUXILIARES ===

def wait_for_button_press():
    while button.value():
        time.sleep(0.05)
    while not button.value():
        time.sleep(0.05)

def buzzer_alert():
    buzzer.freq(1000)
    buzzer.duty_u16(30000)

def buzzer_stop():
    buzzer.duty_u16(0)

def show_progress(progress, total):
    leds_on = int(NUM_LEDS * progress / total)
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 255) if i < leds_on else (0, 0, 0)
    np.write()

# Novo: função que verifica se botão B foi pressionado (interrompe ciclo)
def check_interrupt():
    return not button_b.value()  # Retorna True se botão B for pressionado

# Contagem com barra e possibilidade de interrupção
def show_bar_interruptible(duration):
    for t in range(duration):
        if check_interrupt():
            return True  # Interrompido
        show_progress(t + 1, duration)
        time.sleep(1)
    return False  # Não interrompido

# Seleção de tempo com joystick (idem antes)
def select_time():
    print("Use o joystick para definir o tempo (5 a 60s).")
    time_selected = 25
    last_state = "center"
    show_progress(time_selected, 60)

    while True:
        val = joy_y.read_u16()

        if val > 50000 and last_state != "up":
            if time_selected < 60:
                time_selected += 1
                print("Tempo:", time_selected, "s")
                show_progress(time_selected, 60)
            last_state = "up"
            time.sleep(0.2)

        elif val < 15000 and last_state != "down":
            if time_selected > 5:
                time_selected -= 1
                print("Tempo:", time_selected, "s")
                show_progress(time_selected, 60)
            last_state = "down"
            time.sleep(0.2)

        elif 20000 < val < 45000:
            last_state = "center"

        if not button.value():
            wait_for_button_press()
            return time_selected

        if check_interrupt():
            print("Botão B pressionado — cancelando seleção...")
            return None

        time.sleep(0.05)

# === FASE DE ESTUDO ===
def study_phase(study_time):
    print(f"Iniciando estudo de {study_time}s")
    led_red.value(0)
    led_green.value(0)

    if show_bar_interruptible(study_time):
        print("Interrompido durante o estudo.")
        return True  # Interrompido

    led_red.value(1)
    buzzer_alert()
    print("Fim do estudo. Pressione o botão para iniciar descanso.")
    
    while button.value():
        if check_interrupt():
            buzzer_stop()
            print("Interrompido durante alarme de estudo.")
            return True
        time.sleep(0.05)

    wait_for_button_press()
    buzzer_stop()
    led_red.value(0)
    led_green.value(1)
    return False  # Não interrompido

# === FASE DE DESCANSO ===
def rest_phase():
    print("Descanso de 5 segundos")

    if show_bar_interruptible(5):
        print("Interrompido durante o descanso.")
        return True

    led_green.value(0)
    led_red.value(1)
    buzzer_alert()
    print("Fim do descanso. Pressione o botão para novo ciclo.")

    while button.value():
        if check_interrupt():
            buzzer_stop()
            print("Interrompido durante alarme de descanso.")
            return True
        time.sleep(0.05)

    wait_for_button_press()
    buzzer_stop()
    led_red.value(0)
    led_green.value(0)
    return False

# === EXECUTA UM CICLO COMPLETO POMODORO ===
def pomodoro_cycle(study_time):
    if study_phase(study_time):
        return True  # Se interrompido, retorna ao seletor
    if rest_phase():
        return True
    return False  # Ciclo completo sem interrupção

# === LOOP PRINCIPAL COM INTERRUPÇÃO POR BOTÃO B ===
while True:
    tempo = None
    while tempo is None:
        tempo = select_time()  # Escolha do tempo
    while True:
        interromper = pomodoro_cycle(tempo)
        if interromper:
            break  # Volta para seleção de tempo
