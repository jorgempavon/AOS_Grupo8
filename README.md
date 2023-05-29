
# Práctica 2 AOS
El principal objetivo de esta tarea consiste en consolidar los conceptos relacionados con la infraestructura y el despliegue de una aplicación que sigue una arquitectura orientada a servicios.
Porfavor, se ruega la lectura de este readme antes de desplegar los servicios contenidos en el respositorio.


### Características de Factura

A nuestro grupo, se nos asignó el subsistema de gestión de facturas. Una factura está formada por los siguientes atributos:
* Identificador de factura
* Identificador cliente: Su respectivo DNI o NIE
* Array Identificadores de trabajos: Dado que en un coche se pueden realizar múltiples trabajos, estos deben aparecer en la factura
* fecha_factura: Fecha de emisión de la factura
* VIN_coche: VIN del vehiculo sobre el que se realizan los trabajos.
* estado: Estado de la factura, es decir, emitida o pagada
* importe_total: cantidad total que un cliente debe pagar por los bienes o servicios que ha recibido.


## Despliegue del mock de la api en local con docker compose

Aunque es cierto que el mock era requerido en la primera práctica, se ha decidido dejarlo en el repositorio ya que esto permite ver todo el trabajo del grupo durante toda la asignatura.
En caso de querer clonar el proyecto desde git, se debe ejecutar el siguiente comando:

```bash
  git clone https://github.com/jorgempavon/AOS_Grupo8.git
```
En caso de utilizar el zip entregado en moodle, hay que descomprimirlo en el lugar que se desee almacenar la práctica.

A continuación se debe de ir al directorio donde se encuentra el proyecto:

```bash
  cd AOS_Grupo8
```

Para ejecutar el mock de la api con Docker usamos el siguiente comando:

```bash
  docker-compose -f docker-compose-mock.yaml up
```
El comando docker compose up, nos pemite a partir del docker-compose.yaml levantar tres contenedores:

"mock_backend" es el primer servicio que encontramos en el archivo.yaml y utiliza la imagen de Docker "stoplight/prism:4" para ejecutar un mock de nuestra especificación.

"frontend" es el segundo servicio que encontramos  y utiliza la imagen de Docker "swaggerapi/swagger-ui:latest" para lanzar una interfaz de usuario basada en Swagger de nuestro archivo openapi.yaml.

El último servicio se denomina "proxy" y utiliza la imagen de Docker "caddy:latest" para ejecutar un servidor proxy que permite enruta las peticiones entrantes a la API en el contenedor "mock_backend".

Para detener estos servicios que se ejecutan como contenedores de Docker, hay que ejecutar el siguiente comando en la misma carpeta donde se encuentra el archivo docker-compose.yml, para ello abra otra terminal y ejecute:
```bash
  docker-compose -f docker-compose-mock.yaml down
```
El comando docker compose down parará la ejecución de los contenedores y eliminará fichos contenedores especificados en el archivo docker-compose.yml. 
También puede eliminar estos contenedores mediante docker-desktop

## Despliegue de la api implementada en local con docker-compose
La implementación de la api está realizada con el framework de Flask en la ruta Back-end_Facturas. En dicha ruta encontramos:

Carpeta Software: Contiene el código de la implementación de la API

Carpeta venv: Entorno virtual para almacenar las dependencias del código

Carpeta Kubernets: Contiene los sripts para el despliegue en kubernetes de la aplicación, la base de datos y la interfaz de swagger.

Carpeta imagen_bd: contiene la imagen de la base de datos, la cual contiene una serie de facturas ya insertadas. Esta imagen se utiliza para el despliegue de la bd en kubernetes y esta subida en DockerHub

Carpeta imagen_swagger: contiene la imagen de swagger con la especificación realizada en la primera práctica (openapi.yaml). Esta imagen se utiliza para el despliegue de la bd en kubernetes y esta subida en DockerHub

Dockerfile: se trata de la imagen de la implementación de la api y se encuentra disponible en DockerHub

init.sql: script sql que permite la inserción en la bd de una serie de facturas al iniciarse por primera vez la base de datos

requirements.txt: Es un fichero generado con todas las dependencias del código implementado. Este fichero txt es utilizado en la creación de la imagen de la api.

docker-compose-implementado: Este fichero nos permite levantar tres contenedores:



