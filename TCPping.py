import socket
import time

def main():
    # Configuración del servidor y conexión
    direccion_servidor = '127.0.0.1'
    puerto_servidor = 12000
    tiempo_espera = 1
    num_intentos = 10

    # Variables para almacenar estadísticas
    min_rtt = float('inf')
    max_rtt = float('-inf')
    tiempo_total_rtt = 0
    num_recibidos = 0

    # Creación del socket y conexión al servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_cliente:
        socket_cliente.settimeout(tiempo_espera)
        socket_cliente.connect((direccion_servidor, puerto_servidor))

        # Bucle para realizar pings
        for secuencia in range(1, num_intentos + 1):
            try:
                tiempo_inicio = time.time()
                mensaje = f'Ping {secuencia} {tiempo_inicio}'.encode('utf-8')
                socket_cliente.send(mensaje)

                try:
                    # Recibir la respuesta del servidor
                    respuesta = socket_cliente.recv(1024)
                except ConnectionResetError:
                    # Error en caso de que el host remoto cierre la conexión
                    print("Error: La conexión fue cerrada por el host remoto.")
                    continue

                tiempo_fin = time.time()
                rtt = tiempo_fin - tiempo_inicio

                # Actualizar las estadísticas
                min_rtt = min(min_rtt, rtt)
                max_rtt = max(max_rtt, rtt)
                tiempo_total_rtt += rtt
                num_recibidos += 1

                # Imprimir la respuesta y el RTT
                print(f'Respuesta: {respuesta.decode("utf-8")}, RTT: {rtt:.6f} segundos')
            except socket.timeout:
                # Mensaje en caso de que la solicitud expire
                print('La solicitud ha expirado')

    # Calcular e imprimir las estadísticas finales
    tasa_perdida = (num_intentos - num_recibidos) / num_intentos * 100
    print(f'\nEstadísticas:')
    print(f'  Paquetes: Enviados = {num_intentos}, Recibidos = {num_recibidos}, Perdidos = {num_intentos - num_recibidos} ({tasa_perdida:.2f}% perdidos)')
    if num_recibidos > 0:
        rtt_promedio = tiempo_total_rtt / num_recibidos
        print(f'  RTT (en segundos): Mínimo = {min_rtt:.6f}, Máximo = {max_rtt:.6f}, Promedio = {rtt_promedio:.6f}')
    else:
        print('  RTT: No se recibieron paquetes')

if __name__ == '__main__':
    main()
