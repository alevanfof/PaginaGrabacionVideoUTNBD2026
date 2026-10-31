# Transcripción con marcas de tiempo

## Alejandro Fernández · Comisión 2 · Grupo 3

Duración total: **03:04**

| Escena | Inicio | Fin |
|---|---|---|
| a1 | 00:08 | 01:06 |
| a2 | 01:07 | 02:24 |
| a3 | 02:25 | 03:04 |

- **00:00** Hola, soy Alejandro Fernández, y en este bloque presento el sistema y el modelo de datos del trabajo final.
- **00:08** El sistema representa un comercio electrónico con 5 entidades principales, cliente, pedido, detalle de pedido, producto y categoría.
- **00:17** El recorrido principal es cliente, pedido, detalle del pedido, producto y categoría.
- **00:24** Aplicamos 11 correcciones al DER original para reforzar la integridad, agregamos restricciones check para validar rangos, y uniquen los nombres de categoría, valores por defecto para fechas y un campo de estoque en producto para controlar el inventario.
- **00:38** Una decisión importante fue guardar el precio unitario en detalle de pedido.
- **00:43** Así conservamos el precio histórico de cada venta aunque después cambia el precio del producto.
- **00:49** No agregamos una columna total a pedido porque el total se calcula dinámicamente en una vista.
- **00:55** Usamos MySQL 8.0.42, en una instancia portable, en el porto 3.307, con inodebí y codificación UTF8MV4.
- **01:07** El script 0.1, esquema, crea las 5 tablas y sus restricciones.
- **01:13** Nombramos explicitamente las claves y restricciones con prefijos como PC, FK, UCU y CHECA para facilitar su identificación y mantenimiento.
- **01:22** En cliente, por ejemplo, usamos y de cliente como clave primaria y una restricción unique para el DNI.
- **01:30** También validamos el formato del email con check.
- **01:34** Las claves foráneas usan ondelit restrict para evitar borrar registros que tienen información relacionada.
- **01:41** Consultamos expertos sobre la implementación de check in MySQL 8.0.3.
- **01:46** Y confirmamos que los check nativos son más eficientes y seguros bajo concurrencia.
- **01:51** También validamos que ondelit restrict sea su primera trigger tradicionales, ya que inodebí maneja los lax internamente evitando risk and distance.
- **02:00** En las evidencias vemos incertiones válidas y tres casos rechazados, una categoría duplicada por UNIC, un stock negativo por check y una referencia a un cliente inexistente por clave foránea.
- **02:12** Los errores aparecen documentados en los scripts.
- **02:16** La decisión de usar ondelit restrict sin trigger se valido consultando confuentes especializadas sobre manejo de integridad referencial en InodeV.
- **02:25** Para optimizar las consultas creamos cinco índices, uno compuesto sobre pedido por estado y fecha, otro por fecha, uno por id de cliente para lo SHOIN y dos índices en detalle de pedido y producto.
- **02:37** Medimos tres consultas con ICN índices, realizando 13 ejecuciones de cada una y comparando las medianas.
- **02:45** La consulta de igualdad mejoró 1,5 veces, la derrango 2,2 veces y el SHOIN 4,4 veces.
- **02:53** El explain permite ver la diferencia, con índices se accede directamente a las filas correspondientes, sin índice, se recorren las 80.000 filas de la tabla pedido.

## Gabriel Di Lorenzo · Comisión 2 · Grupo 3

Duración total: **02:26**

| Escena | Inicio | Fin |
|---|---|---|
| g1 | 00:09 | 01:14 |
| g2 | 01:15 | 01:55 |
| g3 | 01:56 | 02:26 |

