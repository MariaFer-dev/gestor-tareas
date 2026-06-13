# Gestor de Tareas

Aplicación web CRUD desarrollada con Flask, SQLAlchemy y PostgreSQL online para gestionar proyectos y tareas con autenticación de usuarios.

## Funcionalidades

- Registro e inicio de sesión
- CRUD de proyectos
- CRUD de tareas
- Asignación de tareas a usuarios y proyectos
- Filtros por estado, prioridad y búsqueda
- Dashboard con métricas básicas
- Diseño frontend responsive con Bootstrap y CSS personalizado

## Tecnologías

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- PostgreSQL
- Bootstrap 5
- Vercel

## Modelo de datos

- Usuario: nombre, email, contraseña
- Proyecto: nombre, descripción
- Tarea: título, descripción, prioridad, estado, fecha límite, usuario asignado, proyecto

## Paso a paso para crear la base de datos online

La opción más simple para este proyecto es PostgreSQL en neon.

1. Crea una cuenta en NEON.
2. Crea un nuevo proyecto.
3. Ve a la sección de configuración de base de datos.
4. Copia la cadena de conexión PostgreSQL.
5. Crear estas variables de entorno:

```env
SECRET_KEY=una_clave_segura
DATABASE_URL=postgresql://usuario:password@host:puerto/base
```

6. Ejecuta la aplicación localmente con:

```bash
python app.py
```

## Despliegue en Vercel

1. Sube el proyecto a GitHub.
2. Conecta el repositorio a Vercel.
3. Agrega las variables de entorno `SECRET_KEY` y `DATABASE_URL`.
4. Vercel usará `api/index.py` como entrada de la aplicación.


## Capturas


- Pantalla de login
 ![Pantalla de login](images/image1.png)
- Dashboard principal
 ![Dashboard principal](images/image2.png)
- Listado de proyectos
 ![listado de proyectos](images/image3.png)
- Listado de tareas
  ![listado de tareas](images/image.png)

