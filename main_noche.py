from machine import I2C, Pin
from bme280_float import BME280
import time
import os

# Configuración
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)
bme = BME280(i2c=i2c)

# Nombre del archivo
ARCHIVO_CSV = "datos_bme280_noche2122.csv"

# Verificar si el archivo existe, si no, crear encabezados
def inicializar_csv():
    try:
        with open(ARCHIVO_CSV, 'r') as f:
            pass  # El archivo ya existe
    except:
        with open(ARCHIVO_CSV, 'w') as f:
            f.write("timestamp,temperatura_C,presion_hPa,humedad_%\n")
        print(f"Archivo {ARCHIVO_CSV} creado con encabezados")

# Guardar una lectura
def guardar_dato(temp, pres, hum):
    timestamp = time.time()  # Segundos desde epoch
    tiempo_local = time.localtime()
    
    # Formato de fecha legible
    fecha = "{:04d}-{:02d}-{:02d}".format(tiempo_local[0], tiempo_local[1], tiempo_local[2])
    hora = "{:02d}:{:02d}:{:02d}".format(tiempo_local[3], tiempo_local[4], tiempo_local[5])
    
    with open(ARCHIVO_CSV, 'a') as f:
        # Opción 1: Con timestamp UNIX
        # f.write(f"{timestamp},{temp:.2f},{pres/100:.2f},{hum:.2f}\n")
        
        # Opción 2: Con fecha y hora legible
        f.write(f"{fecha} {hora},{temp:.2f},{pres/100:.2f},{hum:.2f}\n")
    
    print(f"Dato guardado: {fecha} {hora}")

# Leer todos los datos guardados
def leer_datos_guardados():
    try:
        with open(ARCHIVO_CSV, 'r') as f:
            lineas = f.readlines()
            print(f"\n Datos guardados ({len(lineas)-1} lecturas):")
            for i, linea in enumerate(lineas):
                if i == 0:  # Encabezado
                    print("Encabezado:", linea.strip())
                elif i < 6:  # Mostrar solo las primeras 5 lecturas
                    print(f"  {linea.strip()}")
            if len(lineas) > 6:
                print(f"  ... y {len(lineas)-6} más")
    except:
        print("No hay datos guardados aún")

# Programa principal
inicializar_csv()
print("Iniciando adquisición de datos...")
print("Presiona Ctrl+C para detener\n")

contador = 0
intervalo = 5  # Segundos entre lecturas

try:
    while True:
        # Leer sensor
        temp, pres, hum = bme.read_compensated_data()
        
        # Mostrar en consola
        print(f"[{contador+1}] {temp:.1f}°C | {pres/100:.1f}hPa | {hum:.1f}%")
        
        # Guardar en CSV
        guardar_dato(temp, pres, hum)
        
        contador += 1
        time.sleep(intervalo)
        
except KeyboardInterrupt:
    print(f"\n\n Adquisición detenida. Total: {contador} lecturas")
    print(f" Datos guardados en: {ARCHIVO_CSV}")
    
    # Mostrar espacio disponible
    info = os.statvfs('/')
    espacio_libre = info[0] * info[3]  # block size * free blocks
    print(f" Espacio libre: {espacio_libre / 1024:.1f} KB")
    
    leer_datos_guardados()