"frontend" es el primer servicio que encontramos  y utiliza la imagen de Docker "swaggerapi/swagger-ui:latest" para lanzar una interfaz de usuario basada en Swagger de nuestro archivo openapi.yaml.

"bd-0" es el segundo servicio que encontramos en el archivo.yaml y aloja la base de datos MySQL.

"app" ejecuta la aplicación implementada que se comunica con la base de datos.
Los tres contenedores están conectados a la red mynetwork para permitir la comunicación entre ellos.

Una vez explicado el contenido de la carpeta Back-end_Facturas, para levantar el docker-compose-implementado.yaml seguir los siguientes pasos:



Situarse en la ruta /Back-end_Facturas:
```bash
  cd .\Back-end_Facturas\
```
Ejecutar el docker-compose-implementado.yaml:

```bash
  docker-compose -f docker-compose-implementado.yaml up --build
```
Una vez ejecutado el comando podremos observar el despliegue en local de la api implementada. Este despliegue nos permite ver que no es un mock y que es un depliegue real de nuestra aplicación, base de datos e interfaz de usuario.


## Despliegue en Kubernetes


Primero es recomendable situarse en la ruta \Back-end_Facturas

```bash
  cd .\Back-end_Facturas
```
Iniciar minikube:
```bash
  minikube start
```
Ejecutar en el siguiente comando:

Primero:
```bash
  kubectl apply -f .\kubernets\
```
Al aplicar dicho comando se  ejecutan los scripts de despliegue y creación de servicios de la base de datos, la aplicación y de la interfaz de swagger.
Merece la pena mencionar que al ser creados los 3 pods a la vez , puede que el pod denominado api-facturas tenga un status de error si aún no se ha terminado de crear la base de datos. Por ello aunque de error, si esperamos hasta que se cree el pod de la bd, el pod de api-facturas se reiniciará automáticamente y su estado cambiará a en ejecución.
Como se puede ver en el ejemplo de abajo, el pod de la api se crea antes y da error, pero una vez se crea el pod de la bd, el pod de la api se reinicia y se crea correctamente:
```bash
PS C:\Users\jorge\Escritorio\AOS_Grupo8\Back-end_Facturas> kubectl get pods
NAME                           READY   STATUS    RESTARTS   AGE
api-facturas-cddc5796-lfzfd    0/1     Error     0          4m34s
bd-0                           1/1     Running   0          4m35s
ui-facturas-78fdd5b568-scpl2   1/1     Running   0          4m34s
PS C:\Users\jorge\Escritorio\AOS_Grupo8\Back-end_Facturas> kubectl get pods
NAME                           READY   STATUS    RESTARTS      AGE
api-facturas-cddc5796-lfzfd    1/1     Running   1 (76s ago)   4m35s
bd-0                           1/1     Running   0             4m36s
ui-facturas-78fdd5b568-scpl2   1/1     Running   0             4m35s
```
También hay que rogar la paciencia a la hora de creación de los pods, ya que, como se puede ver arriba, tardan mucho en crearse y esto es debido a que el despliegue de estos pods hace referencia a las imágenes publicadas en DockerHub, dos de las cuales (la de la base de datos y la de la implemetación de la aplicación) con bastante pesadas.

En esta URL se puede consultar el repositorio en DockerHub con las 3 imágenes: https://hub.docker.com/repository/docker/jorgemp/aos_grupo8/general

Una vez realizados estos comandos en el orden indicado, se habrán creado 3 pods y 3 servicios. 
Ahora, para acceder a la interfaz de la UI desplegada en el pod ui-facturas, ejecutar el siguiente comando:
```bash
  minikube service ui-facturas
```
Dicho comando abrirá automáticamente una pestaña en el navegador accediendo así a la interfaz desplegada en kubernets.
Hay que mencionar que por una razón desconocida, desde la interfaz desplegada de swagger no permite realizar peticiones al pod que contiene la app.
Esto es un error  en el que se ha trabajado durante mucho tiempo pero no se ha logrado conseguir, además no tiene sentido que no funcione ya que si hacemos una petición  desde el pod en el que se encuentra la interfaz de swagger hacia el pod de la app, está devuelve correctamente la petición. Aquí un ejemplo:
```bash

PS C:\Users\jorge\Escritorio\AOS_Grupo8\Back-end_Facturas\kubernets> kubectl get pods    
NAME                           READY   STATUS    RESTARTS   AGE      
api-facturas-cddc5796-48jwj    1/1     Running   0          15m      
bd-0                           1/1     Running   0          16m      
ui-facturas-78fdd5b568-8jz8d   1/1     Running   0          15m      

```


