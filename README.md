
# Primera práctica de AOS

Este repositorio contiene la primera práctica de la asignatura Arquitecturas Orientadas a Servicios
del grado de Ingeniería del Software de la UPM. Esta práctica consiste en elaborar una especificación de una API
REST usando OpenAPI 3, además se utilizará Docker para ejecutar tres contenedores, uno actuará
como mock de la API (Stoplight Prism), otro como servidor Proxy (Caddy) y el último permitirá
realizar peticiones al mock mediante la interfaz de Swagger.

## Ejecutar el proyecto en local

Primero se debe de clonar este repositorio:

```bash
  git clone https://github.com/JCelayaRdz/Practica-AOS.git
```

A continuación se debe de ir al directorio donde se encuentra el proyecto:

```bash
  cd Practica-AOS
```

Para ejecutar el proyecto con Docker usamos el siguiente comando:

```bash
  docker compose up
```

Y por último, usando un navegador, si se visita la URL: http://localhost:8000/ 
se podrá interactuar con el mock de la API mediante la interfaz de Swagger.
Para parar el proyecto solo hace falta teclear Ctrl+C y para limpiar los recursos creados
por Docker es recomendable ejecutar el siguiente comando:

```bash
  docker compose down
```


## Decisiones de diseño de la API

A pesar de que las decisiones comentadas en este apartado
se pueden observar en la especificación, hemos considerado relevante
incluir su justificación.

### Atributos de cliente

Un cliente cuenta con los siguientes atributos:
* Identificador: Es su DNI o su NIE
* Nombre
* Apellidos
* Sexo: Masculino, Femenino, Otro
* Edad
* Número de teléfono
* Correo electrónico
* Dirección: Objeto que a su vez está formado por el nombre de la calle, el número de edificación y detalles adicionales
* Vehículos: Una lista que contiene el VIN de cada vehículo del cliente

### Atributos obligatorios del cliente

A la hora de añadir un cliente hemos considerado que los atributos obligatorios son:
* Identificador
* Nombre
* Apellidos
* Número de teléfono
* Vehículos

### Request bodies de POST y PUT

Los request bodies de las peticiones POST y PUT son las mismas (deben incluir los atributos obligatorios)
por las siguientes razones:

* Identificador: El cliente puede pasar de tener NIE a DNI
* Nombre y Apellidos: El cliente se puede cambiar el nombre y/o sus apellidos
* Número de teléfono: El cliente puede cambiarse de número de teléfono
* Vehículos: El cliente puede tener más o menos vehículos que cuando fue dado de alta en el sistema


### Posibilidad de eliminar clientes

La [LOPD](https://www.boe.es/buscar/doc.php?id=BOE-A-2018-16673) establece que la eliminación de los datos personales 
debe de realizarse de manera que se garantice la destrucción completa de los mismos, evitando cualquier tipo de acceso 
no autorizado. Es por ello que hemos considerado añadir un endpoint para eliminar los datos de un cliente por medio de
petición HTTP DELETE.

## Autores [Equipo 6]

- Juan Antonio Celaya Rodríguez
- Miguel Biondi Romero
- Fernando de Santos Montalvo
- Marcos Zapata Bueno

