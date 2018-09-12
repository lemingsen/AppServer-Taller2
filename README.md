[![Coverage Status](https://coveralls.io/repos/github/lucashemmingsen/AppServer-Taller2/badge.svg?branch=master)](https://coveralls.io/github/lucashemmingsen/AppServer-Taller2?branch=master)[![Build Status](https://travis-ci.com/lucashemmingsen/AppServer-Taller2.svg?branch=master)](https://travis-ci.com/lucashemmingsen/AppServer-Taller2)
# Application Server - Taller 2

Se trata de una aplicación por consola destinada a mantenerse en ejecución por períodos prolongados de tiempo.

Esta aplicación debe brindar una interfaz REST [1] para la comunicación de los diferentes usuarios.

Este servidor se comunicará con el _Shared server_ (explicado a continuación) a traves de la interfaz REST común definida para el mismo. En el caso que la _aplicación Android_ (explicada a continuación) necesitará de algún servicio del _Shared Server_, **el _Application server_ deberá de actuar de fachada.**.

#### Servicio de autenticación (login)
Este servicio permitirá a los usuarios poder ingresar al sistema, obteniendo un token que deberá ser utilizado por los demás servicios.

#### Servicio de registro
Este servicio permitirá a los usuarios darse de alta en el sistema.

#### Servicio de consulta de perfil
Este servicio permitirá consultar el perfil de un usuario. El mismo está compuesto por :
* Datos personales (Nombre, Apellido, EMail)
* Foto de perfil
* Actividades: resumen de la actividad del usuario dentro del sistema.

#### Servicio de modificación de perfil
Este servicio permite a un usuario actualizar su perfil, debe permitir modificar y actualizar los siguientes datos:
* Datos personales (Nombre, Apellido, EMail, Cuenta de Facebook, GMail, etc)
* Foto de perfil

#### Servicio chat comprador-vendedor
Después que un usuario haya realizado una compra, se habilitará un chat entre el usuario y el vendedor del artículo.

#### Servicio de publicación de articulo para la venta
Este servicio deberá disponibilizar el artículo para la venta. El artículo deberá contener al menos los siguientes datos:
* Nombre 
* Descripción
* Unidades disponibles
* Precio por unidad
* Fotos: 1 o más fotos
* Usuario que publica el producto.
* Ubicación geográfica del usuario
* Métodos de pago aceptados
* Categoría del artículo: electrodoméstico, mueble, muebles de exterior, usado, nuevo, etc.

Como respuesta de la publicación este servicio deberá generar un código QR que contendrá los datos necesarios del producto en cuestión.    

#### Servicio de alta de pregunta
Este servicio permitirá realizar una pregunta acerca de un artículo que se encuentra publicado para la venta.

#### Servicio de alta de respuesta a pregunta
Este servicio permitirá responder una pregunta que fue realizada.

#### Servicio de compra
Este servicio permitirá realizar la compra de un producto que se encuentra publicado. Ester servicio deberá devolver un código que identifica la compra de forma única y que permita conocer el estado de la misma (tracking). Se debe indicar el método de pago por el cual se abonará la compra. El pago es procesado por un sistema externo que no se encontrará disponible, de manera que el procesamiento del pago se realizará de forma manual desde la **Interfaz WEB** del sistema a través de un administrador del sistema. Por este motivo es necesario consultar al _Shared Server_ acerca del estado de la compra.

#### Servicio de tracking
Este servicio permitirá conocer el estado de una compra a través del código de tracking. Los estados posibles son:
* Compra realizada
* Pago pendiente de proceso
* Pago rechazado
* Pago aceptado
* Envío en progreso
* Pendiente de envío
* Envío realizado.

El envío es procesado por un sistema externo que no se encontrará disponible, de manera que la carga del estado del envío se realizará de forma manual desde la **Interfaz WEB** del sistema a través de un administrador del sistema. Por este motivo es necesario consultar al _Shared Server_ acerca del estado de la compra.

Una vez que el artículo se encuenrtre en eastado "Envío realizado" el sistema debe permitir calificar la compra realizada por el usuario.

#### Servicio de búsqueda de producto 
Este servicio debe permitir la búsqueda de un producto utilizando varios de sus atributos. Un ejemplo de estos:
* Búsqueda por cercanía (ubicacióren geográfica)
* Búsqueda por nombre
* Búsqueda por descripción

Este servicio de búsqueda devolverá cero, uno o más resultados coincidentes con la búsqueda realizada y ponderados por el sistema de puntuación que conformorá el orden de los resultados devueltos.

#### Servicio de cotización de viaje
Permite saber, con un margen de error, el costo de un envío antes de realizarlo. Este servicio será una fachada de uno proporcionado por el Shared Server.

#### Servicio de estado
Este servició tiene como objetivo brindar una respuesta rápida que permita ser consultada para conocer si el servidor se encuentra activo.
Este servicio debé ser consultado a traves de la URI /ping

#### Servicio de consulta de datos de uso
Este servicio deberá brindar datos acerca del uso del application server. Deberá ser consultado a traves de la URI /stats.

#### Sistema de puntuación
El sistema debe poseer una lógica que administre el puntaje del usuario dentro del sistema. Este puntaje es importante a la hora de publicar articulos a la venta ya que brindará mayor visibilidad a los artículos de los usuarios con mayor puntaje.

La lógica de la acumulación de puntos debe ser definida por el grupo. Un ejemplo de este puede ser:
* Suma de puntos por cada publicación realizada
* Suma de puntos por cada compra realizada
* Suma de puntos por pago por X método de pago
* Suma de puntos por primera compra/venta realizada
* Suma de puntos por reputación de usuario

### Tecnologias

* Lenguaje: [Python 3](https://www.python.org/) (`3.6.4`)
* Web Framework: [Flask](http://flask.pocoo.org/)
* WSGI HTTP Server: [Gunicorn](http://gunicorn.org/)
* Database: [MongoDB](https://www.mongodb.com/)  


### Empaquetamiento

Cada uno de los desarrollos solicitados debe empaquetarse según el estandar de la plataforma, es decir:

* _Application Server_: Python Setuptools (`setup.py` y `requeriments.txt`)


Además, ambos servidores deberán traer un `Dockerfile` que permita correrlos sin necesidad de tener instalado los respectivos lenguajes.

### Despliegue en la Nube

Ambos servidores, tanto el _Application server_ como el _Shared Server_, se deberán disponibilizar en la nube utilizando una plataforma como servicio (_PAAS_). Se recomienda usar [Heroku](https://www.heroku.com/) ya que cuenta con todos los requerimientos tecnológicos pedidos anteriormente.

### Log

Los servidores deben contar con un sistema de log en donde se registren los eventos que se generen durante la ejecución. El sistema de log debe permitir configurar el nivel de los eventos que desean registrar. Estos niveles son:

| Nivel | Condiciones |
| ----- | ----------- |
| Error | Condición de falla catastrófica, el sistema no puede funcionar. (criterio de las 2 a.m.) Condición que haga que la aplicación no pueda ejecutar una funcionalidad. Ejemplo: No es posible conectarse con la base de datos |
| Warn | Cualquier condición anómala que afecte el funcionamiento del sistema, pero no impida la funcionalidad básica Ejemplos: Uso de APIs deprecadas, Mal uso de APIs |
| Info | Cualquier acción correspondiente a un caso de uso iniciada por el usuario o el sistema. Información que permita trazar el historial de las entidades. Ejemplos: Conexión a la base de datos exitosa, Conexión de nuevo cliente |
| Debug | Información de contexto que permita resolver un problema técnico. Debe ser útil incluso sin el código fuente Ejemplo:  Datos de login para la DB |

Es necesario recalcar que para que un log sea útil, debe poder ser accedido.

### Pruebas y Métricas

El desarrollo de la aplicación se deberá adaptar a los estándares de calidad utilizados por AppMaker©. Dentro de estos estándares se encuentran:

* Pruebas unitarias [2]
* Métricas: code coverage debe ser mayor a 75% [3]
* Respetar estándar para estilo de codificación: Lint [4]
* Pruebas de integración utilizando python como lenguaje de scripting.
* Todas aquellas que se consideren convenientes para garantizar la calidad de las aplicaciones desarrolladas.

**Nota:** Esta sección hace solo referencía al _Application server_ y al _Shared server_. No se toma como requerimiento el realizar pruebas sobre el cliente Android.

### Integración continua / Despligue continuo

Las pruebas y métricas anteriormente mencionadas deberan correr bajo una plataforma de integración continua. Se sugiere el uso de [TravisCI](https://travis-ci.org/), pero se podrá utilizar otro previa justificación.

El resultado del _code coverage_ debe ser desplegado automáticamente a una plataforma que permita visualizarlas, entre muchas posibilidades se encuentran:

* [Coveralls](https://coveralls.io/)
* [Codecov](https://codecov.io/)
* Usar _Github Pages_ para generar una web para visualizarlo

Finalmente, el despliegue al servidor de _PAAS_ elegido deberá ser automático. Este deberá tener en cuenta como la actualización de la base de datos (cambios en las tablas, etc). El mecanismo utilizado para disparar dicho despliegue (utilizar el branch _master_ como productivo, utilizar un tags con nombre especial) será definido por los desarrolladores y deberá ser detallado en la documentación.

### Documentación

Se deberá entregar la siguiente documentación:

* Manual de administrador: Instalación y configuración
* Definición de Arquitectura / Diseño de la aplicación (**Debe incluir especificación de Api REST: [OpenAPI 2.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md)**)

Se espera que dicha documentación se elabore de manera incremental y que cada entrega parcial tenga parte de la misma.