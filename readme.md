# Meteoreo

Este repositorio contiene el API de backend del sistema de monitoreo y control apra estaciones meteorológicas (meteoreo), así como el daemon que se conecta a las estaciones meteorológicas.

La forma más sencilla de hacer funcionar este sistema, es por el siguiente método.


Este documento a partir de este punto contiene mis ideas, y parte de las razones por las que elegí ciertas tecnologías. Así como el proceso de selección que me llevó a tomarlas.

La idea es que esto sirva como un registro informal de lo que pasa por mio cabeza, para poder formalizarlo después en la redacción del documento final que acompañará este proyecto.

## Identificación de requisitos

### Recabado de información del estado de las estaciones

Debido a la naturaleza autónoma de las estaciones meteorológicas, y a que el hecho que las mismas se encuentran sometidas a [something something] se busca crear un sistema centralizado de recolección de información 

### Conexión a estaciones remotas

La conexión a las estaciones remotas se creó como un sistema modular de conexiones. Teniendo el objetivo de la extensibilidad como objetivo prioritario para el sistema de interacción con las interfaces.

Cada sistema de conexión supone sus propios retos, si bien hay diversos métodos de conexión que podrían ser útiles para la conexión a las estaciones meteorológicas, se decidió enfocarse en la conexión vía SSH a las estaciones meteorológicas que poseen una RaspberryPI como *datalogger* y como medio de interfaz que se encuentran conectadas por medio de puerto serial a las mismas. Y de las estaciones meteorológicas Campbell, que poseen diversos protocolos de comunicación pero se decidió por utilizar el protocolo HTTP.

Para la conexión a las estaciones RaspberryPi se considera lo siguiente:

-  Actualmente cuentan con una VPN configurada para facilitar el acceso a SSH por medio de una dirección IP en el mismo segmento de red que el segmento al que se pretende el servidor final tenga.
- Ocasionalmente, las estaciones meteorológicas perderán acceso a la VPN, ya sea por fallas técnicas del servidor, del ISP, pérdidas de energía eléctrica o demás.
- Que una estación se encuentre fuera de línea de la VPN temporalmente no implica que esta no pueda operar, o incluso que no pueda contactar al servidor, tal como se observa en la **Figura 1.1**

![Figura 1.1](/home/thblckjkr/repos/tesis/resources/conexion.png)

Por esta razón se optó por tener un servicio de monitoreo bidireccional. Se pretende que cambiando el ejecutor de servicios, se pueda obtener la información de la estación meteorológica sin necesidad de realizar diferentes implementaciones para cada caso. En este caso, se pretende que un script funcione en el mismo 

#### Consideraciones de seguridad

Debido a que generalmente no se crea una red virtual privada separada para el manejo exclusivo de estaciones meteorológicas (ya que estas suelen instalarse sobre infraestructura existente) es importante tener consideraciones de seguridad respecto a el acceso a las estaciones, debido a que pueden ser un punto de acceso a una, otherwise, isolada y segura red.

**De la conexión del servidor a las estaciones meteorológicas**

Para realizar la conexión a las estaciones meteorológicas se requiere de acceso a la raspberrypi que funciona como puente entre ambas. Para realizar cambios, crear un servicio, y establecer la información del sistema con una mínima interacción se requiere de un usuario de alta prioridad a la máquina. En el caso del sistema operativo basado en linux que utilizan las estaciones, es el usuario con la mayor cantidad de procesos `root`.