En la imagen superior se ve que todos están en ejecución sin ningún problema.

Aquí se pueden ver los servicios, los cuales se denominan siempre igual, pero pueden tener diferentes IP´s de cluster:
```bash

PS C:\Users\jorge\Escritorio\AOS_Grupo8> kubectl get services
NAME           TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
api-facturas   ClusterIP      10.102.240.102   <none>        5000/TCP         136m
bd             ClusterIP      10.109.207.189   <none>        3306/TCP         137m
kubernetes     ClusterIP      10.96.0.1        <none>        443/TCP          138m
ui-facturas    LoadBalancer   10.98.216.152    <pending>     8080:30089/TCP   136m

```

IMPORTANTE recordar que cada vez que se ejecutan los script de despliegue de pods, cada pod se genera con un nombre nuevo, es decir, en la imagen superior
podemos ver que el pod api-facturas va seguido de una serie de números, estos son generados automáticamente por razones desconocidas.
Dichos nombres son generados automáticamente por kubernets y si se quieren hacer peticiones entre pods hay que poner correctamente e nombre del pod a la hora
de realizar comandos como el que se realiza a continuación.
```bash
  PS C:\Users\jorge\Escritorio\AOS_Grupo8\Back-end_Facturas\kubernets> kubectl exec ui-facturas-78fdd5b568-8jz8d -- curl http://api-facturas:5000/api/v1/facturas/2023-0000
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1071  100  1071    0     0   3919      0 --:--:-- --:--:-- --:--:--  3937
{
  "factura": {
    "Estado": "Emitida",
    "Fecha factura": "2023-05-16",
    "Id_cliente": "09975463Y",
    "Id_factura": "2023-0000",
    "Importe total": "233.00",
    "VIN_coche": "RT3DKGNF0KX480214",
    "trabajos": [
      "T222"
    ]
  },
  "links": {
    "cliente": {
      "href": "http://127.0.0.1:5000/api/v1/clientes/09975463Y",
      "rel": "cliente_get cliente_put cliente_delete cliente_options"
    },
    "parent": {
      "href": "http://127.0.0.1:5000/api/v1/facturas",
      "rel": "factura_post factura_cget factura_coptions"
    },
    "self": {
      "href": "http://127.0.0.1:5000/api/v1/facturas/2023-0000",
      "rel": "factura_get factura_delete factura_put factura_options"
    },
    "trabajos": [
      {
        "href": "http://127.0.0.1:5000/api/v1/trabajos/T222",
        "rel": "trabajos_get trabajos_put trabajos_delete trabajos_options"
      }
    ],
    "vehiculo": {
      "href": "http://127.0.0.1:5000/api/v1/vehiculos/RT3DKGNF0KX480214",
      "rel": "vehiculo_get vehiculo_put vehiculo_delete vehiculo_options"
    }
  }
}
```
Otro ejemplo: 
```bash
  PS C:\Users\jorge\Escritorio\AOS_Grupo8\Back-end_Facturas\kubernets> kubectl exec ui-facturas-78fdd5b568-8jz8d -- curl http://api-facturas:5000/api/v1/facturas/2023-0001
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1239  100  1239    0     0    97k      0 --:--:-- --:--:-- --:--:--  100k
{
  "factura": {
    "Estado": "Pagada",
    "Fecha factura": "2023-05-31",
    "Id_cliente": "04975462Y",
    "Id_factura": "2023-0001",
    "Importe total": "500.00",
    "VIN_coche": "RT3DKGNF0KX480214",
    "trabajos": [
      "T222",
      "T555"
    ]
  },
  "links": {
    "cliente": {
      "href": "http://127.0.0.1:5000/api/v1/clientes/04975462Y",
      "rel": "cliente_get cliente_put cliente_delete cliente_options"
    },
    "parent": {
      "href": "http://127.0.0.1:5000/api/v1/facturas",
      "rel": "factura_post factura_cget factura_coptions"
    },
    "self": {
      "href": "http://127.0.0.1:5000/api/v1/facturas/2023-0001",
      "rel": "factura_get factura_delete factura_put factura_options"
    },
    "trabajos": [
      {
        "href": "http://127.0.0.1:5000/api/v1/trabajos/T222",
        "rel": "trabajos_get trabajos_put trabajos_delete trabajos_options"
      },
      {
        "href": "http://127.0.0.1:5000/api/v1/trabajos/T555",
        "rel": "trabajos_get trabajos_put trabajos_delete trabajos_options"
      }
    ],
    "vehiculo": {
      "href": "http://127.0.0.1:5000/api/v1/vehiculos/RT3DKGNF0KX480214",
      "rel": "vehiculo_get vehiculo_put vehiculo_delete vehiculo_options"
    }
  }
}
```
Como se puede ver arriba en las dos peticiones llega la respuesta del pod de la aplicación, confirmandose así que el despliegue funciona correctamete.
Lo único es que desde la interfaz de swagger en el pod de la ui-facturas no se puede realizar dicha petición por razones inexplicables.

