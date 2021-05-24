# EcoBot

<!-- ACERCA DEL PROYECTO -->
## Acerca del Proyecto

Se presenta un sistema de recomendaciones de eficiencia energética para gestionar el uso de los electrodomésticos en los hogares mediante un bot de la aplicación de mensajería Telegram.
La comunicación con el sistema se establece mediante el escaneo de códigos QR asociados a distintos electrodomésticos. El código QR contiene información sobre las especificaciones de cada electrodoméstico como son la marca, modelo, categoría de eficiencia energética, etc. Dicho código QR es enviado mediante una fotografía, que es tratada de forma automática para distinguir el código QR del resto del entorno de la imagen tomada por el usuario.
Como respuesta a cada interacción iniciada por el usuario, se proporciona información de interés mediante preguntas sobre hábitos de eficiencia energética y tarifaria.

![image](https://user-images.githubusercontent.com/43879255/118670075-97b52100-b7f6-11eb-9555-7ac49291d749.png)
  
<!-- GETTING STARTED -->
## Getting Started

El repositorio contiene todo lo necesario para desplegar el sistema de manera local. Siga los siguientes pasos para su .

### Dependencias a instalar para la ejecución en local

1. Descarga e instalación de Docker Desktop para Windows desde la siguiente [URL](https://docs.docker.com/docker-for-windows/install/)
   
2. Si tu sistema operativo es Windows debes descargar el subsistema de Windows para Linux, para la ejecución de Docker. [URL](https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package) 

3. Instalación de MongoDB Server. [URL](https://www.mongodb.com/try/download/community?tck=docs_server)

4. Instalación del cliente MongoDB Composer. [URL](https://www.mongodb.com/try/download/compass)

5. Instalación del paquete XAMPP para el servicio web de comentarios PHP. [URL](https://www.apachefriends.org/download.html)

### Ejecución en Docker
A continuación, se deben construir las imágenes Docker en tu sistema local y finalmente instanciar los contenedores. Para ello, desde el terminal se ejecutan los siguientes comandos:
1. Construcción de las imágenes.
Ejemplo para la construir la imagen del servicio del bot, a ejecutar en terminal desde el directorio /src/bot.
   ```sh
   docker build -t bot .
   ``` 
2. Creación de red docker.
   ```sh
   Docker network create -–subnet=192.168.50.0/24 mynet
   ```  
3. Instanciación contenedores.
    Ejecución de los contenedores, ejemplo para el servicio del bot.
   ```sh
   docker run -d --name=qr-bot --net=mynet --ip=192.168.50.10 bot
   ```  

## Funcionalidad
El sistema está concebido bajo una arquitectura de microservicios. Los servicios presentes en el sistema son los siguientes:

**Bot de Telegram:**
Recibe los mensajes, fotografías y comandos de los usuarios. Además, cumple el papel de Gateway y redirige las imágenes o datos recibidos a los servicios correspondientes.

**Escáner de QR:**
Recibe las fotografías de los códigos QR tomadas por los usuarios y realiza un procesado de imagen para proceder con la decodificación del contenido del código QR.

**Gestor de datos:**
Gestiona todas las funciones de almacenamiento de información en la base de datos:
* **Logs**: Se guarda la información de cada escaneo del código QR junto con una serie de identificativos acerca del usuario de Telegram y, finalmente, fecha y hora del envío.
* **Usuarios**: Almacenamiento de datos acerca de cada usuario de Telegram con los que el bot entra en contacto.
* **Respuestas**: Guardado de las respuestas de los usuarios a las preguntas y recomendaciones enviadas.

**Motor de reglas:**
El motor de reglas se encarga de filtrar las preguntas y recomendaciones que son enviadas al usuario en función de una serie de criterios a partir de los datos que se extraen del escaneo del código QR: datos acerca del electrodoméstico, fecha y hora...
Se ha utilizado el motor de reglas durable-rules para la definición formal de las reglas, de manera que son agnósticas a cambios en el resto del código.

**Servicio de Comentarios:**
Sitio web que contiene una página para cada pregunta que envía el bot. En esta página se habilita la posibilidad de añadir comentarios a los usuarios, que se deben loguear en la página web a través de Telegram.

![image](https://user-images.githubusercontent.com/43879255/118670588-08f4d400-b7f7-11eb-8371-5d24f4774375.png)
![image](https://user-images.githubusercontent.com/43879255/118670711-245fdf00-b7f7-11eb-8442-5badd6d85eef.png)

<!-- CONTRIBUTING -->
## Autor✒️
Javier Martín Aizpuru




<!-- BIBLIOGRAFIA -->
## Construido con 🛠️

* [Pyzbar](https://pypi.org/project/pyzbar/) - Librería de Python para decodificación código QR.
* [Pillow](https://pypi.org/project/Pillow/) - Librería de Python para funciones de procesado de imagen.
* [Pymongo](https://pypi.org/project/pymongo/) - Cliente de MongoDB.
* [Durable-rules](https://pypi.org/project/durable-rules/) - Motor de reglas.
* [Telegram Bot API](https://core.telegram.org/bots/api) - API de Telegram para el desarrollo de bots.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png

