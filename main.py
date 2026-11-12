import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# URL real de tu formulario de Microsoft Forms
url = "https://forms.cloud.microsoft/pages/responsepage.aspx?id=FBHdc33vx0CGaVadMufim91zcfqWS2JAsamXsx_S3LZUNjZHM0g1QVlaSVE0Q0Q5Q1Q4UVZSOVdIMC4u&origin=QRCode&route=shorturl"

print("=== Automatizador de Formulario (30 envíos) ===")
input(
    "Presiona ENTER cuando estés listo para que empiece a enviar los"
    " formularios..."
)

options = webdriver.ChromeOptions()
# Si quieres ver el navegador abriéndose y rellenándolo solo, deja esta línea comentada (#).
# Si prefieres que corra oculto, desúntala (--headless).
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.get(url)

total_envios = 30

try:
  for i in range(total_envios):
    print(
        f"\n[Envío {i + 1} de {total_envios}] Rellenando formulario de forma"
        " natural..."
    )
    wait = WebDriverWait(driver, 20)

    # 1. Capturar grupos de opción única (Radio buttons: Edad, Total ropa, Dónde compras)
    radio_groups = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div[role='radiogroup']")
        )
    )

    # --- Edad (Perfil 16-30 años) ---
    if len(radio_groups) >= 1:
      opts_edad = radio_groups[0].find_elements(
          By.CSS_SELECTOR, "input[type='radio']"
      )
      if len(opts_edad) == 3:
        edad_elegida = random.choices(opts_edad, weights=[20, 55, 25], k=1)[0]
        driver.execute_script("arguments[0].click();", edad_elegida)

    # --- Cantidad total de ropa ---
    indice_ropa_total = 1
    if len(radio_groups) >= 2:
      opts_ropa = radio_groups[1].find_elements(
          By.CSS_SELECTOR, "input[type='radio']"
      )
      if opts_ropa:
        indice_ropa_total = random.choices(
            range(len(opts_ropa)), weights=[15, 45, 30, 10], k=1
        )[0]
        driver.execute_script(
            "arguments[0].click();", opts_ropa[indice_ropa_total]
        )

    # --- Dónde compras ---
    if len(radio_groups) >= 3:
      opts_donde = radio_groups[2].find_elements(
          By.CSS_SELECTOR, "input[type='radio']"
      )
      if opts_donde:
        tienda_elegida = random.choices(
            opts_donde, weights=[50, 35, 15], k=1
        )[0]
        driver.execute_script("arguments[0].click();", tienda_elegida)

    # 2. Rellenar campos de texto / numéricos
    text_inputs = driver.find_elements(
        By.CSS_SELECTOR, "input[type='text'], input[type='number']"
    )

    max_limite_sin_usar = [10, 25, 45, 70][min(indice_ropa_total, 3)]
    if len(text_inputs) >= 1:
      sin_usar = random.randint(1, max_limite_sin_usar)
      text_inputs[0].clear()
      text_inputs[0].send_keys(str(sin_usar))

    if len(text_inputs) >= 2:
      compradas_3m = random.choices(
          [0, 1, 2, 3, 4, 5, 6, 8], weights=[10, 20, 25, 20, 12, 7, 4, 2], k=1
      )[0]
      text_inputs[1].clear()
      text_inputs[1].send_keys(str(compradas_3m))

    if len(text_inputs) >= 3:
      necesitadas = random.randint(0, min(compradas_3m, 3))
      text_inputs[2].clear()
      text_inputs[2].send_keys(str(necesitadas))

    if len(text_inputs) >= 4:
      tiempo_uso = f"{random.randint(6, 36)} meses"
      text_inputs[3].clear()
      text_inputs[3].send_keys(tiempo_uso)

    if len(text_inputs) >= 5:
      con_etiqueta = random.choices(
          [0, 1, 2, 3, 4], weights=[50, 30, 12, 5, 3], k=1
      )[0]
      text_inputs[4].clear()
      text_inputs[4].send_keys(str(con_etiqueta))

    # 3. Preguntas de selección múltiple (Checkboxes)
    checkbox_groups = driver.find_elements(
        By.CSS_SELECTOR, "div[role='group']"
    )
    for group in checkbox_groups:
      checkboxes = group.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
      if checkboxes:
        cantidad_a_marcar = random.randint(1, min(3, len(checkboxes)))
        seleccionadas = random.sample(checkboxes, cantidad_a_marcar)
        for cb in seleccionadas:
          driver.execute_script("arguments[0].click();", cb)

    # Pausa simulando que una persona lee y rellena el formulario
    time.sleep(random.uniform(3.0, 6.0))

    # 4. Pulsar el botón de Enviar
    submit_btn = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[@type='submit' or .//span[contains(text(),'Enviar')]]",
            )
        )
    )
    driver.execute_script("arguments[0].click();", submit_btn)
    print("¡Envío realizado con éxito!")

    # 5. Si no es el último, preparar el siguiente haciendo clic en "Enviar otra respuesta"
    if i < total_envios - 1:
      another_btn = wait.until(
          EC.element_to_be_clickable(
              (
                  By.XPATH,
                  "//a[contains(text(), 'Enviar otra respuesta') or"
                  " contains(text(), 'Submit another response')] |"
                  " //button[contains(text(), 'Enviar otra respuesta')]",
              )
          )
      )
      driver.execute_script("arguments[0].click();", another_btn)

      # Pausa realista entre persona y persona (entre 45 segundos y 2 minutos)
      pausa_humana = random.uniform(45.0, 120.0)
      minutos = int(pausa_humana // 60)
      segundos = int(pausa_humana % 60)
      print(
          f"Esperando {minutos}m {segundos}s para simular que otra persona"
          " responde..."
      )
      time.sleep(pausa_humana)

  print("\n¡Los 30 envíos reales se han completado y enviado al formulario!")

except Exception as e:
  print(f"Ha ocurrido un error durante la automatización: {e}")

finally:
  time.sleep(5)
  driver.quit()