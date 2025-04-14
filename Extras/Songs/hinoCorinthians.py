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
oled.text("Vai,", 40, 20)
oled.text("Corinthians <3", 10, 40)
oled.show()

# === Notas do hino do Coringão!! ===
notes = [
    262, 247, 196, 330, 330, 330, 330,
    370, 392, 494, 440, 392, 370
]


durations = [
    0.5, 0.52, 0.57, 0.97, 0.9, 0.25, 0.25, 0.2, 0.25, 0.3, 0.3, 0.3, 1
]


# === Função para piscar todos os LEDs em branco a cada nota ===
def show_leds(freq):
    if freq == 0:
        np.fill((0, 0, 0))  # Apaga todos os LEDs
    else:
        np.fill((255, 255, 255))  # Acende todos os LEDs em branco
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

# === Função para tocar a música ===
def play_coringao():
    for note, dur in zip(notes, durations):
        play_tone(note, dur)

# Início do programa
play_coringao()


