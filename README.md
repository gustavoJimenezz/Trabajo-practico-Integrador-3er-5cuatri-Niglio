# Trabajo Práctico Taller Integrador - CABA 1C 2025 (Niglio)

Este proyecto consiste en implementar una API REST de gestión de hoteles, diseñada para interactuar con el cliente frontend entregado por el profesor.

## Integrantes

- Veronica Andrea Girardi  
- Alex Gustavo Jiménez  
- Tomás Agustín Lanza  

## Requisitos Previos

### Instalaciones necesarias

- **Docker**  
  Instalar Docker siguiendo la guía oficial:  
  https://docs.docker.com/get-docker/

---

## Ejecución de la Aplicación con Docker Compose

Este es el método recomendado para levantar la aplicación y la base de datos en un entorno de desarrollo.

### Construir las imágenes de Docker

```bash
docker-compose build
```

Este comando leerá el `Dockerfile` y `docker-compose.yml` para construir las imágenes necesarias.

### Iniciar los servicios (API y Base de Datos)

```bash
docker-compose up -d
```

El flag `-d` (o `--detach`) inicia los servicios en segundo plano, liberando la terminal.

### Verificar el estado de los contenedores

```bash
docker-compose ps
```

---

### Detiene y elimina todos los contenedores

```bash
docker-compose dow
```

## Acceder a la API
Crear las base de datos
`http://localhost:5000/init-db`

Una vez que los contenedores estén levantados, la API estará accesible en:  
`http://localhost:5000`

---

## Desarrollo

### Ejemplo en Postman (o cualquier cliente HTTP)

- Header: `n-auth`  
- Value: `bearer <tu_jwt_aqui>`

---

## Estructura del Proyecto

```
C:.
├───app
│   ├───dao
│   │   └───__pycache__
│   ├───models
│   │   └───__pycache__
│   ├───redprints
│   │   └───__pycache__
│   ├───schemas
│   │   └───__pycache__
│   ├───utils
│   │   └───__pycache__
│   └───__pycache__
└───postgresql
    └───data
        └───volumen postgresql
```
