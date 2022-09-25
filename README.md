# MeLiChallenge

INSTALACION:  
    - Clonar el repositorio  
    - Ubicarse en la carpeta raiz del proyecto.  
    - Abrir la consola y ejecutar el siguiente comando:  
        docker-compose run db  
    - Una vez esté corriendo el contenedor "db", ejecutar el siguiente comando en una consola nueva:  
        docker-compose run -i app  
    - Finalmente, se mostrará en consola el menú de la aplicación.  
    - Para correr el test se puede ejecutar el siguiente comando en consola:  
        docker exec <id del contenedor> python -m unittest discover  

FUENTES CONSULTADAS:  
    - https://developers.google.com/drive/api/quickstart/python  
    - https://developers.google.com/drive/api/v3/reference/files/list  
    - https://docs.docker.com/compose/gettingstarted/  
    - https://docs.python.org/es/3.9/library/unittest.html  
    

