import base64
from datetime import datetime
import io
import threading
import time

import flet as ft
import matplotlib
import matplotlib.pyplot as plt
import requests

# Configura o matplotlib para renderização em memória
matplotlib.use("Agg")

# URL do teu Firebase Realtime Database
FIREBASE_URL = (
    "https://iot-temperatura-f4b5e-default-rtdb.firebaseio.com/leituras.json"
)

# Placeholder transparente para inicialização da imagem
EMPTY_IMG = "data:image/png;base64,iVBORw0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAAANSU0KGgoAAA="


def main(page: ft.Page):
  page.title = "IoT Energy & Temp Monitor"
  page.theme_mode = "dark"
  page.padding = 20
  page.scroll = "auto"
  page.window_width = 420
  page.window_height = 750

  temp_text = ft.Text("-- °C", size=46, weight="bold", color="amber")
  time_text = ft.Text("Aguardando dados...", size=13, color="grey400")

  status_badge = ft.Container(
      content=ft.Text("● SISTEMA ONLINE (FIREBASE)", size=11, color="green400"),
      bgcolor="green900",
      padding=6,
      border_radius=8,
  )

  min_temp_text = ft.Text("-- °C", size=16, weight="bold", color="blue300")
  max_temp_text = ft.Text("-- °C", size=16, weight="bold", color="red300")
  avg_temp_text = ft.Text("-- °C", size=16, weight="bold", color="green300")

  chart_image = ft.Image(src=EMPTY_IMG, fit="contain", height=220)

  def gerar_grafico(timestamps, temperaturas):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(5.5, 3), dpi=100)
    fig.patch.set_facecolor("#1e1e2e")
    ax.set_facecolor("#1e1e2e")

    ax.plot(
        timestamps,
        temperaturas,
        color="#ffb74d",
        marker="o",
        linewidth=2.5,
        markersize=5,
    )
    ax.set_title("Variação Térmica Recente (°C)", color="#ffffff", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.2, color="#ffffff")

    plt.xticks(rotation=35, ha="right", fontsize=7, color="#cccccc")
    plt.yticks(fontsize=8, color="#cccccc")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", transparent=True)
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_b64}"

  def atualizar_dados(e=None):
    try:
      resposta = requests.get(FIREBASE_URL)
      if resposta.status_code == 200 and resposta.json():
        dados_firebase = resposta.json()

        temps = []
        times = []
        for item in dados_firebase.values():
          if isinstance(item, dict) and "temperatura" in item:
            temps.append(float(item["temperatura"]))
            hora = item.get("timestamp", "").split(" ")[-1]
            times.append(hora)

        if temps:
          temps_recentes = temps[-12:]
          times_recentes = times[-12:]

          ultimo_val = temps[-1]
          ultimo_tempo = times[-1]

          temp_text.value = f"{ultimo_val:.2f} °C"
          time_text.value = f"Última atualização: {ultimo_tempo}"

          min_temp_text.value = f"{min(temps):.2f} °C"
          max_temp_text.value = f"{max(temps):.2f} °C"
          avg_temp_text.value = f"{sum(temps) / len(temps):.2f} °C"

          chart_image.src = gerar_grafico(times_recentes, temps_recentes)
          page.update()

    except Exception as err:
      print(f"Erro ao buscar dados do Firebase: {err}")

  # Loop de atualização em segundo plano (a cada 3 segundos)
  def loop_tempo_real():
    while True:
      atualizar_dados()
      time.sleep(3)

  card_principal = ft.Card(
      content=ft.Container(
          content=ft.Column(
              [
                  ft.Row([status_badge], alignment="center"),
                  ft.Container(height=5),
                  ft.Text(
                      "TEMPERATURA ATUAL",
                      size=12,
                      color="grey400",
                      weight="w600",
                  ),
                  temp_text,
                  time_text,
              ],
              horizontal_alignment="center",
          ),
          padding=20,
          border_radius=15,
      )
  )

  card_metricas = ft.Row(
      [
          ft.Container(
              content=ft.Column(
                  [ft.Text("MÍNIMA", size=10, color="grey400"), min_temp_text],
                  horizontal_alignment="center",
              ),
              bgcolor="#2a2a3c",
              padding=10,
              border_radius=10,
              expand=True,
          ),
          ft.Container(
              content=ft.Column(
                  [ft.Text("MÉDIA", size=10, color="grey400"), avg_temp_text],
                  horizontal_alignment="center",
              ),
              bgcolor="#2a2a3c",
              padding=10,
              border_radius=10,
              expand=True,
          ),
          ft.Container(
              content=ft.Column(
                  [ft.Text("MÁXIMA", size=10, color="grey400"), max_temp_text],
                  horizontal_alignment="center",
              ),
              bgcolor="#2a2a3c",
              padding=10,
              border_radius=10,
              expand=True,
          ),
      ]
  )

  card_grafico = ft.Card(
      content=ft.Container(
          content=ft.Column(
              [
                  ft.Text(
                      "HISTÓRICO EM TEMPO REAL",
                      size=13,
                      weight="bold",
                      color="amber300",
                  ),
                  chart_image,
              ]
          ),
          padding=15,
          border_radius=15,
      )
  )

  btn_atualizar = ft.Container(
      content=ft.Row(
          [
              ft.Text(
                  "🔄 Atualizar Agora",
                  color="black",
                  weight="bold",
                  size=14,
              )
          ],
          alignment="center",
      ),
      bgcolor="amber",
      padding=12,
      border_radius=10,
      on_click=atualizar_dados,
      ink=True,
  )

  page.add(
      ft.Text("⚡ IoT Monitor", size=22, weight="bold", color="white"),
      card_principal,
      card_metricas,
      card_grafico,
      ft.Row([btn_atualizar], alignment="center"),
  )

  # Inicia a thread de atualização automática em segundo plano
  threading.Thread(target=loop_tempo_real, daemon=True).start()


if __name__ == "__main__":
  ft.run(main)