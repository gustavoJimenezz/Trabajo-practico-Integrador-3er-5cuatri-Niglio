# Instalar dependencias

pip install -r requirements.txt

# Consigna

Realizar una API que permita gestionar las **habitaciones y reservas** en un hotel.

La misma debe ser desarrollada en **Python utilizando el framework Flask**.

La aplicación debe integrarse perfectamente con el **frontend brindado por el docente**.  
(Ante cualquier duda, ver el video explicativo).

---

## Requerimientos de la App

### 🔐 Autenticación

- Se debe validar la identidad de los usuarios utilizando **JWT**.
- Deben existir dos tipos de usuario:
  - **Cliente**
  - **Empleado**
- El tipo de usuario puede estar incluido dentro del **payload** del JWT.

---

### 🏨 Habitaciones

- Alta de habitaciones con:
  - **Número**
  - **Precio por día**
  - Solo accesible por **Empleado**.
  
- Edición del **precio** de una habitación (**Empleado**).

- Marcar una habitación como **inactiva** para que no aparezca en búsquedas (**Empleado**).
- Posibilidad de **reactivar** una habitación (**Empleado**).

---

### 📅 Reservas

- Registro de todas las habitaciones reservadas:
  - Puede ser un registro por **día reservado**, sin necesidad de usar rangos de fechas (**Empleado**).

- Se debe poder reservar una habitación específica eligiendo:
  - **Fecha de inicio**
  - **Fecha de fin**
  - Debe verificarse la disponibilidad antes de permitir la reserva (**Cliente**).

---

## 🛠 Requisitos Obligatorios

- Los **schemas** deben llamarse **DAO**.
- Los atributos de los modelos deben comenzar con el prefijo **`_`**.
- Los **Blueprints** deben llamarse **redprint**.
- Asegúrate de que todos los elementos de la API sigan las **convenciones y normas específicas** vistas anteriormente.

---

## 🔍 Búsquedas

- Buscar el listado de habitaciones disponibles en un **rango de fechas** (**Cliente**).
- Búsqueda por un **día en particular**, mostrando todas las habitaciones:
  - Debe discriminar cuáles están **disponibles** y cuáles **ocupadas** (**Cliente**).
- Buscar habitaciones con un **precio menor** al elegido (**Cliente**).
- Buscar una habitación en particular, mostrando:
  - Su **número**
  - **Precio**
  - Las **reservas** que posee (**Empleado**).

---

## ⚠️ Notas

Presta especial atención a:
- Los nombres de los modelos y sus atributos.
- La forma de estructurar los componentes de la aplicación.
- Seguir las convenciones y estructuras solicitadas para mantener coherencia en el diseño de la API.

## 🛠 Tecnologías Obligatorias

- **PostgreSQL**  
- **Redis** _(Deprecado)_  
- **Docker**  
- **Flask**  
- **SQLAlchemy**  
- **Blueprint**  
- **Marshmallow**  

---

## 📋 Requerimientos Obligatorios

- **Los nombres de las columnas en la base de datos NO pueden ser los mismos que los mostrados en los endpoints**.  
  - Es obligatorio que los **Schemas de Marshmallow** realicen el cambio de nombres.

- Todos los **ingresos de datos** deben ser validados mediante **Schemas de Marshmallow**, incluyendo:
  - Validaciones de tipos de datos.
  - Validaciones de reglas de negocio.

- Debe respetarse el uso correcto de los **verbos HTTP**:
  - **GET** → Obtener información o realizar búsquedas.
  - **POST** → Insertar nuevos datos.
  - **PUT** → Editar o actualizar datos existentes.
  - **DELETE** → Eliminar o dar de baja registros.

- Los archivos deben estar distribuidos en sus **carpetas correspondientes**, siguiendo buenas prácticas de organización.

- Debe existir un archivo **`README.md`** explicando el **paso a paso** para montar la aplicación.

- El proyecto debe ejecutarse sobre un servidor **WSGI**, como **Gunicorn**.

