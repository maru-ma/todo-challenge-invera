# ToDo-List APP (Python/Django)

### Ejecutar proyecto:
Es necesario tener instalado [docker](https://www.docker.com/) y [docker-compose](https://docs.docker.com/compose/).

```
$ docker-compose up --build

```
el proyecto se levanta en http://0.0.0.0:8000/ y la documentacion en http://0.0.0.0:8000/api/docs/ .

Para probar el proyecto es necesario crear un superuser:

```
$ docker exec -ti todo-app bash
$ python manage.py createsuperuser

```
luego en http://0.0.0.0:8000/api-auth/login/ loguearse como super user, dirigirse a http://0.0.0.0:8000/api/docs/#/users/users_create y crear un usuario.
O desde postman para testear con Token Auth, obtener token http://0.0.0.0:8000/api-token-auth/ .
#### Para ejecutar los tests:

```
$ docker-compose run --rm todo-app pytest

```


#### Entorno de desarrollo:

```
pip install pre-commit
pre-commit install

```
## Tareas de desarrollo y su duración:
* Diseño de aplicación: eleccion de MVP, modelos, tecnologías me llevó aprox 45min
* Setup inicial: con Docker, Docker-compose, Django, DRF, PostgreSQL, libs, pre-commits y hooks 1:30hs
* Modelos, serializadores, vistas y test de vistas: 1:30h
* Permisos, throttling, auth y adicion/corrección tests: 2hs
* Filters, paginacion y adicion/corrección tests: 2h

#### Quedan para mejorar y/o agregar:
* Al testear desde swagger las vistas de busqueda de Task agrega un parametro "search", sin embargo desde postman está ok (ej para probar desde postman con token auth:
>`http://0.0.0.0:8000/api/todo-lists/badefcc7-c757-452e-b7b3-98df5a78bce0/tasks/filter?done=false`
`http://0.0.0.0:8000/api/todo-lists/badefcc7-c757-452e-b7b3-98df5a78bce0/tasks/filter?created=2023-06-07`)
* Mejorar test unitarios y agregar para la creacion de Usuarios.
* Edición bulk de Task y TodoList.
