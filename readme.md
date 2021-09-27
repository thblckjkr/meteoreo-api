# Meteoreo

Este repositorio contiene el API de backend del sistema de monitoreo y control apra estaciones meteorológicas (meteoreo), así como el daemon que se conecta a las estaciones meteorológicas.

La forma más sencilla de hacer funcionar este sistema, es por el siguiente método.


Este documento a partir de este punto contiene mis ideas, y parte de las razones por las que elegí ciertas tecnologías. Así como el proceso de selección que me llevó a tomarlas.

La idea es que esto sirva como un registro informal de lo que pasa por mio cabeza, para poder formalizarlo después en la redacción del documento final que acompañará este proyecto.

## Identificación de requisitos



## Diseño del sistema



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

Además, viendo un ejemplo similar (icinga, debido a el codebase tan limpio y a que es open source), si ellos utilizan para un sistema a nivel mundial un sistema de reportes [que depende de systemd para llamar un script en php](https://github.com/Icinga/icingaweb2-module-reporting) este sistema similar, pero a menor escala no debería sufrir un impacto grande por hacer algo similar en python.

Entonces se decidió hacer un archivo "run.py" o similar, que sea llamado por systemd cada X minutos, para que funcione como base principal del monitoreo con daemon.

Aún no decido la estructura de los folders a tomar.

<!-- Decisiones de diseño -->



### Registros de conexión

Una de las desiciones que se tomó al momento de hacer el diseǹo de los registros de conexión, es mantener todo en archivos (serparados?) para el almacenamiento de la información.  Se utilizará la librería nativa de Python debido a que no es necesario importar algún tipo nuevo de configuración ni información, y a que

Se separaron los registros de información en dos tipos de archivos. En un log para datos d conexión, de estado de servicios y demás cosas que se requieran, y otro log para la información de errores y excepciones del sistema.

### Seguridad para conexión a Raspberrys

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
