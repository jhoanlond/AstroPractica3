import serial
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import deque
from datetime import datetime
import csv

# Crear una instancia de serial para leer desde el puerto COM8
ser = serial.Serial('COM8', 9600)

# Crear listas para guardar los datos
time_data = deque(maxlen=100)
temp_dht = deque(maxlen=100)
temp_bmp = deque(maxlen=100)
hum_dht = deque(maxlen=100)
pres_bmp = deque(maxlen=100)

# Crear un archivo CSV para guardar los datos
csv_file = open('data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'temp_dht', 'temp_bmp', 'hum_dht', 'pres_bmp'])

# Crear una figura para cada gráfico
plt.ion()

fig1, ax1 = plt.subplots()
line1, = ax1.plot([], [], label='temp_dht')
line2, = ax1.plot([], [], label='temp_bmp')
ax1.set_xlabel('Tiempo')
ax1.set_ylabel('Temperatura')
ax1.legend()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

fig2, ax2 = plt.subplots()
line3, = ax2.plot([], [], label='hum_dht')
ax2.set_xlabel('Tiempo')
ax2.set_ylabel('Humedad')
ax2.legend()
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

fig3, ax3 = plt.subplots()
line4, = ax3.plot([], [], label='pres_bmp')
ax3.set_xlabel('Tiempo')
ax3.set_ylabel('Presión')
ax3.legend()
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

while True:
    try:
        # Leer una línea del puerto serial
        line = ser.readline().decode('utf-8').rstrip()
        data = line.split(", ")

        # Verificar si tenemos los 4 datos
        if len(data) == 4:
            # Agregar los datos a las listas
            current_time = datetime.now()
            time_data.append(mdates.date2num(current_time))
            temp_dht.append(float(data[0]))
            temp_bmp.append(float(data[2]))
            hum_dht.append(float(data[1]))
            pres_bmp.append(float(data[3]))

            # Guardar los datos en el archivo CSV
            csv_writer.writerow([current_time, data[0], data[2], data[1], data[3]])

            # Actualizar los datos del gráfico
            line1.set_data(time_data, temp_dht)
            line2.set_data(time_data, temp_bmp)
            line3.set_data(time_data, hum_dht)
            line4.set_data(time_data, pres_bmp)

            # Ajustar los límites del gráfico
            ax1.relim()
            ax1.autoscale_view()
            ax2.relim()
            ax2.autoscale_view()
            ax3.relim()
            ax3.autoscale_view()

            # Redibujar el gráfico
            fig1.canvas.draw()
            fig1.canvas.flush_events()
            fig2.canvas.draw()
            fig2.canvas.flush_events()
            fig3.canvas.draw()
            fig3.canvas.flush_events()

            # Esto permite que el gráfico se actualice
            plt.pause(0.01)

        else:
            print("Línea de datos incompleta: ", line)

    except KeyboardInterrupt:
        print("Interupción por teclado, cerrando...")
        ser.close()
        csv_file.close()  # No olvides cerrar el archivo CSV cuando termines
        break
