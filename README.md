# Automatización de Compra - Elektra (Prueba Selenium)

Este repositorio contiene un script de Python diseñado para automatizar el flujo de compra en el sitio web de Elektra.mx utilizando **Selenium WebDriver**.

## Funcionalidades del Script
* **Inicio de sesión:** Automatiza el acceso con credenciales de usuario.
* **Búsqueda y Selección:** Añade una "Máquina de Coser Singer Heavy Duty" al carrito de compras.
* **Flujo de Checkout:** Gestiona la navegación por el carrito, selección de dirección y sección de pagos.
* **Simulación de Pago:** Realiza una prueba de pago con una tarjeta ficticia para validar el manejo de errores (pago declinado).

## Requisitos
* Python 3.x
* Selenium (`pip install selenium`)
* ChromeDriver (compatible con tu versión de Chrome)

## Ejecución
1. Clona el repositorio.
2. Configura tus credenciales en el objeto 'Credentials' dentro del script.
3. Ejecuta: 'python simulate_elektra_purchase.py'
