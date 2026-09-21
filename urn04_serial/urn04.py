import serial
import time

serial = serial.Serial('/dev/ttyUSB0',19200, timeout=1)

if serial.is_open:
    print("Serial port opened correctly")
else:
    serial.open()

print("Setting address 0x11")
serial.write(b'\x55\xAA\xAB\x01\x55\x11\x11')
data = serial.read(size=7)
print(data.hex(' '))

print("Measuring:")
serial.write(b'\x55\xAA\x11\x00\x01\x11')
time.sleep(0.1)
serial.write(b'\x55\xAA\x11\x00\x02\x12')
measure = serial.read(size=8)
print (measure.hex(' '))

distance1 = measure[5]
distance2 = measure[6]
total_distance = distance1 + distance2
print(f"The distance is:",total_distance,"cm")

serial.close()
