from machine import Pin, ADC, PWM, SoftI2C
import neopixel
import time
from ssd1306 import SSD1306_I2C  # Biblioteca do display OLED

# === CONFIGURAÇÃO DE COMPONENTES ===

# LEDS e Buzzer
led_red = Pin(12, Pin.OUT)
led_green = Pin(13, Pin.OUT)
buzzer = PWM(Pin(21))

# Neopixel (matriz WS2812B)
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# Joystick
joy_y = ADC(Pin(26))
joy_button = Pin(22, Pin.IN, Pin.PULL_UP)

# Botões
button = Pin(5, Pin.IN, Pin.PULL_UP)       # Botão A
button_b = Pin(6, Pin.IN, Pin.PULL_UP)     # Botão B

# === DISPLAY OLED ===
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

def show_oled(text, subtext=''):
    """Mostra duas linhas centralizadas no display OLED"""
    oled.fill(0)  # Limpa tela
    oled.text(text, 0, 16)
    oled.text(subtext, 0, 40)
    oled.show()

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

def check_interrupt():
    return not button_b.value()

def show_bar_interruptible(duration, mode=""):
    for t in range(duration):
        if check_interrupt():
            return True
        show_progress(t + 1, duration)
        show_oled(f"{mode}", f"Restante: {duration - t}s")
        time.sleep(1)
    return False

# === SELEÇÃO DE TEMPO COM DISPLAY ===
def select_time():
    print("Use o joystick para definir o tempo (5 a 60s).")
    time_selected = 25
    last_state = "center"
    show_progress(time_selected, 60)
    show_oled("Selecione tempo", f"{time_selected} segundos")

    while True:
        val = joy_y.read_u16()

        if val > 50000 and last_state != "up":
            # Agora: joystick para cima → DIMINUI tempo
            if time_selected > 5:
                time_selected -= 1
                show_progress(time_selected, 60)
                show_oled("Selecione tempo", f"{time_selected} segundos")
            last_state = "up"
            time.sleep(0.2)

        elif val < 15000 and last_state != "down":
            # Agora: joystick para baixo → AUMENTA tempo
            if time_selected < 60:
                time_selected += 1
                show_progress(time_selected, 60)
                show_oled("Selecione tempo", f"{time_selected} segundos")
            last_state = "down"
            time.sleep(0.2)


        elif 20000 < val < 45000:
            last_state = "center"

        if not button.value():
            wait_for_button_press()
            return time_selected

        if check_interrupt():
            show_oled("Cancelado", "Voltando...")
            time.sleep(1)
            return None

        time.sleep(0.05)

# === FASE DE ESTUDO ===
def study_phase(study_time):
    show_oled("Estudo iniciado", f"{study_time}s")
    led_red.value(0)
    led_green.value(0)

    if show_bar_interruptible(study_time, "Estudo"):
        show_oled("Interrompido", "Estudo cancelado")
        return True

    led_red.value(1)
    buzzer_alert()
    show_oled("Fim do estudo", "Pressione o botao")

    while button.value():
        if check_interrupt():
            buzzer_stop()
            show_oled("Cancelado", "Estudo interrompido")
            return True
        time.sleep(0.05)

    wait_for_button_press()
    buzzer_stop()
    led_red.value(0)
    led_green.value(1)
    return False

# === FASE DE DESCANSO ===
def rest_phase():
    show_oled("Descanso", "5 segundos")
    if show_bar_interruptible(5, "Descanso"):
        show_oled("Interrompido", "Descanso cancelado")
        return True

    led_green.value(0)
    led_red.value(1)
    buzzer_alert()
    show_oled("Fim do descanso", "Pressione o botao")

    while button.value():
        if check_interrupt():
            buzzer_stop()
            show_oled("Cancelado", "Descanso interrompido")
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
        return True
    if rest_phase():
        return True
    return False

# === LOOP PRINCIPAL ===
while True:
    tempo = None
    while tempo is None:
        tempo = select_time()
    while True:
        interromper = pomodoro_cycle(tempo)
        if interromper:
            break  # Volta para seleção
