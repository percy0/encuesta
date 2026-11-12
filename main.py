import os
import random
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# URL real de tu formulario de Microsoft Forms
url = "https://forms.cloud.microsoft/pages/responsepage.aspx?id=FBHdc33vx0CGaVadMufim91zcfqWS2JAsamXsx_S3LZUNjZHM0g1QVlaSVE0Q0Q5Q1Q4UVZSOVdIMC4u&origin=QRCode&route=shorturl"

# Crear carpeta para guardar comprobantes si no existe
os.makedirs("comprobantes_envios", exist_ok=True)

print("=== Automatizador de Formulario (Modo Seguro) ===")
input("Presiona ENTER cuando estés listo para empezar...")

try:
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Descomenta si quieres que corra oculto sin abrir ventanas

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    total_envios = 30

    for i in range(total_envios):
        num_envio = i + 1
        print("\n--------------------------------------------------")
        print(f"Iniciando proceso del [Envio {num_envio} de {total_envios}]...")
        print("--------------------------------------------------")
        
        wait = WebDriverWait(driver, 20)

        # Esperar a que cargue el formulario
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='form'], form, div.office-form")))

        # 1. Capturar grupos de opción única (Radio buttons)
        radio_groups = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='radiogroup']"))
        )

        # --- Edad ---
        if len(radio_groups) >= 1:
            opts_edad = radio_groups[0].find_elements(By.CSS_SELECTOR, "input[type='radio']")
            if len(opts_edad) == 3:
                edad_elegida = random.choices(opts_edad, weights=[20, 55, 25], k=1)[0]
                driver.execute_script("arguments[0].click();", edad_elegida)

        # --- Cantidad total de ropa ---
        indice_ropa_total = 1
        if len(radio_groups) >= 2:
            opts_ropa = radio_groups[1].find_elements(By.CSS_SELECTOR, "input[type='radio']")
            if opts_ropa:
                indice_ropa_total = random.choices(range(len(opts_ropa)), weights=[15, 45, 30, 10], k=1)[0]
                driver.execute_script("arguments[0].click();", opts_ropa[indice_ropa_total])

        # --- Dónde compras ---
        if len(radio_groups) >= 3:
            opts_donde = radio_groups[2].find_elements(By.CSS_SELECTOR, "input[type='radio']")
            if opts_donde:
                tienda_elegida = random.choices(opts_donde, weights=[50, 35, 15], k=1)[0]
                driver.execute_script("arguments[0].click();", tienda_elegida)

        # 2. Rellenar campos de texto / numéricos
        text_inputs = driver.find_elements(
            By.CSS_SELECTOR, "input[role='textbox'], input.office-form-textfield-input, input[type='text'], input[type='number']"
        )

        max_limite_sin_usar = [10, 25, 45, 70][min(indice_ropa_total, 3)]
        if len(text_inputs) >= 1:
            text_inputs[0].clear()
            text_inputs[0].send_keys(str(random.randint(1, max_limite_sin_usar)))

        if len(text_inputs) >= 2:
            compradas_3m = random.choices([0, 1, 2, 3, 4, 5, 6, 8], weights=[10, 20, 25, 20, 12, 7, 4, 2], k=1)[0]
            text_inputs[1].clear()
            text_inputs[1].send_keys(str(compradas_3m))

        if len(text_inputs) >= 3:
            necesitadas = random.randint(0, min(compradas_3m, 3))
            text_inputs[2].clear()
            text_inputs[2].send_keys(str(necesitadas))

        if len(text_inputs) >= 4:
            text_inputs[3].clear()
            text_inputs[3].send_keys(f"{random.randint(6, 36)} meses")

        if len(text_inputs) >= 5:
            text_inputs[4].clear()
            text_inputs[4].send_keys(str(random.choices([0, 1, 2, 3, 4], weights=[50, 30, 12, 5, 3], k=1)[0]))

        # 3. Checkboxes
        checkbox_groups = driver.find_elements(By.CSS_SELECTOR, "div[role='group']")
        for group in checkbox_groups:
            checkboxes = group.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            if checkboxes:
                cantidad_a_marcar = random.randint(1, min(3, len(checkboxes)))
                for cb in random.sample(checkboxes, cantidad_a_marcar):
                    driver.execute_script("arguments[0].click();", cb)

        time.sleep(random.uniform(2.0, 4.0))

        # 4. Pulsar el botón de Enviar
        submit_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' or .//span[contains(text(),'Enviar') or contains(text(),'Submit')]]")
            )
        )
        driver.execute_script("arguments[0].click();", submit_btn)

        # === 5. COMPROBACIÓN DE ÉXITO ===
        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'su respuesta se ha enviado') or contains(text(), 'Your response was submitted') or contains(text(), 'Enviar otra respuesta')]")
                )
            )
            print(f"[OK] ¡Se ha enviado el formulario {num_envio} de {total_envios} correctamente!")
            
            ruta_screenshot = f"comprobantes_envios/envio_{num_envio}.png"
            driver.save_screenshot(ruta_screenshot)
            
        except Exception:
            print(f"[AVISO] El envío {num_envio} se ejecutó, pero no se pudo confirmar visualmente el mensaje de éxito.")

        # 6. Preparar el siguiente envío
        if num_envio < total_envios:
            another_btn = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//a[contains(text(), 'Enviar otra respuesta') or contains(text(), 'Submit another response')] | "
                        "//button[contains(text(), 'Enviar otra respuesta') or contains(text(), 'Submit another response')]"
                    )
                )
            )
            driver.execute_script("arguments[0].click();", another_btn)
            time.sleep(2.0)

            pausa_humana = random.uniform(45.0, 120.0)
            minutos = int(pausa_humana // 60)
            segundos = int(pausa_humana % 60)
            print(f"Pausa de seguridad: Esperando {minutos}m {segundos}s antes del siguiente envio...")
            time.sleep(pausa_humana)

    print("\n¡EXCELENTE! Los 30 envios se han completado y verificado con éxito.")

except Exception as e:
    error_detalle = traceback.format_exc()
    print(f"\n[ERROR CRITICO]: {e}")
    
    with open("error.log", "w", encoding="utf-8") as f:
        f.write(error_detalle)
    print("Se ha guardado un registro detallado del error en el archivo 'error.log'.")

finally:
    print("\nEl programa ha finalizado.")
    input("Presiona ENTER para cerrar esta ventana...")
    try:
        driver.quit()
    except:
        pass
