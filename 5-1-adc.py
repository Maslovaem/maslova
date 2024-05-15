import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def adc():
    i = 64

    res = 128

    while i >= 1:
        #print(res)
        GPIO.output(dac, decimal2binary(res))
        time.sleep(0.003)

        comp_value = GPIO.input(comp)

        if (comp_value == 1):
            res -= i
        elif (comp_value == 0):
            res += i

        i //= 2

    if (comp_value == 1):
        return res - 1
    if (comp_value == 0):
        return res


adc_resolution = 3.3 / 255 # шаг квантования АЦП

def DtoU(d):
    return d * adc_resolution


dac = [8, 11, 7, 1, 0, 5, 12, 6]
led = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(led, GPIO.OUT)


try:
    measurements = []
    start_time = time.time()


    # измерения при зарядке конденсатора
    GPIO.output(troyka, 1)
    try:
        while True:
            V = adc()
            measurements.append(V)

            print(V)

    except KeyboardInterrupt:
        measurements.append(V)


    # измерения при разрядке конденсатора
    GPIO.output(troyka, 0)
    try:
        while True:
            V = adc()
            measurements.append(V)

            print(V)

    except KeyboardInterrupt:
        measurements.append(V)

    end_time = time.time()

    dt = end_time - start_time # время измерений
    N = len(measurements) # количество измерений

    frec = N / dt # частота дискретизации
    T = 1 / frec  # период  дискретизации

    plt.plot(measurements)
    plt.xlabel('Номер измерения')
    plt.ylabel('Показания АЦП')
    plt.show()

    str_measurements = [str(i) for i in measurements]

    with open('data.txt', 'w') as file:
        file.write('\n'.join(str_measurements))

    with open('settings.txt', 'w') as file:
        file.write(f'Средняя частота дискретизации: {frec:.2f} Гц \n')
        file.write(f'Шаг квантования АЦП: {adc_resolution:.3f} V \n')

    print(f'Продолжительность эксперимента: {dt:.2f} c')
    print(f'Период измерений: {T:.2f} c')
    print(f'Средняя частота дискретизации: {frec:.2f} Гц')
    print(f'Шаг квантования АЦП: {adc_resolution:.3f} V')

except KeyboardInterrupt:
    print('\nStopped')
finally:
    GPIO.output(dac, 0)
    GPIO.output(led, 0)
    GPIO.cleanup()
