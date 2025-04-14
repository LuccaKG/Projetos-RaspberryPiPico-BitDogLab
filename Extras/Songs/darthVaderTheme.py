from machine import Pin, PWM, SoftI2C
from neopixel import NeoPixel
from ssd1306 import SSD1306_I2C
from time import sleep

# === Inicialização ===

# Buzzer no pino GP21
buzzer = PWM(Pin(21))

# Matriz WS2812B (5x5 = 25 LEDs) no pino GP7
np = NeoPixel(Pin(7), 25)

# Display OLED (via I2C: SDA=GP14, SCL=GP15)
i2c = SoftI2C(sda=Pin(14), scl=Pin(15))
oled = SSD1306_I2C(128, 64, i2c)

# === Exibe mensagem personalizada ===
oled.fill(0)
oled.text("Star Wars", 30, 30)
oled.show()

# === Notas da Marcha Imperial (trecho) ===
notes = [
    440, 440, 440, 349, 523, 440, 349, 523, 440, 0,
    659, 659, 659, 698, 523, 415, 349, 523, 440, 0
]

durations = [
    0.5, 0.5, 0.5, 0.35, 0.15, 0.5, 0.35, 0.15, 1.0, 0.5,
    0.5, 0.5, 0.5, 0.35, 0.15, 0.5, 0.35, 0.15, 1.0, 0.5
]

# === Função para mostrar intensidade invertida ===
def show_leds(freq):
    np.fill((0, 0, 0))  # limpa tudo
    if freq == 0:
        np.write()
        return
    # Mapeia frequência para número de LEDs (base invertida)
    min_freq, max_freq = 300, 800
    level = int(25 * (freq - min_freq) / (max_freq - min_freq))
    level = max(0, min(level, 25))
    for i in range(25 - level, 25):  # INVERTE a base
        np[i] = (0, 0, 255)  # azul
    np.write()

# === Função para tocar nota ===
def play_tone(freq, duration):
    if freq == 0:
        buzzer.duty_u16(0)
        show_leds(0)
        sleep(duration)
    else:
        buzzer.freq(freq)
        buzzer.duty_u16(30000)
        show_leds(freq)
        sleep(duration)
        buzzer.duty_u16(0)
        show_leds(0)
        sleep(0.05)

# === Toca a Marcha Imperial ===
def play_imperial_march():
    for note, dur in zip(notes, durations):
        play_tone(note, dur)

# Início do programa
play_imperial_march()