- **00:00** Hola, soy Gabriel D. Lorenzo, y en este bloque presento la carga masiva de datos, las consultas
- **00:06** y los roles de acceso.
- **00:08** Para la carga masiva usamos S.S.E.U.L., sin procedimientos.
- **00:13** Una C.E.E., con montable express chain, recurse a generar los digitos del 0 al 9 y los combinamos
- **00:19** con croncroyo en para producir hasta 10.000 combinaciones.
- **00:23** Con esta estrategia generamos 345.000 filas manteniendo el rendimiento, tal como se recomendon
- **00:29** consultas técnicas sobre optimización de setes recursivos en maillases se huele 8.
- **00:35** Con esa técnica generamos 20.000 clientes, 5.000 productos, 80.000 pedidos y 240.000 detalles,
- **00:42** en total, 345.000.000 filas.
- **00:46** Usamos funciones como Maddy case para definir distribuciones, por ejemplo, asignar más productos
- **00:52** a ciertas categorías.
- **00:54** En las verificaciones compróbamos que cada tabla tenga la cantidad esperada, que no existan
- **00:59** claves foranias huérfanas y que las fechas estén dentro del rango 2020 a 2026.
- **01:05** También revisamos la distribución de estados.
- **01:08** Los 240.000 detalles para 80.000 pedidos dan un promedio de 3 productos por pedido.
- **01:15** Implementamos 6 consultas de negocio, 4 requerías, 2 con Join, una con Group
- **01:20** Byhaving, y una subconsulta, más dos adicionales.
- **01:25** Entre ellas, mostramos los 10 pedidos de mayor monto, las ventas por categoría y los clientes
- **01:30** vi a hípico más de 10.000 pesos en compras.
- **01:34** También creamos cuatro vistas, un resumen de pedidos que calcula el total, una vista
- **01:39** de ventas por categoría y dos vistas orientadas al enmascaramiento de datos.
- **01:44** En esta evidencia se ve la vista de cliente público, presenta el nombre de forma parcial,
- **01:49** oculta parte del email y oculta el teléfono para limitar la exposición de datos personales.
- **01:55** Para controlar el acceso creamos dos roles.
- **01:59** El rol analista tiene selectunicamente sobrevistas de reporting.
- **02:03** El rol bendedor puede consultar incertar pedidos y detalles, pero no tiene acceso a las tablas
- **02:08** maestras.
- **02:10** Los permiso del usuario TFI analistamos que puede consultar tres vistas, pero no las
- **02:15** tablas base.
- **02:17** Al intentar consultar directamente la tabla que interrecie un error de acceso enigado,
- **02:22** al hacer la consulta través de la vista, funciona.

## Josue Gallardo · Comisión 2 · Grupo 12

Duración total: **02:53**

| Escena | Inicio | Fin |
|---|---|---|
| j1 | 00:08 | 00:53 |
| j2 | 00:54 | 01:41 |
| j3 | 01:42 | 02:53 |

- **00:00** Hola, soy José Gallardo, y en este bloque presento la seguridad, las transacciones y la concurrencia.
- **00:08** Para evitar inyección SSIUL, creamos un procedimiento almacenado parametrizado.
- **00:15** El parámetro tiene tipo barcar y se usa como valor, no concatenamos SSIUL ni ejecutamos consultas dinámicas con PRIPF.
- **00:24** Al probar la cadena comilla simple, or, comilla simple, uno, comilla simple, igual, comilla simple, uno, comilla simple,
- **00:34** el procedimiento la trata como un dato literal y devuelve cero filas, en lugar de devolver todos los clientes.
- **00:41** También verificamos las restricciones de integridad, cheque rechaza estados inválidos, la clave foranea impide referencias a clientes inexistentes y unique evita duplicados.
- **00:53** Para registrar una venta completa implementamos el procedimiento registrar venta.
- **00:59** El procedimiento controla el stock con una transacción, bloquea la fila del producto consolact for update, valida las condiciones de negocio y confirma con comito revierte con rollback.
- **01:11** En el caso exitoso, el stock pasa de 50 a 45.
- **01:17** Si no hay stock suficiente, se ejecuta el rollback y el stock queda sin cambios.
- **01:23** También se valida que el cliente esté activo y que el producto exista, si una condición falla, no se persiste la venta.
- **01:31** La estrategia de mantenibilidad transaccional para cargas masivas también se valido con consultas técnicas sobre métodos robustos de bulkensor en Maya CCUL.
- **01:42** Para probar concurrencia simulamos un dedlack con dos sesiones.
- **01:46** La sesión ha bloqueado el producto 1 y la sesión ve bloquea el producto 2.
- **01:52** Después cada una intenta actualizar el producto bloqueado por la otra.
- **01:57** Y no debí detectar el ciclo y aborta una transacción con el error 1213.
- **02:03** El procedimiento contempla este error y reintenta hasta 3 veces con una espera incremental.
- **02:09** También comparamos los niveles reprobor ready red comat.
- **02:14** En repitabol, RID, una segunda lectura dentro de la misma transacción conserva la primera imagen de los datos.
- **02:22** En red comat, la segunda lectura puede ver los cambios confirmados por otra transacción.
- **02:28** En conclusión, implementamos las etapas del trabajo con 345.10 registros, consultas optimizadas, vistas y roles de seguridad.
- **02:38** Validaciones contra inyección y manejo transaccional del stock y la concurrencia.
- **02:44** Los scripts permiten reproducir las pruebas y las capturas documentan sus resultados.
- **02:50** Muchas gracias por su atención.
