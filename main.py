# Bubble Sort als LED-Visualisierung: 32 Werte werden gemischt und sichtbar
# sortiert, jeder Wert ist eine Farbe, das verglichene Paar leuchtet weiß.
# ESP32: LED-Streifen an GPIO 15, Status-LED an GPIO 13

from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
from random import randint

led = Pin(13, Pin.OUT)
pixels_count = 32                                # Anzahl LEDs = Anzahl der Werte
pixels = NeoPixel(Pin(15), pixels_count)
pixels_count_half = int(pixels_count/2)


def color_by_position(offset_unlimited):
    """Zahlenwert -> 8-Bit-Farbkomponente, Dreiecksverlauf 0 -> 1 -> 0."""
    offset = offset_unlimited % pixels_count     # auf 0..31 begrenzen
    return int(255 * abs(offset-pixels_count_half) / pixels_count_half)


def show(values, p1=-1, p2=-1):
    """Array anzeigen, verglichenes Paar p1/p2 weiß markieren."""
    for i in range(pixels_count):
        # R, G und B aus demselben Wert, je um ein Drittel versetzt -> Regenbogen
        pixels[i] = (255, 255, 255) if i in (p1, p2) else tuple(
            color_by_position(values[i] + int(pixels_count*k/3)) for k in (0, 1, 2))
    pixels.write()                               # erst write() sendet an den Streifen


values = list(range(pixels_count))

while True:
    for i in range(pixels_count-1, 0, -1):       # mischen (Fisher-Yates)
        j = randint(0, i)
        values[i], values[j] = values[j], values[i]
    show(values)
    sleep_ms(800)

    last, swapped = pixels_count, True           # last = Grenze des unsortierten Bereichs
    while swapped:                               # Durchlauf ohne Tausch -> sortiert
        swapped = False
        for i in range(last-1):                  # Nachbarn vergleichen und ggf. tauschen
            if values[i] > values[i+1]:
                values[i], values[i+1] = values[i+1], values[i]
                swapped = True
            led.value(i%2)                       # Modulo lässt die Status-LED blinken
            show(values, i, i+1)
            sleep_ms(40)                         # Tempo der Visualisierung
        last -= 1                                # größter Wert sitzt hinten, fällt weg

    show(values)                                 # sortiert: durchgehender Farbverlauf
    led.value(1)
    sleep_ms(2000)