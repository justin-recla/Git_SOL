from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
from random import randint

led = Pin(13, Pin.OUT)
led.value(1)


pixels_count = 32
pixels = NeoPixel(Pin(15), pixels_count)
pixels_count_half = int(pixels_count/2)


def color_by_position(offset_unlimited):
    offset = offset_unlimited % pixels_count
    brightness = abs(offset-pixels_count_half) / pixels_count_half
    return int(255*brightness)


def show(values, p1=-1, p2=-1):
    for i in range(pixels_count):
        if i == p1 or i == p2:
            pixels[i] = (255, 255, 255)
        else:
            r = color_by_position(values[i])
            g = color_by_position(values[i] + int(pixels_count*1/3))
            b = color_by_position(values[i] + int(pixels_count*2/3))
            pixels[i] = (r, g, b)

    pixels.write()


values = list(range(pixels_count))
t = 0

while True:
    for i in range(pixels_count-1, 0, -1):
        j = randint(0, i)
        values[i], values[j] = values[j], values[i]

    show(values)
    sleep_ms(800)

    last = pixels_count
    swapped = True
    while swapped:
        swapped = False
        for i in range(last-1):
            t += 1
            led.value(t%2)

            if values[i] > values[i+1]:
                values[i], values[i+1] = values[i+1], values[i]
                swapped = True

            show(values, i, i+1)
            sleep_ms(40)
        last -= 1

    show(values)
    led.value(1)
    sleep_ms(2000)