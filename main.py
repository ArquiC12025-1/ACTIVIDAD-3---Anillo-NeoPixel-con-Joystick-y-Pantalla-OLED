# Autores: Andres Galvis, Keppler Sanchez y Daniel Viafara.

from machine import Pin, ADC, I2C
from neopixel import NeoPixel
from ssd1306 import SSD1306_I2C
import utime
import framebuf

# Configuración de la pantalla OLED (128x32)
i2c = I2C(0, scl=Pin(2), sda=Pin(5))
oled = SSD1306_I2C(128, 32, i2c)

# Tamaño de la imagen (ajustado)
img_width = 22
img_height = 30

# Datos de la imagen en formato bytearray
image_data = bytearray([
    0b11111111, 0b11111111, 0b11111111,
    0b11111111, 0b11111111, 0b11111111,
    0b11111111, 0b10000001, 0b11111111,
    0b11111000, 0b00000000, 0b01111111,
    0b11100000, 0b11111110, 0b00011111,
    0b11100001, 0b11111110, 0b00011111,
    0b11100011, 0b11111110, 0b00011111,
    0b11100011, 0b11111110, 0b00011111,
    0b11100001, 0b11111110, 0b00011111,
    0b11100011, 0b11111110, 0b00011111,
    0b11100001, 0b11111110, 0b00011111,
    0b11100001, 0b11111110, 0b00011111,
    0b11100011, 0b11111000, 0b00011111,
    0b11100111, 0b11111110, 0b00011111,
    0b11111111, 0b11111111, 0b10001111,
    0b11111111, 0b11111111, 0b11001111,
    0b11111111, 0b11111111, 0b11001111,
    0b11111111, 0b11111111, 0b11111111,
    0b11111111, 0b11111111, 0b11111111,
    0b11111111, 0b11111000, 0b01111111,
    0b11111111, 0b11111111, 0b11111111,
    0b11111111, 0b11111111, 0b11111111,
    0b11011110, 0b10011001, 0b10001111,
    0b11011110, 0b10100101, 0b10110111,
    0b11011110, 0b10100101, 0b10110111,
    0b11011110, 0b10111101, 0b10001111,
    0b11011110, 0b10111101, 0b10110111,
    0b11101101, 0b10111101, 0b10110111,
    0b11110011, 0b10111101, 0b10001111,
    0b11111111, 0b11111111, 0b11111111
])

# Función para mostrar la imagen centrada en la pantalla OLED
def mostrar_imagen():
    fb = framebuf.FrameBuffer(image_data, img_width, img_height, framebuf.MONO_HLSB)
    
    x_pos = (oled.width - img_width) // 2  # Centrar horizontalmente
    y_pos = (oled.height - img_height) // 2  # Centrar verticalmente

    oled.fill(0)  # Limpia la pantalla
    oled.blit(fb, x_pos, y_pos)  # Dibuja la imagen en la posición calculada
    oled.show()  # Actualiza la pantalla
    utime.sleep(3)  # Mostrar por 3 segundos

# Función para desplazar nombres de derecha a izquierda
def scroll_nombres():
    texto = "Andres Galvis, Keppler Sanchez y Daniel Viafara  "
    ancho_texto = len(texto) * 6  # Cada carácter tiene aproximadamente 6 píxeles de ancho

    for offset in range(ancho_texto + 128):  # Mueve el texto completamente
        oled.fill(0)  # Limpia la pantalla
        oled.text(texto, 128 - offset, 12)  # Mueve el texto de derecha a izquierda
        oled.show()
        utime.sleep(0.01)  # Ajusta la velocidad del desplazamiento

    utime.sleep(1)  # Pausa final antes de terminar la función

# Ejecutar funciones
mostrar_imagen()
scroll_nombres()


# Configuración del joystick
joy_x = ADC(Pin(12))
joy_y = ADC(Pin(14))
joy_x.atten(ADC.ATTN_11DB)
joy_y.atten(ADC.ATTN_11DB)
joy_x.width(10)
joy_y.width(10)
joy_button = Pin(25, Pin.IN)

# Configuración de Neopixel
num_leds = 16
pixels = NeoPixel(Pin(15), num_leds)

# Variables de estado
color_rojo = 0
color_azul = 0
pos_led_blanco = 0
direccion = 1
movimiento_activo = True
boton_anterior = 1

# Función para actualizar los Neopixels
def actualizar_neopixel():
    for i in range(num_leds):
        if i == pos_led_blanco:
            pixels[i] = (255, 255, 255)
        else:
            pixels[i] = (color_rojo, 0, color_azul)
    pixels.write()

# Función para mostrar información en la OLED
def actualizar_oled():
    oled.fill(0)
    oled.text("Color:", 0, 0)
    if color_azul > 0:
        oled.text("Azul", 50, 0)
    elif color_rojo > 0:
        oled.text("Rojo", 50, 0)
    else:
        oled.text("Negro", 50, 0)
    
    oled.text("Dir:", 0, 16)
    if movimiento_activo:
        oled.text("Horario" if direccion == 1 else "Antihorario", 50, 16)
    else:
        oled.text("Detenido", 50, 16)
    oled.show()

# Bucle principal
while True:
    joy_x_val = joy_x.read()
    joy_y_val = joy_y.read()
    button_pressed = not joy_button.value()

    if button_pressed and boton_anterior == 1:
        movimiento_activo = not movimiento_activo
    boton_anterior = joy_button.value()

    if joy_x_val > 600 and direccion != 1:
        direccion = 1
        color_azul = 50
        color_rojo = 0
    elif joy_x_val < 400 and direccion != -1:
        direccion = -1
        color_rojo = 50
        color_azul = 0
    
    if direccion == 1:
        if joy_y_val > 600:
            color_azul = min(255, color_azul + 5)
        elif joy_y_val < 400:
            color_azul = max(0, color_azul - 5)
    else:
        if joy_y_val > 600:
            color_rojo = min(255, color_rojo + 5)
        elif joy_y_val < 400:
            color_rojo = max(0, color_rojo - 5)
    
    if movimiento_activo:
        pos_led_blanco = (pos_led_blanco + direccion) % num_leds
    
    actualizar_neopixel()
    actualizar_oled()
    utime.sleep(0.1)
