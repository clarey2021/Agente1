"""
simulate_elektra_purchase.py

Este script automatiza el flujo de compra en Elektra. Usa Selenium para
controlar Chrome, iniciar sesión con tus credenciales, añadir el producto
“Máquina de Coser Singer Heavy Duty” al carrito, avanzar por el proceso de
checkout y finalmente intentar pagar con una tarjeta de prueba. El pago
será rechazado, como se espera, ya que la tarjeta es ficticia.

Requisitos previos:
  pip install selenium
y contar con el binario de ChromeDriver disponible en tu PATH.

Ejecuta el script con:
  python simulate_elektra_purchase.py
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@dataclass
class Credentials:
    """Datos de acceso y pago."""
    email: str
    password: str
    card_number: str
    card_name: str
    card_exp_month: str  # dos dígitos, e.g. "12"
    card_exp_year: str   # dos dígitos, e.g. "27"
    card_cvv: str


def simulate_purchase(creds: Credentials, headless: bool = False) -> None:
    """Simula una compra en elektra.mx usando Selenium."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    try:
        # Ir a Elektra e iniciar sesión
        driver.get("https://www.elektra.mx")
        try:
            login_link = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(text(),'Inicia sesión')] | //a[contains(text(),'Inicia sesión')]")
                )
            )
            login_link.click()
        except TimeoutException:
            # Si no aparece el enlace, accede directamente a /Login
            driver.get("https://www.elektra.mx/Login")

        # Rellenar formulario de login
        email_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='email' or contains(@placeholder,'Correo')]")
            )
        )
        email_input.clear()
        email_input.send_keys(creds.email)

        password_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='password' or contains(@placeholder,'Contraseña')]")
            )
        )
        password_input.clear()
        password_input.send_keys(creds.password)

        submit_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Iniciar sesión')]")
            )
        )
        submit_button.click()
        print("Inicio de sesión completado.")

        # Navegar a la página del producto
        driver.get("https://www.elektra.mx/maquina-de-coser-singer-heavy-duty-9000481/p")

        # Añadir al carrito
        add_to_cart_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Agregar al carrito')]")
            )
        )
        add_to_cart_btn.click()
        print("Producto añadido al carrito.")

        # Cerrar la oferta de garantía si aparece
        try:
            no_thanks_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(.,'No, gracias')] | //span[contains(.,'No, gracias')]")
                )
            )
            no_thanks_btn.click()
            print("Oferta de garantía descartada.")
        except TimeoutException:
            pass  # Si no aparece, continuar

        # Abrir carrito (icono del carrito en la esquina superior)
        cart_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@aria-label,'carrito') or contains(@class,'minicart')]//span[contains(@class,'icon-cart')] | //div[contains(@class,'minicart')]")
            )
        )
        cart_button.click()

        # Continuar con la compra
        continue_purchase_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Continuar con la compra') or contains(.,'Continuar con tu compra')]")
            )
        )
        continue_purchase_btn.click()
        print("Acceso a la vista de carrito completo.")

        # En el carrito, pulsar de nuevo el botón continuar
        continue_btn2 = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Continuar con tu compra') and not(@disabled)]")
            )
        )
        continue_btn2.click()

        # Seleccionar la dirección y seguir al pago
        shipping_continue_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Continuar con el pago')]")
            )
        )
        shipping_continue_btn.click()
        print("Dirección de envío confirmada.")

        # Seleccionar método de pago con tarjeta
        card_section_header = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(.,'Tarjeta de débito o crédito')]")
            )
        )
        card_section_header.click()

        # Rellenar datos de tarjeta
        card_number_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@inputmode='numeric' or @placeholder='Número de tarjeta' or contains(@aria-label,'Número de la tarjeta')]")
            )
        )
        card_number_input.clear()
        card_number_input.send_keys(creds.card_number)

        card_name_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[contains(@placeholder,'Nombre') or contains(@aria-label,'Nombre')]")
            )
        )
        card_name_input.clear()
        card_name_input.send_keys(creds.card_name)

        # Seleccionar mes y año de expiración
        exp_month_select = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[contains(@name,'month') or contains(@id,'month')]")
            )
        )
        exp_month_select.click()
        exp_month_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//select[contains(@name,'month') or contains(@id,'month')]//option[normalize-space(text())='{creds.card_exp_month}']")
            )
        )
        exp_month_option.click()

        exp_year_select = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[contains(@name,'year') or contains(@id,'year')]")
            )
        )
        exp_year_select.click()
        exp_year_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//select[contains(@name,'year') or contains(@id,'year')]//option[normalize-space(text())='{creds.card_exp_year}']")
            )
        )
        exp_year_option.click()

        # CVV
        cvv_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='password' or contains(@placeholder,'Seguridad') or contains(@aria-label,'Seguridad')]")
            )
        )
        cvv_input.clear()
        cvv_input.send_keys(creds.card_cvv)

        # Pulsar “Pagar”
        pay_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Pagar') and not(@disabled)]")
            )
        )
        pay_button.click()
        print("Se hizo clic en pagar; esperando respuesta…")

        # Esperar unos segundos para que aparezca el mensaje de error
        time.sleep(10)
        try:
            driver.find_element(
                By.XPATH,
                "//div[contains(@class,'modal')]//p[contains(.,'Pago declinado')]"
            )
            print("El pago fue declinado (comportamiento esperado con datos de prueba).")
        except Exception:
            print("No se encontró mensaje de declinación; revise manualmente si hubo cambios.")
    finally:
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    # Sustituye estos valores por tus credenciales reales si lo vas a usar.
    creds = Credentials(
        email="vvvvvv@outlook.com",
        password="kkkkkkk",
        card_number="4242424242424242",
        card_name="Pruebas Gee",
        card_exp_month="12",
        card_exp_year="27",
        card_cvv="123",
    )
    simulate_purchase(creds, headless=False)
