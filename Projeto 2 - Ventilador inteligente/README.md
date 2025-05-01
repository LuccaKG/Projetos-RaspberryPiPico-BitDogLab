# 🌀 Ventilador Inteligente com BitDogLab, Sensor de Presença e Sensor de Temperatura (BMP280)

Este projeto utiliza a placa educacional **BitDogLab** baseada no **Raspberry Pi Pico (RP2040)** para implementar um sistema de ventilação automática, acionado por **sensor de temperatura (BMP280)** e **sensor de presença PIR (HW-201)**, com visualização em **display OLED SSD1306**.

---

## 📦 Funcionalidades

✅ Lê a temperatura ambiente com o **BMP280**  
✅ Detecta presença com o **sensor PIR HW-201**  
✅ Controla um **motor DC** via **ponte H (L298N)** com **PWM proporcional à temperatura**  
✅ Exibe todas as informações no **display OLED**  
✅ Motor só liga quando há **pessoa presente**

---

## ⚙️ Lógica do sistema

- Se **não houver pessoa presente**, o ventilador permanece **desligado**
- Se **pessoa presente**:
  - Temperatura ≥ 29 °C → ventilador a **100%**
  - 28.5 °C ≤ Temperatura < 29 °C → ventilador a **50%**
  - Temperatura < 28.5 °C → **motor desligado**
    
Obs.: intervalos de temperatura escolhidos apenas por critérios de simplicidade para demonstração.

---

## 🧰 Componentes utilizados

| Componente             | Descrição                         |
|------------------------|-----------------------------------|
| BitDogLab              | Placa com RP2040                  |
| Sensor BMP280          | Temperatura e pressão (I2C)       |
| Sensor PIR HW-201      | Sensor de presença                |
| Ponte H L298N          | Controle de motor DC              |
| Motor DC               | Alimentado com 5–9 V              |
| Display OLED SSD1306   | Interface visual (I2C)            |
| 4 pilhas de 1.5V       | Alimentação de motor     |

---

## 🔌 Ligações principais

### 🧠 BitDogLab

| Pino GPIO | Função                     |
|-----------|----------------------------|
| GP0, GP1  | I2C para BMP280 (SDA, SCL) |
| GP2, GP3  | I2C para OLED (SDA, SCL)   |
| GP16      | PWM ENA (motor)            |
| GP17      | IN1 (motor)                |
| GP18      | IN2 (motor)                |
| GP19      | Leitura do sensor PIR      |

> GND comum entre sensores, motor e placa.

---

## 🖥️ Exemplo de exibição no display OLED

![display_smartFan](https://github.com/user-attachments/assets/610a1987-e9e0-42dc-b8f0-b4e6d5c20675)



## ▶️ Como usar

1. Siga os passos descritos [aqui](https://electrocredible.com/bmp280-raspberry-pi-pico-micropython-guide/) para carregar na RP2040 a biblioteca para uso do BMP280
2. Realize as conexões conforme esquemático abaixo:

[Adicionar esquemático aqui]

3. Rode o código SmartFan.py na **BitDogLab** com o MicroPython.

---

## 📷 Demonstração

Utilizei um ferro de passar para forçar o aquecimento do ambiente e acelerar a demonstração do funcionamento do ventilador a 50% e a 100%.


https://github.com/user-attachments/assets/57ac7680-db3d-418f-8c6a-69a76fe1c044



---

## 📚 Créditos

Projeto criado com base em estudo de controle embarcado, automação e sensores ambientais, usando recursos da **BitDogLab (UNICAMP)**.
