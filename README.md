
# Práctica 1 AOS
El principal objetivo de esta tarea consiste en consolidar los conceptos relacionados con el diseño y la especificación de un servicio. En el caso de nuestro grupo, se nos encomendó la tarea de crear la especificación del servicio de facturas del taller mecánico. A continuación se definen las principales características de este servicio.

### Características de Factura

Una factura está formado por los siguientes atributos:
* Identificador de factura
* Identificador cliente: Su respectivo DNI o NIE
* Array Identificadores de trabajos: Dado que en un coche se pueden realizar múltiples trabajos, estos deben aparecer en la factura
* fecha_factura: Fecha de emisión de la factura
* VIN_coche: VIN del vehiculo sobre el que se realizan los trabajos.
* estado: Estado de la factura, es decir, emitida o pagada
* importe_total: cantidad total que un cliente debe pagar por los bienes o servicios que ha recibido.

Los request bodies de estos endpoints contienen los mismos atributos obligatorios:

* id_factura: Identificador único de la factura
* VIN_coche: VIN del vehículo beneficiado
* Id_cliente: DNI o NIE del cliente
* fecha_factura: fecha de emisión de la factura
* estado: Estado del cobro de la factura
* trabajos: Lista de trabajos realizados al vehículo


## Despliegue del proyecto en local


En caso de querer clonar el proyecto desde git, se debe ejecutar el siguiente comando:

```bash
  git clone https://github.com/jorgempavon/AOS_Grupo8.git
```
En caso de utilizar el zip entregado en moodle, hay que descomprimirlo en el lugar que se desee almacenar la práctica.

A continuación se debe de ir al directorio donde se encuentra el proyecto:

```bash
  cd AOS_Grupo8
```

Para ejecutar el proyecto con Docker usamos el siguiente comando:

```bash
  docker compose up
```
El comando docker compose up, nos pemite a partir del docker-compose.yaml levantar tres contenedores:

"mock_backend" es el primer servicio que encontramos en el archivo.yaml y utiliza la imagen de Docker "stoplight/prism:4" para ejecutar un mock de nuestra especificación.

"frontend" es el segundo servicio que encontramos  y utiliza la imagen de Docker "swaggerapi/swagger-ui:latest" para lanzar una interfaz de usuario basada en Swagger de nuestro archivo openapi.yaml.

El último servicio se denomina "proxy" y utiliza la imagen de Docker "caddy:latest" para ejecutar un servidor proxy que permite enruta las peticiones entrantes a la API en el contenedor "mock_backend".

Para detener estos servicios que se ejecutan como contenedores de Docker, hay que ejecutar el siguiente comando en la misma carpeta donde se encuentra el archivo docker-compose.yml:
```bash
  docker compose down
```
El comando docker compose down parará la ejecución de los contenedores y eliminará fichos contenedores especificados en el archivo docker-compose.yml. 

##Otros aspectos de la practica
Merece la pena mencionar, que el docker compose levanta el contenedor de UI mediante la especificación sin trozear mediante split, es decir, 
hay que tener en cuenta que dentro del subdirectorio openapi encontramos:
* openapi.yaml: Aqui se encuentra la especificación completa en un único fichero y es esta la que se utiliza para levantar el docker compose por indicación del profesor en una tutoría
* multifile: contiene la especificación en múltiples ficheros que permiten observar de una manera general la estructura de la especificación.
Para dividir la especificación en múltiples ficheros, se utilizó el siguiente comando:

```bash
  docker run -it --rm -v C:\<ruta_hasta_openapi.yaml>:/aos redocly/cli split /aos/openapi.yaml --outDir /aos/multiFile
```

El último aspecto a comentar, es que se revisaron los errores de la especificación mediante el siguiente comando:

```bash
  docker run --rm -v C:\<ruta_hasta_openapi.yaml>:/aos/openapi.yaml redocly/cli lint /aos/openapi.yaml
```

Después de aplicar el comando sólo se encontraron warnings y errores de seguridad. Estos errores se corregirían fácilmente añadiendo la autenticación mediante por ejemplo, jwt, con la cabecera authorization, pero el profesor indicó que no era necesario en esta primera práctica.

## Autores [Equipo 8]

- JORGE MUÑOZ PAVÓN
- ADRIÁN GARCIA LOPEZ 
- MANUEL MORENO ASIAIN  
- JULIÁN NEVADO RAMOS 
- VICTOR TRAPERO CATALAN 


