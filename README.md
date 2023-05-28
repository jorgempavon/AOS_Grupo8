
# Práctica 2 AOS
El principal objetivo de esta tarea consiste en consolidar los conceptos relacionados con la infraestructura y el despliegue de una aplicación que sigue una arquitectura orientada a servicios.
Porfavor, se ruega la lectura de este readme antes de desplegar los servicios contenidos en el respositorio.
Otro aspecto a comentar, porfavor, cada vez que se despliegue 

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

Carpeta imagen_bd: contiene la imagen de la base de datos, la cual contiene una serie de facturas ya insertadas. Esta imagen se utiliza para el despliegue de la bd en kubernetes

Carpeta imagen_swagger: contiene la imagen de swagger con la especificación realizada en la primera práctica (openapi.yaml). Esta imagen se utiliza para el despliegue de la bd en kubernetes

Dockerfile: se trata de la imagen de la implementación de la api.

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
En cuanto al despliegue en Kubernetes, se ha creado una carpeta denominada kubernets dentro de la ruta AOS_Grupo8\Back-end_Facturas\ . Esta carpeta contiene las siguientes carpetas:

despliegue_app:Esta carpeta contiene el archivo app_deployment.yaml que se encarga del despliegue de la imagen situada en la ruta AOS_GRUPO8\Back-end\,dicha imagen se subió al repositorio de Docker hub. Esta carpeta también contiene el app_service.yaml que crea el servicio para que así la aplicación pueda ser accedida desde otro pod.

despliegue_bd: Esta carpeta contiene el archivo stateful.yaml que se encarga del despliegue de la imagen situada en la carpeta imagen_bd en la ruta AOS_GRUPO8\Back-end\,dicha imagen se subió al repositorio de Docker hub. Esta carpeta también contiene el bd_service.yaml que crea el servicio para que así la base de datos pueda ser accedida desde otro pod.

despliegue_UI: Esta carpeta contiene el archivo ui_deployment.yaml que se encarga del despliegue de la imagen situada en la carpeta imagen_swagger en la ruta AOS_GRUPO8\Back-end\,dicha imagen se subió al repositorio de Docker hub. Esta carpeta también contiene el ui_service.yaml que crea el servicio para que así la interfaz de swagger sea accesible desde fuera del pod.

Una vez explicado todo, para realizar el despliegue en kubernetes, primero es recomendable situarse en la ruta \kubernets

```bash
  cd kubernets
```
Iniciar minikube:
```bash
  minikube start
```
Ejecutar en este orden los siguientes comandos:

Primero:
```bash
  kubectl apply -f .\despliegue_bd\
```
Segundo:
```bash
  kubectl apply -f .\despliegue_UI\
```
Tercero:
```bash
  kubectl apply -f .\despliegue_app\
```
La razón por la que se pide ejecutar los comandos en este orden es porque es necesario que se creen los servicios de la bd antes que los de la api para que cuando la api intente acceder a la base de datos esta ya exista.

Otro aspecto a mencionar es que al ejecutar el despliegue de la app  (kubectl apply -f .\despliegue_app\), este pod suele tardar unos 5 minutos o más en crearse ya que la imagen de la app es bastante pesada, pero se crea correctamente después de esperar un tiempo. A nosotros nos solía tardar 5 minutos en crearse el pod, además si ejecutamos el comando kubectl get pods mientras se crea el despliegue de la app, aunque tarde bastante podemos ver que el estado de el pod es CreatingContainer.

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
Dado que nuestro grupo se encarga de la gestión de facturas, cada factura referencia a un cliente, un vehículo y a uno o varios trabajos, por lo tanto, cada vez que se introduce una nueva factura hay que comprobar si existe el cliente , el vehículo y los trabajos.
Por ello, cuando se recibe una nueva factura a insertar, se debería mandar una petición get al servicio de gestión de clientes con el id del cliente referenciado para ver si dicho cliente existe o no. También se debería hacer lo mismo con el id del vehículo y los id´s de trabajos.
Por lo tanto, en vez de realizar dichas peticiones a los servicios de los compañeros de otros grupos, se ha decidido mockear los servicios de los clientes, vehículos y trabajos.
Dicho mock, consiste en tres funciones que devuelven true o false para así simular el servicio de los compañeros. Dichas funciones se pueden encontrar en la ruta AOS_GRUPO8/Back-end_Facturas/Software/Facturas/controller_facturas/controller.py


## Autores [Equipo 8]

- JORGE MUÑOZ PAVÓN
- ADRIÁN GARCIA LOPEZ 
- MANUEL MORENO ASIAIN  
- JULIÁN NEVADO RAMOS 
- VICTOR TRAPERO CATALAN 


