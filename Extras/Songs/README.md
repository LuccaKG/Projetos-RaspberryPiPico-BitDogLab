# 🎶 Reproduzindo músicas famosas na BitDogLab

Neste espaço, adicionarei códigos que utilizam o buzzer para reproduzir músicas famosas, como o clássico "Darth Vader Theme Song".

Todos os códigos compartilharão da mesma base, com distinção adicionada no trecho abaixo:

<pre>notes = [
    440, 440, 440, 349, 523, 440, 349, 523, 440, 0,
    659, 659, 659, 698, 523, 415, 349, 523, 440, 0
]

durations = [
    0.5, 0.5, 0.5, 0.35, 0.15, 0.5, 0.35, 0.15, 1.0, 0.5,
    0.5, 0.5, 0.5, 0.35, 0.15, 0.5, 0.35, 0.15, 1.0, 0.5
]</pre>

Cada música terá, obviamente, seu próprio conjunto de notas (representadas pelas suas respectivas frequências) e durações de cada nota.

O maior desafio, então, é conseguir "traduzir" o trecho de música estudado em elementos de *nota* e *duração*.

## 📝 To Do
Criar um script em Python que receba o arquivo de áudio e consiga transcrever suas notas e a duração de cada uma.

