# FlaskDB

## Requisitos
* MongoDB corriendo, conectada con la aplicación usando el nombre de la database.
* PostgreSQL corriendo, conectada con la aplicación usando un nombre de usuario, constraseña y el nombre de la database.

## Funcionamiento
* `MongoDB query`: Ejecutar una consulta mongo especificando la colección, ejemplo
```js
myCollection.find()
```
* `PostgreSQL query`: Ejecutar una consulta sql especificando la tabla y atributos a consultar, ejemplo
```sql
SELECT * FROM myTable
```


## Pendiente:
* Agregar nombre y posible descripción a las consultas desde el archivo de texto
* Limpiar el evento "onClick"
* Mostrar el esquema de las respuestas en postgres