También, si se deseea hacer peticiones a la app desde nuestro ordenador, se puede ejecutar:


```bash
  minikube service api-facturas
```
Dicho comando nos abrirá una página en nuestro navegador, recordar añadir a la ruta de la página abierta /api/v1/facturas o mirar las diferentes rutas definidas en el openapi.yaml para hacer peticiones.
Como equipo recomendamos ejecutar el comando superior y utilizar postman para hacer peticiones.

## Aspectos importantes de la práctica

### Endpoints de la API
La API tiene los siguientes endpoints:

| Método HTTP | Endpoint                     | Resultado                                                           |
|-------------|------------------------------|---------------------------------------------------------------------|
| GET         | /api/v1/facturas             | Obtiene todos las facturas                                          |
| POST        | /api/v1/facturas             | Inserta una nueva Factura                                           |
| OPTIONS     | /api/v1/facturas             | Devuelve la lista de los métodos HTTP soportados por este endpoint  |
| GET         | /api/v1/facturas/{id_factura}| Devuelve la factura identificadoa por `id_factura` si existe        |
| OPTIONS     | /api/v1/facturas/{id_factura}| Devuelve la lista de los métodos HTTP soportados por este endpoint  |
| PUT         | /api/v1/facturas/{id_factura}| Modifica la factura identificada por `id_factura` si existe         |
| DELETE      | /api/v1/facturas/{id_factura}| Elimina la factura identificada por `id_factura` si existe          |

La documentación completa de la API se encuentra en la interfaz de Swagger, o en la especificación OpenAPI
incluida en el fichero `/openapi/openapi.yml`

### Mock de los servicios restantes
Dado que nuestro grupo se encarga de la gestión de facturas, cada factura referencia a un cliente, un vehículo y a uno o varios trabajos, por lo tanto, cada vez que se introduce una nueva factura hay que comprobar si existe el cliente , el vehículo y los trabajos.
Por ello, cuando se recibe una nueva factura a insertar, se debería mandar una petición get al servicio de gestión de clientes con el id del cliente referenciado para ver si dicho cliente existe o no. También se debería hacer lo mismo con el id del vehículo y los id´s de trabajos.
Por lo tanto, en vez de realizar dichas peticiones a los servicios de los compañeros de otros grupos, se ha decidido mockear los servicios de los clientes, vehículos y trabajos.
Dicho mock, consiste en tres funciones que devuelven true o false para así simular el servicio de los compañeros. Dichas funciones se pueden encontrar en la ruta AOS_GRUPO8/Back-end_Facturas/Software/Facturas/controller_facturas/controller.py .

Estas son dichas funciones:
```python

 def mock_Cliente(id_cliente):
        return True
        return random.choice([True, False])

    def mock_Vehiculo(VIN_coche): 
        return True
        return random.choice([True,False])
    

    def mock_Trabajos(trabajos):
        return True
        return random.choice([True,False])

```
Todas devuelven True ya que se fuerza a que cada vez que se inserte una factura la función de cada mock simule que son válidos los valores del id del cliente del vehículo y de los trabajos.


## Autores [Equipo 8]

- JORGE MUÑOZ PAVÓN
- ADRIÁN GARCIA LOPEZ 
- MANUEL MORENO ASIAIN  
- JULIÁN NEVADO RAMOS 
- VICTOR TRAPERO CATALAN 


