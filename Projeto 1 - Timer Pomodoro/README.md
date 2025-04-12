# ⏰ Timer Pomodoro

Projeto educacional baseado na placa **BitDogLab** (Raspberry Pi Pico), que implementa a técnica **Pomodoro** de gerenciamento de tempo. O usuário define os tempos de **estudo** e **descanso** usando o joystick, com feedback visual via **OLED** e **matriz de LEDs**, além de sinalização com **buzzer** e **LEDs RGB**.

---

## 🚀 Funcionalidades

- ✅ Seleção do tempo de estudo e descanso via **joystick**
- 🖥️ Visualização em **display OLED** (mensagens e contagens)
- 🔊 Alerta sonoro com **buzzer** ao fim de cada fase
- 💡 Barra de progresso com **matriz WS2812B (Neopixel 5x5)**
- 🔘 Botão A inicia e confirma ações
- ❌ Botão B cancela o ciclo e retorna à seleção de tempo
- 🔁 Ciclo contínuo entre estudo e descanso após cada confirmação

---

## 🛠️ Hardware Utilizado

- 📦 **BitDogLab** (baseado em Raspberry Pi Pico)
- 🎮 **Joystick KY-023** (VRy em GPIO26)
- 🔘 **Botões**:
  - Botão A → GPIO5
  - Botão B → GPIO6
- 🔊 **Buzzer passivo** → GPIO21
- 💡 **Matriz de LEDs WS2812B (5x5)** → GPIO7
- 🖥️ **Display OLED 0.96” I2C (SSD1306)**:
  - SDA → GPIO14
  - SCL → GPIO15
- 🔴🟢 **LED RGB**:
  - Vermelho → GPIO12
  - Verde → GPIO13

---

## 💻 Requisitos de Software

- 📂 Biblioteca `ssd1306.py` copiada para a placa
- ✅ Firmware MicroPython gravado no Raspberry Pi Pico
- ✅ `neopixel` e `machine` disponíveis no ambiente MicroPython

---

## 📋 Como usar

1. Faça o upload dos arquivos `PomoTimer.py` e `ssd1306.py` para a placa.
2. Conecte todos os componentes conforme os pinos indicados.
3. Após iniciar:
   - Use o **joystick vertical** para ajustar os tempos.
   - Pressione o **botão A** para confirmar cada valor.
   - Acompanhe o progresso no **OLED** e nos **LEDs**.
   - Ao final de cada fase, o **buzzer soará**.
   - Pressione o botão A para parar o som e continuar.
   - Pressione o **botão B a qualquer momento** para cancelar o ciclo e redefinir os tempos.

---

## 📷 Ilustração (exemplo de montagem)

![WhatsApp Image 2025-04-12 at 12 20 19](https://github.com/user-attachments/assets/510f6b7f-1e29-44ea-862c-7662511346a0)

Para ver o projeto em ação, confira o vídeo disponível abaixo: 





https://github.com/user-attachments/assets/7773d580-bf6a-4cab-bf5f-90132a93adc8





---

## 📚 Sobre a Técnica Pomodoro

A técnica Pomodoro é um método de produtividade em que você trabalha por períodos focados (geralmente 25 minutos) seguidos de pausas curtas (5 minutos). Isso ajuda a manter a concentração e evita o cansaço mental.

---

## 📄 Licença

Este projeto é de uso educacional e segue a filosofia open hardware/open software do BitDogLab.

---

## 👨‍🏫 Créditos

Projeto desenvolvido com base na plataforma BitDogLab – iniciativa educacional da Unicamp.
