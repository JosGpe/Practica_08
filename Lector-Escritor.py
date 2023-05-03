import threading
import time
import random

class Archivo:

    def __init__(self):
        self.valor = 0
        self.archivo = open("archivo (1).txt", "r+")
        self.lock_escritor = threading.Lock()
        self.sem_lector = threading.Semaphore(2) # Dos lectores permitidos al mismo tiempo

    def escribir(self, id_escritor):
        while True:
            tiempo_espera = random.choice([0.5, 1, 2])
            print(f"Escritor {id_escritor} inició con una frecuencia de {tiempo_espera} segundos")
            time.sleep(tiempo_espera)

            self.lock_escritor.acquire() # Bloquear el acceso al archivo para otros escritores
            self.archivo.write(f"{self.valor}\n")
            self.valor += 1
            self.archivo.flush() # Forzar la escritura en disco
            print(f"Escritor {id_escritor} escribió en el archivo")
            self.lock_escritor.release() # Desbloquear el acceso al archivo para otros escritores

    def leer(self, id_lector):
        while True:
            tiempo_espera = random.choice([1, 1.5, 2])
            print(f"Lector {id_lector} inició con una frecuencia de {tiempo_espera} segundos")
            time.sleep(tiempo_espera)

            self.sem_lector.acquire() # Bloquear el acceso al archivo para otros lectores
            self.lock_escritor.acquire() 

            # Si hay otro lector leyendo y tienen la misma frecuencia, establecer el puntero
            # al inicio del archivo para permitir que ambos lean al mismo tiempo
            frecuencias = [1, 1.5, 2]
            if self.sem_lector._value == 1 and tiempo_espera in frecuencias \
            or self.sem_lector._value == 1.5 and tiempo_espera in frecuencias \
            or self.sem_lector._value == 2 and tiempo_espera in frecuencias:
                self.archivo.seek(0) # Mover el puntero al inicio del archivo
                
            contenido = self.archivo.read()
            print(f"Lector {id_lector} leyó: {contenido}")
            self.lock_escritor.release() 
            self.sem_lector.release() # Desbloquear el acceso al archivo para otros lectores

if __name__ == "__main__":
    archivo = Archivo()
    hilos = []
    
    for i in range(2):
        hilo_lector = threading.Thread(target=archivo.leer, args=(i,))
        hilo_lector.start()
        hilos.append(hilo_lector)

    for i in range(2):
        hilo_escritor = threading.Thread(target=archivo.escribir, args=(i,))
        hilo_escritor.start()
        hilos.append(hilo_escritor)

    for hilo in hilos:
        hilo.join()

    archivo.archivo.close() # Cerrar el archivo al finalizar
