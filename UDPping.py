import socket
import time
import sys

def main():
    # Dirección IP del servidor
    direccion_servidor = '127.0.0.1'
    # Puerto del servidor
    puerto_servidor = 12000
    # Tiempo de espera en segundos antes de que una solicitud expire
    tiempo_espera = 1
    # Número total de intentos de ping
    num_intentos = 10

    # Variables para guardar los valores mínimos, máximos y totales de RTT
    rtt_min = float('inf')
    rtt_max = float('-inf')
    rtt_total = 0
    # Contador del número de paquetes recibidos
    num_recibidos = 0

    # Crear un socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_cliente:
        # Establecer el tiempo de espera del socket
        socket_cliente.settimeout(tiempo_espera)

        # Bucle para enviar y recibir paquetes
        for seq in range(1, num_intentos + 1):
            try:
                # Marcar el tiempo de inicio
                tiempo_inicio = time.time()
                # Crear el mensaje a enviar, incluyendo el número de secuencia y el tiempo de inicio
                mensaje = f'Ping {seq} {tiempo_inicio}'.encode('utf-8')
                # Enviar el mensaje al servidor
                socket_cliente.sendto(mensaje, (direccion_servidor, puerto_servidor))

                try:
                    # Intentar recibir la respuesta del servidor
                    respuesta, _ = socket_cliente.recvfrom(1024)
                except ConnectionResetError:
                    # Si se produce un error de conexión, mostrar un mensaje y continuar con el siguiente intento
                    print("Error: La conexión fue cerrada por el host remoto.")
                    continue

                # Marcar el tiempo de finalización
                tiempo_final = time.time()
                # Calcular el RTT (tiempo de ida y vuelta) restando el tiempo de inicio del tiempo de finalización
                rtt = tiempo_final - tiempo_inicio

                # Actualizar las variables de estadísticas de RTT
                rtt_min = min(rtt_min, rtt)
                rtt_max = max(rtt_max, rtt)
                rtt_total += rtt
                num_recibidos += 1

                # Imprimir la respuesta y el RTT
                print(f'Respuesta: {respuesta.decode("utf-8")}, RTT: {rtt:.6f} segundos')
            except socket.timeout:
                # Si el tiempo de espera expira, imprimir un mensaje y continuar con el siguiente intento
                print('La solicitud ha expirado')

    # Calcular la tasa de pérdida de paquetes
    tasa_perdida = (num_intentos - num_recibidos) / num_intentos * 100

    # Imprimir las estadísticas finales
    print(f'\nEstadísticas:')
    print(f'  Paquetes: Enviados = {num_intentos}, Recibidos = {num_recibidos}, Perdidos = {num_intentos - num_recibidos} ({tasa_perdida:.2f}% pérdida)')
    if num_recibidos > 0:
        # Si se recibieron paquetes, calcular e imprimir los valores promedio, mínimo y máximo de RTT
        rtt_promedio = rtt_total / num_recibidos
        print(f'  RTT (en segundos): Min = {rtt_min:.6f}, Max = {rtt_max:.6f}, Promedio = {rtt_promedio:.6f}')
    else:
        print('  RTT: No se recibieron paquetes')

if __name__ == '__main__':
    main()
