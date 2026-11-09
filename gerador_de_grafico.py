import matplotlib.pyplot as plt
from datetime import datetime

# Cria listas vazias para guardar o tempo (eixo X) e a temperatura (eixo Y)
tempos = []
temperaturas = []

# Tenta abrir e ler o arquivo de texto
try:
    with open("dados_temperatura.txt", "r") as arquivo:
        linhas = arquivo.readlines()
        
        for linha in linhas:
            # Pula linhas vazias por precaução
            if linha.strip() == "":
                continue
                
            # O texto está assim: "2026-08-19 23:15:00,25.50"
            # O split(",") corta exatamente na vírgula!
            partes = linha.strip().split(",")
            
            # Converte a parte da data para um objeto de tempo do Python
            data_hora = datetime.strptime(partes[0], "%Y-%m-%d %H:%M:%S")
            # Converte a parte da temperatura de texto para número decimal (float)
            temp = float(partes[1])
            
            # Adiciona os valores prontos nas nossas listas
            tempos.append(data_hora)
            temperaturas.append(temp)
    
    # Prepara a tela (tamanho 10x5 polegadas)
    plt.figure(figsize=(10, 5))
    
    # Desenha a linha (X=tempos, Y=temperaturas, com bolinhas vermelhas)
    plt.plot(tempos, temperaturas, marker='o', linestyle='-', color='red')
    
    # Adiciona títulos
    plt.title("Evolução da Temperatura (ESP32 via MQTT)")
    plt.xlabel("Tempo")
    plt.ylabel("Temperatura (°C)")
    
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    
    # 1. Avisa no terminal que chegou até aqui
    print(f"Desenhando o gráfico com {len(tempos)} leituras...")
    
    # 2. Salva uma foto do gráfico na mesma pasta!
    plt.savefig("meu_grafico.png")
    print("Sucesso! Verifique o arquivo 'meu_grafico.png' na sua pasta.")
    
    # Tenta mostrar a janela
    plt.show()

except FileNotFoundError:
    print("Erro: O arquivo 'dados_temperatura.txt' ainda não foi encontrado!")