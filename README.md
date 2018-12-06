# App Server - Taller de programación II
[![Coverage Status](https://fiverr-res.cloudinary.com/images/t_main1,q_auto,f_auto/gigs/46941709/original/d5ace87ba59d0d4e5151668e60e8eaf673153ff7/build-api-in-python-flask.jpg)[![Build Status](https://g.foolcdn.com/art/companylogos/square/MDB.png)


![](https://sourcedexter.com/wp-content/uploads/2017/09/flask-python.png)
![](https://logosvector.net/wp-content/uploads/2015/10/mongodb-logo-vector-download.jpg)


## Documentación

**[Definición de la API](https://app-server-taller2.herokuapp.com/apidocs/)**

**[Definición de arquitectura / Diseño de la aplicación](https://github.com/DamiCassinotti/SharedServer-Taller2/blob/master/api/documentacion.yaml)**

**[Acceso al servidor](http://app-server-taller2.herokuapp.com/)**

## Instalación
Para poder instalar el servidor, primero debemos instalar Python 3 si no está instalado.
Una vez instalado Python debemos crear un virtualenv. Para hacerlo, escribimos el siguiente comando:

```
$ virtualenv venv --python=python3
```

Una vez creado, debemos activarlo, para esto vamos a la carpeta donde lo creamos y escribimos:

```
$ source bin/activate
(venv)$
```

Luego debemos ir a la carpeta principal de la aplicación y ejececutar el comando

```
$ python3 setup.py install
```

Seguido a esto ejecutamos el comando

```
$ pip3 install -r requirements.txt
```

El próximo paso será configurar todas las variables de ambiente necesarias para que la aplicación pueda ejecutarse.


## Base de datos
Podemos iniciar la aplicación con una instalación local de mongodb y luego ejecutar un script para crear los índices necesarios.


## Inicilización
Para inicializar el servidor de forma local se debe utilizar el siguiente comando:

```
$ gunicorn -b 127.0.0.1: 5000 "appserver.app:create_app()"
```

## Docker
No se pudo terminar de dockerizar la aplicación.


## Configuración
La mayor parte de la configuración se encuentra en variables de entorno.
```
MONGO_URI: ruta a la base de datos
FIREBASE_CONFIG: token necesario para autenticarse con firebase
JWT_SECRET_KEY: clave utilizada para la generación de tokens jwt
SWAGGER_FILE: ruta donde se encuentra el archivo de la especificación de api.
SHARED_SERVER_URI: url del shared server
SHARED_SERVER_FILE: nombre de archivo donde guarda el id del app server al registrarse. 
                    También se guarda aquí el token para acceder al mismo.
```

## Organización de directorios

```
/tests: tests
/docs: documentación
/appserver: directorio de la aplicación
  config.py: contiene la configuración de la aplicación, para ejecutarse en modo de desarrollo o de producción.
  app.py: main file
  /controllers: es el punto de acceso a la api, se encarga de recibir las peticiones y preparar las respuestas
  /data: capa de datos, encargada de interactuar entre la capa de servicios y la base de datos
  /models: entidades del modelo de negocio
  /services: capa de servicios, provee la lógica para el modelo de negocio
  /utils: utilidades
  /api: Contiene las clases necesarias para el funcionamiento de la aplicación
    /controllers: contiene las clases responsables de comsumir el modelo de datos
    /routes: contiene las clases que contiene las rutas de la aplicación (routing)
	/services: contiene las clases que consumen la base de datos
  /test: contiene los tests de la aplicación.
```

## Autenticación
Para la autenticación se utilizó [firebase](http://firebase.google.com/) y [flask-jwt-extended](https://github.com/vimalloc/flask-jwt-extended)

## Test
Para el desarrollo de los test unitarios se utilizan las siguientes herramientas:
 * [pytest](https://github.com/pytest-dev/pytest/): herramienta para realizar tests en python
 * [unittest.mock](https://github.com/python/cpython/blob/3.7/Lib/unittest/mock.py):librería para mocks en python

Para ejecutar los test:
```
$ pytest
```

## Tecnologias

* Lenguaje: [Python 3](https://www.python.org/) (`3.6.4`)
* Web Framework: [Flask](http://flask.pocoo.org/)
* WSGI HTTP Server: [Gunicorn](http://gunicorn.org/)
* Database: [MongoDB](https://www.mongodb.com/)  
* Database Cloud Service: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)


### Empaquetamiento


* _Application Server_: Python Setuptools (`setup.py` y `requeriments.txt`)


### Despliegue en la Nube

Plataforma: [Heroku](https://www.heroku.com//)


### Integración continua / Despligue continuo

Plataforma de integración continua: [TravisCI](https://travis-ci.org/)
Code coverage: [Coveralls](https://coveralls.io/)
