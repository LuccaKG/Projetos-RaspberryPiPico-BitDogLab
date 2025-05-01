from machine import Pin, I2C, PWM, SoftI2C
from ssd1306 import SSD1306_I2C
from bmp280 import *
import time

# === Configura display OLED ===
i2c = SoftI2C(sda=Pin(2), scl=Pin(3))
oled = SSD1306_I2C(128, 64, i2c)

# === Configura sensor de temperatura - BMP280 ===
sdaPIN = Pin(0)
sclPIN = Pin(1)
bus = I2C(0, sda=sdaPIN, scl=sclPIN, freq=400000)
time.sleep(1)
bmp = BMP280(bus)
bmp.use_case(BMP280_CASE_INDOOR)

# === Configura GPIOs do motor ===
ena = PWM(Pin(16))        # PWM no pino ENA
ena.freq(1000)            # Frequência de 1 kHz
in1 = Pin(17, Pin.OUT)    # Direção
in2 = Pin(18, Pin.OUT)    # Direção oposta

# Sensor de presença HW-201 no pino GP19
pir = Pin(19, Pin.IN)

# === Loop principal ===
while True:
    temperature = bmp.temperature

    oled.fill(0)
    oled.text(f"Temp.: {temperature:.1f} C", 0, 0)
    if pir.value() == 0:
        if (temperature >= 29):
            oled.text("Pessoa presente!", 0, 16)
            oled.text("Ventilador: 100%", 0, 30)
            in1.high()
            in2.low()
            ena.duty_u16(65535)  # 100% potência

        elif temperature >= 28.5:
            oled.text("Pessoa presente!", 0, 16)
            oled.text("Ventilador: 50%", 0, 30)
            in1.high()
            in2.low()
            ena.duty_u16(int(65535 * 0.5))  # 50% potência

        else:
            oled.text("Pessoa presente!", 0, 16)
            oled.text("Ventilador: OFF", 0, 30)
            ena.duty_u16(0)  # desliga motor
    else:
        oled.text("Pessoa ausente!", 0, 16)
        oled.text("Ventilador: OFF", 0, 30)
        ena.duty_u16(0)
        

    oled.show()
    time.sleep(1)