Al considerarse comprometido el ambiente de la apliación, se consideraría comprometido el sistema completo. Ya que en este ambiente se encontrarán las contraseñas de acceso a la base de datos y la llave privada que se utiliza para hacer autenticación, si bien existen servicios como Aws-KMS (Key Management Service), el implementar un sistema tan robusto para la administración de secretos sale de los objetivos de este proyecto. (It's beyond scope).

Por lo tanto, se decidió crear un servicio que tome un usuario y password con acceso "root" de forma temporal (o al menos uno que tenga permisos de `sudoer`) y utilizarlo para almacenar la llave pública local del servidor para realizar operaciones sin tener un usuario/password almacenado en la base de datos que pudiera ser comprometido. De esta forma, se mitiga el impacto de una posible intrusión a la base de datos, para no comprometer las credenciales de acceso a las estaciones.

**De las estaciones meteorológicas al servidor**

Debido a que las estaciones meteorológicas suelen ser instaladas en puntos con poco o mínimo control de seguridad física, se busca mitigar el acceso de las estaciones meteorológicas a la base de datos en la que se centralizarán los datos. Por lo tanto, se decidió utilizar un protocolo de API para insertar los eventos.

TODO POR API.

## Diseño del sistema

También

### Casos principales para resolución

**Conectividad de red**

- No hay conexión de ninguna dirección
- No hay VPN pero sí conexión de la estación al servidor, 
- No hay servidor VPN

**Weewx, davis, serial overload:** Problemas de comunicación serial de Davis a la RPi.

Esto pasa cuando se des-sincroniza

- Reiniciar puerto serial. `vantage: Unable to wake up console` 

```
$ sudo wee_device --clear-memory
$ sudo wee_device --info

OSError: [Errno 11] Resource temporarily unavailable # This line is the important of the output
```

`sudo systemctl stop serial-getty@ttyS0.service`

Hacer retry para `sudo wee_device --info`



(IF TCP not running)

`/mount/usb/` proxy o port-forwarding



## Configuración de ambiente de desarrollo

El ambiente de desarrollo que se seleccionó para el proyecto fué seleccionado con el objetivo de

## Contenedor *docker* para desarrollo

Con la finalidad de tener un contenedor de desarrollo que pueda ser replicado con la mínima configuración se eligió la plataforma docker, por su amplia adopción y por las facilidades que ofrece para crear sistemas complejos que dependen de varios servicios sin tener que realizar configuraciones en el sistema que puedan ser perdidas al momento de cambiar a otro.

Debido a la sencillez que el sistema de cnfiguración de contenedores *docker compose* ofrece, se eligió para almacenar los parámetros de configuración de los contenedores en vez de crear comandos compatibles con docker para ello. Esto permite una fácil edición de los servicios y la aplicación de los mismos de una forma estandarizada que permite la fácil lectura de los parámetros.

El archivo de configuración fué almacenado en la raíz del proyecto, con el nombre de `docker-compose.yml` tal como el estándar de la utilería `docker-compose` sugiere, y este archivo tiene el contenido siguiente que se muestra en el listado [INSERTAR].

```yaml
version: '3.3'

services:
  mysql:
    image: mysql
    container_name: meteoreo-mysql
    environment:
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_USER: ${MYSQL_USER}
      SERVICE_TAGS: dev
      SERVICE_NAME: mysql
    ports:
      - "3306:3306"
    networks:
      - meteoreo-backend

  api:
    container_name: meteoreo-api
    build:
      context: ./
      dockerfile: Dockerfile
    volumes:
      - './:/app:delegated'
    depends_on:
      - mysql
    environment:
      - WEB_CONCURRENCY=2
      - PORT=80
      - PRE_START_PATH=/app/app/prestart.sh
      - GUNICORN_CMD_ARGS="--reload"
    ports:
      - "81:80"
    networks:
      - meteoreo-backend

networks:
  meteoreo-backend:
    driver: bridge
```

Las variables utilizadas para el sistema vienen del archivo `.env` en la raíz del proyecto. Estas variables tienen el

## *Devcontainer*

Para tener una plataforma de desarrollo sencilla de configurar para proveer la máxima compatibilidad de se utilizó de una herramienta relativamente común en el desarrollo de aplicaciones con Visual Studio Code, el uso de *devcontainers*. Estos son, un archivo de configuración que da indicaciones al editor de código para crear un ambiente a la medida dentro de un contenedor docker.

Para realizar la configuración de este contenedor, se creó un directorio en la raíz del repositorio* llamado `.devcontainer`, y dentro de este folder se puso un archivo `devcontainer.json` como se muestra en el listado [LISTADO]

```json
{
  "name": "Meteoreo API",
  "service": "api",
  "remoteUser": "root",
  "shutdownAction": "stopCompose",
  "workspaceFolder": "/app",
  "dockerComposeFile": "../docker-compose.yml",
  "extensions": [
	 "editorconfig.editorconfig",
	 "mikestead.dotenv",
	 "njpwerner.autodocstring",
	 "aaron-bond.better-comments",
	 "mhutchie.git-graph",
	 "hookyqr.beautify",
	 "magicstack.magicpython",
	 "gruntfuggly.todo-tree",
	 "ms-python.vscode-pylance",
	 "sleistner.vscode-fileutils"
	]
}
```

En este archivo se especifica un nombre para identificar el ambiente de desarrollo que sea reconocible por el desarrollador, la localización del archivo que describe el contenedor, y una lista de extensiones para el editor de código. Entre las más importantes se encuentra *pylance* y *magicpython*, las demás son meramente preferencias personales para el ambiente de programación.



## Selección del motor de base de datos

<!-- Casi todas las secciones de desrrollo, van ligadas a una de resultados.-->

Debido a la facilidad de uso que ofrecen las librerías de conexión *ORM* para la traducción de bases de datos a modelos de código, se decidió utilizarlas. La librería específica que se decidió utilizar para el desarrollo del proyecto es  *Masonite-ORM* debido a que ofrece un ambiente de trabajo agnóstico a otras librerías, y tiene una amplia compatibilidad con diferentes motores de bases de datos.

De acuerdo al artículo [10.1007/978-3-642-10424-4_13](https://link.springer.com/chapter/10.1007/978-3-642-10424-4_13), la 

Se preparó un script para la inserción de la información a la base de datos de la siguiente forma:





Con un tiempo de respuesta de *~[N]ms*, el sistema puede soprotar hasta N estaciones concurrentes.

Debido a que la recolección de los datos es por métodología pull y no push, es posible tener las estaciones en una cola que se ejecute hasta por un periodo de 5 minutos (que es un estándar en la recolección de datos de estaciones meteorológicas). Esto implica que la base de datos [X] puede soportar hasta [N x 60 x 5] datos de forma concurrente.



Tomando en cuenta las necesidades actuales del LCCA, y el estimado del tamaño de las redes de alta densidad (que pueden llegar hasta los N nodos como X artículo lo demuestra), no vale la pena el introducir la complejidad extra de un motor de base de datos desconocido y para el que no existen ORM's con soporte completo en el lenguaje de desarrollo. Porque no es un sistema de alta densidad de datos.



Si bien es posible escalar horizontalmente la infraestructura, se busca evitarlo ya que los diminishing returns del costo de tener que mantener un sistema de monitoreo no es costeable. Para los casos de sistemas de extremadamente alta densidad, se recomienda el crear varias instancias seccionadas en bases de datos, o escalar la base de con un redis en vez de escalar.



*%! Recordar que la información debe ser consultada desde el API, así que no sólo se tienen que tomar en cuenta la cantidad de query's por segundo que se requieren hacer para las inserciones, sino también para la consulta de datos.*



*%! Si lo que queremos es proveer herramientas para la gestión de calidad de los datos meteorológicos, la información tiene que tener en mente los principios Solidos y transaccionales, al menos en la creación de reportes basados en incidentes.*

El diagrama de la base de datos,

# Desarrollo del sistema de monitoreo

## Selección de un worker para correr los archivos

Estaba pensando en utilizar un sistema tal como *dramatiq.io* o *celery* para el desarrollo del worker/daemon que se encargará de realizar reportes, enviar  notificaciones, y monitorear los sistemas meteorológicos.

El problema que celery presenta, es que no se puede utilizar en este proyecto por la [limitada compatibilidad](https://dramatiq.io/motivation.html#compared-to). Y el competidor más convincente (dramatiq.io) no tiene soporte para conexiones a bases de datos estándar, sólo a RabbitMQ o Redis, en  este caso, nos supone un problema ya que no quiero iuntroducir la complejidad extra que supone una base de datos como es Redis para un proyecto en el que hay tan poca necesidad de paralelismo.

Además, viendo un ejemplo similar (icinga, debido a el codebase tan limpio y a que es open source), si ellos utilizan para un sistema a nivel mundial un sistema de reportes [que depende de systemd para llamar un script en php](https://github.com/Icinga/icingaweb2-module-reporting) este sistema similar, pero a menor escala no debería sufrir un impacto gra nde por hacer algo similar en python.

Entonces se decidió hacer un archivo "run.py" o similar, que sea llamado por systemd cada X minutos, para que funcione como base principal del monitoreo con daemon.

Aún no decido la estructura de los folders a tomar.

<!-- Decisiones de diseño -->



### Registros de conexión

Una de las desiciones que se tomó al momento de hacer el diseǹo de los registros de conexión, es mantener todo en archivos (serparados?) para el almacenamiento de la información.  Se utilizará la librería nativa de Python debido a que no es necesario importar algún tipo nuevo de configuración ni información, y a que

Se separaron los registros de información en dos tipos de archivos. En un log para datos d conexión, de estado de servicios y demás cosas que se requieran, y otro log para la información de errores y excepciones del sistema.





Tomar un Usuario y pasword, utilizarlos para subir a la raspberry el archivo de monitoreo ycrear un usuario y password para conectarse a la raspberry. (almacenarlos como variable de ambiente, en un .env)

*Seccion de trabajos futuros en el documento, robustecer los elementos de seguridad del sistema*.

**Tomar el XML para precargarme, o generar el XML en mi sistema?**

**Generate a XML according to the Schema http://cecatev.uacj.mx/Estaciones.xml after the request** (como si fuera un reporte)

**¿La última notificcación ha sido X, no ha habido cambios? ¿El Evento X ha sido resuelto?**
Inicio de evento y fin de evento. (para no almacenar el mismo evento X veces).


SystemD para manejar eventos en vez de un crontab en general. *Es lo más correcto* (buscar documentación al respecto).

### Decisiones al momento de crear la estructura para cargar los drivers para la extensibilidad del proyecto

Una de las promesas más importantes del proyecto es la promesa de la extensibilidad. Con sólo escribir un driver (que extiende a su vez un driver de conexión) y cambiar algunas líneas de código, debería poder crearse una conexión con un nuevo tipo de estación meteorológica.

Lo importante aquí es cómo hacer esta carga dinámica de drivers sin que exista una penalización muy grande en los tiempos de carga de cuando se lee la base de datos a cuando se instancia el driver de la estación.

Using factories should resolve this, right?

Hablar del principio de inversión de dependencias referencia [en este artículo](https://medium.com/@geoffreykoh/implementing-the-factory-pattern-via-dynamic-registry-and-python-decorators-479fc1537bbe)

*Dependencias inversas* https://medium.com/@geoffreykoh/implementing-the-factory-pattern-via-dynamic-registry-and-python-decorators-479fc1537bbe

*SCI-Hub* https://sci-hub.se/10.2514/6.2018-3856

https://www.weewx.com/docs/utilities.htm

10.2514/6.2018-3856

pi:climasUACJ





## Bitacora accionable

Idea para futuro: que un usuario pueda utilizar la interfaz gráfica para crear un "if X then do Y" y almacenarla ya sea como un paso extra en el script del driver de la estación meteorológica, o como código accionabvle (pasos)  en la base de datos. 
