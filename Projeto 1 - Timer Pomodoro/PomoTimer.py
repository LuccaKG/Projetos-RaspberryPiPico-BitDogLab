# === Pomodoro com BitDogLab ===
# Versao completa com:
# - Controle de tempo de estudo e descanso via joystick
# - Display OLED para feedback visual
# - LEDs e buzzer para sinais
# - Cancelamento do ciclo via botao B

from machine import Pin, ADC, PWM, SoftI2C
import neopixel
import time
from ssd1306 import SSD1306_I2C  # Biblioteca para o display OLED

# === CONFIGURACAO DE HARDWARE ===

# LED RGB (GPIOs 12 e 13)
led_red = Pin(12, Pin.OUT)
led_blue = Pin(13, Pin.OUT)

# Buzzer com PWM (GPIO21)
buzzer = PWM(Pin(21))

# Matriz WS2812B com 25 LEDs no GPIO7
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# Joystick vertical no GPIO26 (analogico)
joy_y = ADC(Pin(26))

# Botao central do joystick e botoes A/B (GPIOs 22, 5, 6)
joy_button = Pin(22, Pin.IN, Pin.PULL_UP)
button = Pin(5, Pin.IN, Pin.PULL_UP)       # Botao A (confirmar)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)     # Botao B (cancelar ciclo)

# Inicializa display OLED via I2C (SDA=GPIO14, SCL=GPIO15)
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

# === FUNCOES DE UTILIDADE ===

def show_oled(text, subtext=''):
    """Mostra duas linhas de texto no display OLED"""
    oled.fill(0)
    oled.text(text, 0, 16)
    oled.text(subtext, 0, 40)
    oled.show()

def wait_for_button_press():
    """Espera o botao A ser pressionado e solto"""
    while button.value():
        time.sleep(0.05)
    while not button.value():
        time.sleep(0.05)

def buzzer_alert():
    """Ativa buzzer com som de 1000Hz"""
    buzzer.freq(1000)
    buzzer.duty_u16(30000)

def buzzer_stop():
    """Silencia o buzzer"""
    buzzer.duty_u16(0)

def show_progress(progress, total):
    """Atualiza a barra de progresso na matriz de LEDs"""
    leds_on = int(NUM_LEDS * progress / total)
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 255) if i < leds_on else (0, 0, 0)
    np.write()

def check_interrupt():
    """Verifica se o botao B foi pressionado para interromper o ciclo"""
    return not button_b.value()

def show_bar_interruptible(duration, mode=""):
    """Executa contagem regressiva com barra de LEDs e possibilidade de interrupcao"""
    for t in range(duration):
        if check_interrupt():
            return True
        show_progress(t + 1, duration)
        show_oled(f"{mode}", f"Restante: {duration - t}s")
        time.sleep(1)
    return False

# === SELECAO DE TEMPO ===

def select_times():
    """Permite definir tempos de estudo e descanso com o joystick"""
    def choose_time(label, initial):
        time_selected = initial
        last_state = "center"
        show_progress(time_selected, 60)
        show_oled(f"{label}", f"{time_selected} segundos")

        while True:
            val = joy_y.read_u16()

            if val > 50000 and last_state != "up":
                if time_selected > 5:
                    time_selected -= 1
                    show_progress(time_selected, 60)
                    show_oled(f"{label}", f"{time_selected} segundos")
                last_state = "up"
                time.sleep(0.2)

            elif val < 15000 and last_state != "down":
                if time_selected < 60:
                    time_selected += 1
                    show_progress(time_selected, 60)
                    show_oled(f"{label}", f"{time_selected} segundos")
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

    tempo_estudo = choose_time("Tempo - estudos", 10)
    if tempo_estudo is None:
        return None, None

    time.sleep(0.5)

    tempo_descanso = choose_time("Tempo - descanso", 5)
    if tempo_descanso is None:
        return None, None

    return tempo_estudo, tempo_descanso

# === FASE DE ESTUDO ===

def study_phase(study_time):
    show_oled("Estudo iniciado", f"{study_time}s")
    led_red.value(0)
    led_blue.value(0)

    if show_bar_interruptible(study_time, "Estudo"):
        show_oled("Interrompido", "Estudo cancelado")
        return True

    led_red.value(1)
    buzzer_alert()
    show_oled("Fim do estudo", "Aperte o botao")

    while button.value():
        if check_interrupt():
            buzzer_stop()
            show_oled("Cancelado", "Estudo interrompido")
            return True
        time.sleep(0.05)

    wait_for_button_press()
    buzzer_stop()
    led_red.value(0)
    led_blue.value(1)
    return False

# === FASE DE DESCANSO ===

def rest_phase(descanso_time):
    show_oled("Descanso", f"{descanso_time} segundos")
    if show_bar_interruptible(descanso_time, "Descanso"):
        show_oled("Interrompido", "Descanso cancelado")
        return True

    led_blue.value(0)
    led_red.value(1)
    buzzer_alert()
    show_oled("Fim do descanso", "Aperte o botao")

    while button.value():
        if check_interrupt():
            buzzer_stop()
            show_oled("Cancelado", "Descanso interrompido")
            return True
        time.sleep(0.05)

    wait_for_button_press()
    buzzer_stop()
    led_red.value(0)
    led_blue.value(0)
    return False

# === CICLO COMPLETO ===

def pomodoro_cycle(tempo_estudo, tempo_descanso):
    if study_phase(tempo_estudo):
        return True
    if rest_phase(tempo_descanso):
        return True
    return False

# === LOOP PRINCIPAL ===

while True:
    tempo_estudo, tempo_descanso = None, None
    while tempo_estudo is None:
        tempo_estudo, tempo_descanso = select_times()

    while True:
        interromper = pomodoro_cycle(tempo_estudo, tempo_descanso)
        if interromper:
            break  # Volta para redefinir os tempos	