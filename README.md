# 🔬 Automação e Monitorização IoT (LACOP - UFF)

Este repositório contém os scripts desenvolvidos para o **Laboratório de Controle e Otimização de Processos (LACOP)** da Universidade Federal Fluminense (UFF). O projeto foca-se na automação da recolha, processamento e visualização de dados de sensores em tempo real.

## 🚀 O Problema e a Solução
Antes, a recolha de dados dos equipamentos exigia monitorização manual, consumindo tempo de pesquisa. Criei uma pipeline automatizada que lê os dados dos sensores via protocolo MQTT, processa as informações em Python e envia-as para a nuvem (Firebase), permitindo a monitorização remota e a geração de gráficos de forma automática.

## 🛠️ Tecnologias Utilizadas
* **Python 3** (Lógica principal, processamento de dados e requests)
* **MQTT (Paho)** (Comunicação em tempo real com os sensores/ESP32)
* **Firebase / Cloud** (Armazenamento de dados e histórico)
* **Visualização de Dados** (Geração de gráficos automatizados)

## 📂 Estrutura do Projeto
* `leitor_mqtt.py`: Script principal que atua como *subscriber* no Broker MQTT, recebe os dados de temperatura e faz o POST automático para a API do Firebase.
* `gerador_de_grafico.py`: Processa o histórico de dados recolhidos (como o `dados_temperatura.txt`) e gera gráficos analíticos (`meu_grafico.png`).
* `app_mobile.py`: Interface em desenvolvimento para o acesso e consumo rápido dos dados do laboratório.

## 💡 Impacto
Este sistema economizou horas reais de trabalho manual no laboratório, garantindo maior precisão na recolha de dados e permitindo que a equipa tome decisões baseadas em dados em tempo real.
