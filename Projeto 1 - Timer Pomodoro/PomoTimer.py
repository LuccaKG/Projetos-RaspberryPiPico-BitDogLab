# Importa bibliotecas essenciais
from machine import Pin, ADC, PWM           # Controle de pinos digitais, entrada analógica e PWM
import neopixel                              # Controle da matriz de LEDs WS2812B (Neopixel)
import time                                  # Funções de temporização

# === CONFIGURAÇÃO DOS COMPONENTES ===

# LEDs RGB conectados aos GPIOs 12 (vermelho) e 13 (verde)
led_red = Pin(12, Pin.OUT)
led_green = Pin(13, Pin.OUT)

# Buzzer passivo conectado ao GPIO21 (via transistor)
buzzer = PWM(Pin(21))  # Usa PWM para gerar frequência de som

# Matriz de LEDs WS2812B com 25 LEDs conectada ao GPIO7
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# Joystick KY-023:
joy_y = ADC(Pin(26))  # Eixo vertical (VRy)
joy_button = Pin(22, Pin.IN, Pin.PULL_UP)  # Botão central do joystick

# Botão A (para iniciar, confirmar, parar alarme), conectado ao GPIO5
button = Pin(5, Pin.IN, Pin.PULL_UP)

# === FUNÇÕES AUXILIARES ===

# Aguarda o botão A ser pressionado e solto, com debounce
def wait_for_button_press():
    while button.value():
        time.sleep(0.05)  # Espera enquanto o botão não é pressionado
    while not button.value():
        time.sleep(0.05)  # Espera até que ele seja solto

# Ativa o buzzer com som contínuo a 1000Hz
def buzzer_alert():
    buzzer.freq(1000)
    buzzer.duty_u16(30000)  # Volume moderado (valor PWM entre 0 e 65535)

# Desativa o buzzer
def buzzer_stop():
    buzzer.duty_u16(0)

# Mostra o progresso na matriz de LEDs como uma barra horizontal azul
def show_progress(progress, total):
    leds_on = int(NUM_LEDS * progress / total)  # Calcula quantos LEDs acender
    for i in range(NUM_LEDS):
        if i < leds_on:
            np[i] = (0, 0, 255)  # Azul
        else:
            np[i] = (0, 0, 0)    # Desligado
    np.write()

# Executa a contagem com feedback visual na matriz de LEDs
def show_bar(duration):
    for t in range(duration):
        show_progress(t + 1, duration)
        time.sleep(1)  # Espera 1 segundo por etapa

# Função para selecionar o tempo de estudo com o joystick (um pulso por vez)
def select_time():
    print("Use o joystick para definir o tempo (5 a 60s).")
    time_selected = 25  # Valor inicial padrão
    last_state = "center"  # Armazena último estado do eixo vertical
    show_progress(time_selected, 60)  # Mostra o tempo inicial como barra

    while True:
        val = joy_y.read_u16()  # Lê o valor do eixo vertical (0 a 65535)

        # Pulso para cima → aumenta tempo
        if val > 50000 and last_state != "up":
            if time_selected < 60:
                time_selected += 1
                print("Tempo:", time_selected, "s")
                show_progress(time_selected, 60)
            last_state = "up"
            time.sleep(0.2)  # Debounce

        # Pulso para baixo → reduz tempo
        elif val < 15000 and last_state != "down":
            if time_selected > 5:
                time_selected -= 1
                print("Tempo:", time_selected, "s")
                show_progress(time_selected, 60)
            last_state = "down"
            time.sleep(0.2)  # Debounce

        # Retorna ao centro → pronto para novo comando
        elif 20000 < val < 45000:
            last_state = "center"

        # Pressionar botão A inicia o ciclo com tempo selecionado
        if not button.value():
            wait_for_button_press()
            return time_selected

        time.sleep(0.05)  # Pequena espera para suavizar leitura

# === FASE DE ESTUDO ===
def study_phase(study_time):
    print(f"Iniciando estudo de {study_time}s")
    led_red.value(0)
    led_green.value(0)

    # Conta o tempo com barra de progresso
    show_bar(study_time)

    # Ao fim: LED vermelho e buzzer ativado
    led_red.value(1)
    buzzer_alert()
    print("Fim do estudo. Pressione o botão para iniciar descanso.")

    # Espera usuário apertar botão para parar o som
    wait_for_button_press()
    buzzer_stop()

    # Indica modo descanso com LED verde
    led_red.value(0)
    led_green.value(1)

# === FASE DE DESCANSO ===
def rest_phase():
    print("Descanso de 5 segundos")

    # Mostra barra por 5 segundos
    show_bar(5)

    # Ao fim do descanso: buzzer + LED vermelho
    led_green.value(0)
    led_red.value(1)
    buzzer_alert()
    print("Fim do descanso. Pressione o botão para novo ciclo.")

    # Aguarda botão para encerrar alarme
    wait_for_button_press()
    buzzer_stop()

    # Apaga os LEDs para reinício do ciclo
    led_red.value(0)
    led_green.value(0)

# === EXECUTA UM CICLO COMPLETO POMODORO ===
def pomodoro_cycle(study_time):
    study_phase(study_time)  # Estudo + alarme + confirmação
    rest_phase()             # Descanso + alarme + confirmação

# === LOOP PRINCIPAL ===
while True:
    tempo = select_time()       # Seleciona tempo com o joystick
    while True:
        pomodoro_cycle(tempo)   # Executa o ciclo (estudo + descanso) indefinidamente
