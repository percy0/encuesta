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

print("=== Automatizador de Formulario (Recarga Directa) ===")

# Preguntar al usuario cuántos envíos desea realizar
try:
    total_envios = int(input("¿Cuántos formularios deseas rellenar y enviar?: "))
except ValueError:
    total_envios = 30
    print("Valor no válido. Se establecerá un total predeterminado de 30 envíos.")

input(f"\nSe realizarán {total_envios} envíos. Presiona ENTER cuando estés listo para empezar...")

try:
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Descomenta si quieres que corra oculto sin abrir ventanas

    driver = webdriver.Chrome(options=options)

    for i in range(total_envios):
        num_envio = i + 1
        print("\n--------------------------------------------------")
        print(f"Iniciando proceso del [Envio {num_envio} de {total_envios}]...")
        print("--------------------------------------------------")
        
        # Abrir o recargar la URL limpia del formulario directamente
        driver.get(url)
        
        wait = WebDriverWait(driver, 25)

        # Esperar a que carguen los radio buttons (Preguntas 1, 2 y 6)
        radio_groups = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='radiogroup']"))
        )

        # --- Pregunta 1: Edad ---
        if len(radio_groups) >= 1:
            opts_edad = radio_groups[0].find_elements(By.CSS_SELECTOR, "input[type='radio']")
            if len(opts_edad) >= 3:
                edad_elegida = random.choices(opts_edad, weights=[20, 55, 25], k=1)[0]
                driver.execute_script("arguments[0].click();", edad_elegida)
                print("  -> Pregunta 1 (Edad): Respondida")

        # --- Pregunta 2: Cantidad total de ropa ---
        indice_ropa_total = 1
        if len(radio_groups) >= 2:
            opts_ropa = radio_groups[1].find_elements(By.CSS_SELECTOR, "input[type='radio']")
            if opts_ropa:
                indice_ropa_total = random.choices(range(len(opts_ropa)), weights=[15, 45, 30, 10], k=1)[0]
                ropa_elegida = opts_ropa[indice_ropa_total]
                driver.execute_script("arguments[0].click();", ropa_elegida)
                print("  -> Pregunta 2 (Total ropa): Respondida")

        # --- Pregunta 6: Dónde compras ---
        if len(radio_groups) >= 3:
            opts_donde = radio_groups[2].find_elements(By.CSS_SELECTOR, "input[type='radio']")
            if opts_donde:
                tienda_elegida = random.choices(opts_donde, weights=[50, 35, 15], k=1)[0]
                driver.execute_script("arguments[0].click();", tienda_elegida)
                print("  -> Pregunta 6 (Dónde compras): Respondida")

        # 2. Rellenar campos de texto / numéricos de forma ordenada y coherente
        time.sleep(1.5)
        text_inputs = driver.find_elements(
            By.CSS_SELECTOR, "input[data-automation-id='textInput'], input.office-form-textfield-input, input[type='text'], input[type='number']"
        )

        print(f"  -> Se detectaron {len(text_inputs)} campos de texto para rellenar.")

        def escribir_en_input(elemento, texto):
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
                driver.execute_script("arguments[0].click();", elemento)
                elemento.clear()
                elemento.send_keys(str(texto))
            except:
                driver.execute_script(f"arguments[0].value = '{texto}';", elemento)

        max_limite_sin_usar = [10, 25, 45, 70][min(indice_ropa_total, 3)]
        
        if len(text_inputs) >= 1:
            val_no_usadas = random.randint(1, max_limite_sin_usar)
            escribir_en_input(text_inputs[0], val_no_usadas)
            print(f"  -> P3 (No usadas último año): {val_no_usadas}")

        if len(text_inputs) >= 2:
            compradas_3m = random.choices([0, 1, 2, 3, 4, 5, 6, 8], weights=[10, 20, 25, 20, 12, 7, 4, 2], k=1)[0]
            escribir_en_input(text_inputs[1], compradas_3m)
            print(f"  -> P4 (Compradas últimos 3m): {compradas_3m}")

        if len(text_inputs) >= 3:
            necesitadas = random.randint(0, min(compradas_3m, 3))
            escribir_en_input(text_inputs[2], necesitadas)
            print(f"  -> P5 (Realmente necesitadas): {necesitadas}")

        if len(text_inputs) >= 4:
            tiempo_uso = f"{random.choice([6, 12, 18, 24, 36])} meses"
            escribir_en_input(text_inputs[3], tiempo_uso)
            print(f"  -> P9 (Tiempo medio de uso): {tiempo_uso}")

        if len(text_inputs) >= 5:
            con_etiqueta = random.choices([0, 1, 2, 3, 4], weights=[50, 30, 12, 5, 3], k=1)[0]
            escribir_en_input(text_inputs[4], con_etiqueta)
            print(f"  -> P10 (Con etiqueta sin usar): {con_etiqueta}")

        # 3. Checkboxes (Preguntas de selección múltiple 7 y 8)
        checkbox_groups = driver.find_elements(By.CSS_SELECTOR, "div[role='group']")
        for idx_cb, group in enumerate(checkbox_groups):
            checkboxes = group.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            if checkboxes:
                cantidad_a_marcar = random.randint(1, min(3, len(checkboxes)))
                seleccionadas = random.sample(checkboxes, cantidad_a_marcar)
                print(f"  -> Checkboxes grupo {idx_cb + 1}: Marcadas {cantidad_a_marcar} opciones.")
                for cb in seleccionadas:
                    driver.execute_script("arguments[0].click();", cb)

        time.sleep(2.0)

        # 4. Pulsar el botón de Enviar
        print("  -> Intentando enviar formulario...")
        submit_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' or @data-automation-id='submitButton' or .//span[contains(text(),'Enviar') or contains(text(),'Submit')]]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", submit_btn)

        # === 5. COMPROBACIÓN DE ÉXITO Y CAPTURA ===
        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'su respuesta se ha enviado') or contains(text(), 'Your response was submitted') or contains(text(), 'Enviar otra respuesta')]")
                )
            )
            print(f"✅ [OK] ¡Formulario {num_envio} de {total_envios} enviado y confirmado con éxito!")
            
            ruta_screenshot = f"comprobantes_envios/envio_{num_envio}.png"
            driver.save_screenshot(ruta_screenshot)
            
        except Exception:
            print(f"⚠️ [AVISO] El envío {num_envio} se ejecutó, pero tardó en mostrar la confirmación visual.")

        # 6. Pausa de seguridad humana antes del siguiente envío (si no es el último)
        if num_envio < total_envios:
            pausa_humana = random.uniform(45.0, 120.0)
            minutos = int(pausa_humana // 60)
            segundos = int(pausa_humana % 60)
            print(f"⏳ Pausa de seguridad: Esperando {minutos}m {segundos}s antes del siguiente envío...\n")
            time.sleep(pausa_humana)

    print(f"\n🎉 ¡EXCELENTE! Los {total_envios} envíos se han completado y verificado con éxito.")

except Exception as e:
    error_detalle = traceback.format_exc()
    print(f"\n❌ [ERROR CRITICO]: {e}")
    
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
