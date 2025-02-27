#Autores: Keppler Sanchez, Daniel Viafara y Andrés Galvis
from machine import Pin, ADC, PWM, I2C
from neopixel import NeoPixel
from ssd1306 import SSD1306_I2C
import utime
import math

# Configuración del servo
servo = PWM(Pin(13), freq=50)

# Configuración del potenciómetro
potenciometro = ADC(Pin(32))
potenciometro.atten(ADC.ATTN_11DB)
potenciometro.width(ADC.WIDTH_12BIT)

# Configuración del joystick
joy_x = ADC(Pin(12))
joy_y = ADC(Pin(14))
joy_x.atten(ADC.ATTN_11DB)
joy_y.atten(ADC.ATTN_11DB)
joy_x.width(10)
joy_y.width(10)
joy_button = Pin(25, Pin.IN, Pin.PULL_UP)

# Configuración de la pantalla SSD1306 (128x32)
i2c = I2C(0, scl=Pin(2), sda=Pin(5))
oled = SSD1306_I2C(128, 32, i2c)

# Configuración de Neopixel
pixels = NeoPixel(Pin(15), 16)

# Función para mapear valores
def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Función para mover el servo
def mover_servo(angulo):
    duty = map_value(angulo, 0, 180, 25, 125)
    servo.duty(duty)

# Función para actualizar los Neopixels según la dirección
def actualizar_neopixel(direccion):
    if direccion == -1:
        color = (255, 0, 0)  #  Rojo (Antihorario)
    elif direccion == 1:
        color = (0, 255, 0)  #  Verde (Horario)
    else:
        color = (255, 255, 255)  #  Blanco (Botón presionado)

    for i in range(16):
        pixels[i] = color
    pixels.write()

# Función para mostrar el "manómetro" en la pantalla OLED
def mostrar_manometro(angulo):
    oled.fill(0)  # Limpiar pantalla

    # Dibujar un semicírculo (imitación de un manómetro)
    for i in range(10, 118, 4):
        oled.pixel(i, 16, 1)  # Línea horizontal base

    # Calcular la posición de la "aguja"
    x = int(64 + 20 * math.cos(math.radians(angulo + 180)))
    y = int(16 + 10 * math.sin(math.radians(angulo + 180)))  # Reducido por la altura de la pantalla

    # Dibujar la aguja
    oled.line(64, 16, x, y, 1)

    # Mostrar el ángulo en texto
    oled.text(f"Angulo: {angulo}°", 30, 24)

    oled.show()

# Función principal
def main():
    angulo = 90  # Mantiene el último ángulo en memoria
    boton_presionado = False  # Estado previo del botón

    while True:
        joy_value_x = joy_x.read()  # Leer el joystick (Eje X)
        joy_value_y = joy_y.read()  # Leer el joystick (Eje Y)
        pot_value = potenciometro.read()  # Leer potenciómetro
        delay = map_value(pot_value, 0, 4095, 5, 50)  # Control de velocidad

        # Movimiento del joystick en X e Y
        if joy_value_x < 400 or joy_value_y < 400:  # Antihorario
            angulo = max(0, angulo - 5)
            actualizar_neopixel(-1)
        elif joy_value_x > 600 or joy_value_y > 600:  # Horario
            angulo = min(180, angulo + 5)
            actualizar_neopixel(1)

        # Verificar si el botón del joystick fue presionado
        if not joy_button.value():  # Si el botón está presionado (valor 0)
            if not boton_presionado:  # Solo cambiar si es la primera vez que se detecta
                actualizar_neopixel(0)
                boton_presionado = True  # Marcar como presionado
        else:
            boton_presionado = False  # Restablecer cuando se suelta

        # Mover el servo al nuevo ángulo solo si cambió
        mover_servo(angulo)

        # Mostrar el ángulo en la pantalla OLED
        mostrar_manometro(angulo)

        utime.sleep_ms(delay)  # Ajuste de velocidad según el potenciómetro

if __name__ == "__main__":
    main()
