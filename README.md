# Edugami-Test
Repositorio para la entrega de la prueba tecnica de Edugami

## Requisitos
- Python 3.x
- Git
- pip

## Instalacion y ejecucion
- pip install -r requirements.txt

- Crear propio archivo .env y asignar SECRET_KEY. 
- python -c "import secrets; print(secrets.token_urlsafe(50))" para crear una key

- python manage.py makemigrations
- python manage.py migrate
- python manage.py load_seed_data
- python manage.py runserver

## Rutas extras y ruta base
- Ruta base: localhost:8000/test
- Se creo la ruta extra [POST] localhost:8000/test/student para poder crear estudiante y testear las pruebas

## Respuesta para hacer recomendaciones para cada estudiante
Crearia un historial de pruebas de los alumnos donde podamos acceder a sus puntajes, areas fuertes y debilidades. Con esto monitorearia su progreso durante el tiempo, enfocandome en que tipo de respuestas se le hacen mas dificil o donde destaca mas. Con estos datos haria una comparacion contra la media del curso o incluso del historico de ese curso.

Con lo anterior entrenaria un LLM para identificar patrones y generar sugerencias para el alumno enfocandome en las areas a mejorar y sugerir pruebas o contenidos personalizados.

Para el modelo inicial rescataria los datos historicos de los cursos para enseñarle al modelo como han sido previamente los cursos y dejaria prompts para poder entregar valores especificos de cada estudiante para que me entregue recomendaciones.

De la mano con lo anterior dejaria un espacio para poder seguir entregandole valores al modelo para poder hacer un seguimiento continuo del estudiante y de esta forma que el modelo se vaya adaptando a el.

Otras consideraciones podrian ser tambien crear Dashboards o aplicaciones para visualizar la data de los estudiantes y poder enviarsela a los padres o estudiantes para que puedan visualizar de mejor manera su progreso.