import requests
import math


API_KEY = '0f377676c4054c8f9587a2987b50e7ab'

def obtener_coordenadas(ciudad, pais):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={ciudad},{pais}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error en la solicitud: {response.status_code}")
        return None
    
    data = response.json()
    if data['results']:
        location = data['results'][0]['geometry']
        return location['lat'], location['lng']
    else:
        print("No se encontraron resultados para la ubicación solicitada.")
        return None

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia_km = R * c
    return distancia_km

def calcular_duracion(distancia, velocidad):
    return distancia / velocidad

def main():
    while True:
        print("Bienvenido al calculador de distancias y tiempos de viaje.")
        ciudad_origen = input("Ingrese la Ciudad de Origen: ")
        ciudad_destino = input("Ingrese la Ciudad de Destino: ")

        coord_origen = obtener_coordenadas(ciudad_origen, 'Chile')
        coord_destino = obtener_coordenadas(ciudad_destino, 'Argentina')

        if coord_origen and coord_destino:
            distancia_km = haversine(coord_origen[0], coord_origen[1], coord_destino[0], coord_destino[1])
            distancia_millas = distancia_km * 0.621371

            print(f"La distancia entre {ciudad_origen} y {ciudad_destino} es de {distancia_km:.2f} km ({distancia_millas:.2f} millas).")

            print("Seleccione el medio de transporte:")
            print("1. Automóvil (80 km/h)")
            print("2. Tren (100 km/h)")
            print("3. Avión (800 km/h)")

            opcion = input("Ingrese la opción: ")

            if opcion == '1':
                velocidad = 80
            elif opcion == '2':
                velocidad = 100
            elif opcion == '3':
                velocidad = 800
            else:
                print("Opción no válida.")
                continue

            duracion_horas = calcular_duracion(distancia_km, velocidad)
            print(f"La duración del viaje de {ciudad_origen} a {ciudad_destino} en {opcion} es de {duracion_horas:.2f} horas.")

            print(f"Narrativa del viaje: El viaje desde {ciudad_origen} hasta {ciudad_destino} cubre una distancia de {distancia_km:.2f} km y tomará aproximadamente {duracion_horas:.2f} horas en el medio de transporte seleccionado.")

        else:
            print("No se pudieron obtener las coordenadas de una o ambas ciudades.")

        salida = input("¿Desea salir? (s/n): ")
        if salida.lower() == 's':
            break

if __name__ == "__main__":
    main()
