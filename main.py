from functions.db.database import createDB, deleteDB
from functions.historical import getHistorical
from functions.drive import getDrive
import os

def main():
    createDB()
    while(True):
        print('\n Menú: \n'
            '1. Cerrar la sesión de usuario actual. \n'
            '2. Iniciar sesión y/o Ejecutar script. \n'
            '3. Mostrar Historico de archivos que fueron públicos. \n'
            '4. Eliminar todos los archivos de la base de datos. \n'
            '5. Terminar. \n')
        user_input = input('Ingrese una opción: ')
        if user_input == '1':
            try:
                #Al eliminar el archivo token.json perdemos los datos de la sesión activa
                os.remove('token.json')
                print("Sesión cerrada con éxito! \n")
            except:
                print("No tiene una sesión activa! \n")
        elif user_input == '2':
            getDrive()
        elif user_input == '3':
            getHistorical()
        elif user_input == '4':
            deleteDB()
        else:
            break



if __name__ == '__main__':
    main()