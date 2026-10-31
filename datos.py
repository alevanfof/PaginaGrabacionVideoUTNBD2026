# -*- coding: utf-8 -*-
"""Datos de la presentación: voces, escenas, textos y capturas.

Cada escena equivale a una diapositiva y a un fragmento de audio.
El texto es el guion que se sintetiza; la web nunca lo muestra.
"""

VOCES = {
    "alejandro": {
        "nombre": "Alejandro Fernández",
        "voz": "es-AR-TomasNeural",
        "bloque": "Bloque 1 · Sistema, modelo e índices",
        "comision": "Comisión 2 · Grupo 3",
        "codigo": "C2-3",
        "intro": (
            "Hola, soy Alejandro Fernández, y en este bloque presento el sistema y el modelo de datos "
            "del trabajo final."
        ),
    },
    "gabriel": {
        "nombre": "Gabriel Di Lorenzo",
        "voz": "es-CO-GonzaloNeural",
        "bloque": "Bloque 2 · Carga masiva, consultas y roles",
        "comision": "Comisión 2 · Grupo 3",
        "codigo": "C2-3",
        "intro": (
            "Hola, soy Gabriel Di Lorenzo, y en este bloque presento la carga masiva de datos, "
            "las consultas y los roles de acceso."
        ),
    },
    "josue": {
        "nombre": "Josue Gallardo",
        "voz": "es-MX-JorgeNeural",
        "bloque": "Bloque 3 · Seguridad, transacciones y concurrencia",
        "comision": "Comisión 2 · Grupo 12",
        "codigo": "C2-12",
        "intro": (
            "Hola, soy Josue Gallardo, y en este bloque presento la seguridad, las transacciones "
            "y la concurrencia."
        ),
    },
}

ESCENAS = [
    # ---------------------------------------------------------------- ALEJANDRO
    {
        "id": "a1",
        "alumno": "alejandro",
        "portada": True,
        "kicker": "Bloque 1 · Sistema y modelo",
        "titulo": "Comercio electrónico: cinco entidades",
        "subtitulo": "Cliente, pedido, detalle de pedido, producto y categoría",
        "texto": (
            "El sistema representa un comercio electrónico con cinco entidades principales: cliente, "
            "pedido, detalle de pedido, producto y categoría. El recorrido principal es cliente, pedido, "
            "detalle del pedido, producto y categoría. "
            "Aplicamos once correcciones al DER original para reforzar la integridad: agregamos "
            "restricciones CHECK para validar rangos, UNIQUE en los nombres de categoría, valores por "
            "defecto para fechas y un campo de stock en producto para controlar el inventario. "
            "Una decisión importante fue guardar el precio unitario en detalle de pedido. Así conservamos "
            "el precio histórico de cada venta aunque después cambie el precio del producto. No agregamos "
            "una columna total a pedido porque el total se calcula dinámicamente en una vista. "
            "Usamos MySQL ocho punto cero punto cuarenta y dos, en una instancia portable, en el puerto "
            "tres mil trescientos siete, con InnoDB y codificación UTF ocho EME BE cuatro."
        ),
        "grupos": [[0, 1], [2, 3, 4, 5, 6]],
        "capturas": [
            {"archivo": "00_der.png", "epigrafe": "DER final: cinco entidades y sus relaciones."},
            {"archivo": "06_estado_etapa1.png", "epigrafe": "Estado de las tablas al cierre de la Etapa 1."},
        ],
    },
    {
        "id": "a2",
        "alumno": "alejandro",
        "kicker": "Bloque 1 · Esquema y constraints",
        "titulo": "Restricciones que sostienen la integridad",
        "subtitulo": "PK, FK, UNIQUE y CHECK con nombres explícitos",
        "texto": (
            "El script cero uno, esquema, crea las cinco tablas y sus restricciones. Nombramos "
            "explícitamente las claves y restricciones con prefijos como pe ka, efe ka, u cu y che ka, "
            "para facilitar su identificación y mantenimiento. "
            "En cliente, por ejemplo, usamos id cliente como clave primaria y una restricción UNIQUE "
            "para el DNI. También validamos el formato del email con CHECK. Las claves foráneas usan "
            "ON DELETE RESTRICT para evitar borrar registros que tienen información relacionada. "
            "Consultamos a expertos sobre la implementación de CHECK en MySQL ocho versus triggers, y "
            "confirmamos que los CHECK nativos son más eficientes y seguros bajo concurrencia. También "
            "validamos que ON DELETE RESTRICT sea superior a triggers tradicionales, ya que InnoDB maneja "
            "los locks internamente evitando race conditions. "
            "En las evidencias vemos inserciones válidas y tres casos rechazados: una categoría duplicada "
            "por UNIQUE, un stock negativo por CHECK y una referencia a un cliente inexistente por clave "
            "foránea. Los errores aparecen documentados en los scripts. La decisión de usar ON DELETE "
            "RESTRICT sin triggers se validó consultando con fuentes especializadas sobre manejo de "
            "integridad referencial en InnoDB."
        ),
        "capturas": [
            {"archivo": "01_ok_insert_1.png", "epigrafe": "Inserción válida sobre cliente."},
            {"archivo": "03_err_unique.png", "epigrafe": "Rechazo por UNIQUE: categoría duplicada."},
            {"archivo": "04_err_check.png", "epigrafe": "Rechazo por CHECK: stock negativo."},
            {"archivo": "05_err_fk.png", "epigrafe": "Rechazo por clave foránea: cliente inexistente."},
        ],
        "grupos": [[0, 1, 2], [3, 4], [5, 6], [7, 8, 9]],
    },
    {
        "id": "a3",
        "alumno": "alejandro",
        "kicker": "Bloque 1 · Índices",
        "titulo": "Consultas medidas con y sin índice",
        "subtitulo": "Igualdad, rango y JOIN sobre 80.000 pedidos",
        "texto": (
            "Para optimizar las consultas creamos cinco índices: uno compuesto sobre pedido por estado "
            "y fecha, otro por fecha, uno por id cliente para los JOIN, y dos índices en detalle de "
            "pedido y producto. "
            "Medimos tres consultas con y sin índices, realizando tres ejecuciones de cada una y "
            "comparando las medianas. La consulta de igualdad mejoró una coma cinco veces, la de rango "
            "dos coma dos veces y el JOIN cuatro coma cuatro veces. "
            "El EXPLAIN permite ver la diferencia: con índice se accede directamente a las filas "
            "correspondientes; sin índice, se recorren las ochenta mil filas de la tabla pedido."
        ),
        "capturas": [
            {"archivo": "13_indices.png", "epigrafe": "Definición de los cinco índices."},
            {"archivo": "29_tiempos_indices.png", "epigrafe": "Comparación de tiempos con y sin índice."},
            {"archivo": "20_explain_e1_con.png", "epigrafe": "EXPLAIN con índice: acceso por índice."},
            {"archivo": "22_analyze_e1_sin.png", "epigrafe": "EXPLAIN ANALYZE sin índice: recorrido completo."},
        ],
        "grupos": [[0], [1], [2], [3]],
    },
    # ------------------------------------------------------------------ GABRIEL
    {
        "id": "g1",
        "alumno": "gabriel",
        "portada": True,
        "kicker": "Bloque 2 · Carga masiva",
        "titulo": "345.010 filas generadas con SQL",
        "subtitulo": "CTE recursiva y producto cartesiano controlado",
        "texto": (
            "Para la carga masiva usamos SQL, sin procedimientos. Una CTE, Common Table Expression, "
            "recursiva genera los dígitos del cero al nueve y los combinamos con CROSS JOIN para producir "
            "hasta diez mil combinaciones. Con esta estrategia generamos trescientas cuarenta y cinco mil "
            "filas manteniendo el rendimiento, tal como se recomendó en consultas técnicas sobre "
            "optimización de CTEs recursivos en MySQL ocho. "
            "Con esa técnica generamos veinte mil clientes, cinco mil productos, ochenta mil pedidos y "
            "doscientos cuarenta mil detalles; en total, trescientas cuarenta y cinco mil diez filas. "
            "Usamos funciones como MOD y CASE para definir distribuciones, por ejemplo, asignar más "
            "productos a ciertas categorías. "
            "En las verificaciones comprobamos que cada tabla tenga la cantidad esperada, que no existan "
            "claves foráneas huérfanas y que las fechas estén dentro del rango dos mil veinte a dos mil "
            "veintiséis. También revisamos la distribución de estados. Los doscientos cuarenta mil detalles "
            "para ochenta mil pedidos dan un promedio de tres productos por pedido."
        ),
        "grupos": [[0, 1], [2, 3, 4], [5, 6, 7]],
        "capturas": [
            {"archivo": "07_catalogos.png", "epigrafe": "Catálogos semilla cargados."},
            {"archivo": "08_verif_conteos.png", "epigrafe": "Conteos por tabla tras la carga masiva."},
            {"archivo": "12_verif_coherencia.png", "epigrafe": "Coherencia entre pedidos y detalles."},
        ],
    },
    {
        "id": "g2",
        "alumno": "gabriel",
        "kicker": "Bloque 2 · Consultas y vistas",
        "titulo": "Seis consultas y cuatro vistas",
        "subtitulo": "JOIN, GROUP BY con HAVING, subconsultas y enmascaramiento",
        "texto": (
            "Implementamos seis consultas de negocio: cuatro requeridas, dos con JOIN, una con GROUP BY "
            "y HAVING, y una subconsulta, más dos adicionales. Entre ellas, mostramos los diez pedidos de "
            "mayor monto, las ventas por categoría y los clientes VIP con más de diez mil pesos en compras. "
            "También creamos cuatro vistas: un resumen de pedidos que calcula el total, una vista de ventas "
            "por categoría y dos vistas orientadas al enmascaramiento de datos. "
            "En esta evidencia se ve la vista de cliente público: presenta el nombre de forma parcial, "
            "oculta parte del email y oculta el teléfono para limitar la exposición de datos personales."
        ),
        "capturas": [
            {"archivo": "14_q1_join_top_pedidos.png", "epigrafe": "Top de pedidos por monto."},
            {"archivo": "16_q3_having_clientes_vip.png", "epigrafe": "Clientes VIP con HAVING."},
            {"archivo": "15_q2_join_ventas_categoria.png", "epigrafe": "Ventas agregadas por categoría."},
            {"archivo": "32_vista_cliente_publico.png", "epigrafe": "Vista de cliente público con datos enmascarados."},
        ],
        "grupos": [[0], [1], [2], [3]],
    },
    {
        "id": "g3",
        "alumno": "gabriel",
        "kicker": "Bloque 2 · Roles y acceso",
        "titulo": "Privilegios mínimos por rol",
        "subtitulo": "Analista sobre vistas, vendedor sobre pedidos",
        "texto": (
            "Para controlar el acceso creamos dos roles. El rol analista tiene SELECT únicamente sobre vistas "
            "de reporting. El rol vendedor puede consultar e insertar pedidos y detalles, pero no tiene acceso "
            "a las tablas maestras. "
            "Los permisos del usuario TFI analista muestran que puede consultar tres vistas, pero no las "
            "tablas base. Al intentar consultar directamente la tabla cliente recibe un error de acceso "
            "denegado; al hacer la consulta a través de la vista, funciona."
        ),
        "capturas": [
            {"archivo": "42_grants_analista.png", "epigrafe": "Privilegios del rol analista."},
            {"archivo": "45_acceso_restringido.png", "epigrafe": "Acceso denegado a la tabla base."},
        ],
        "grupos": [[0, 1, 2], [3, 4]],
    },
    # -------------------------------------------------------------------- JOSUE
    {
        "id": "j1",
        "alumno": "josue",
        "portada": True,
        "kicker": "Bloque 3 · Seguridad",
        "titulo": "Integridad y anti-inyección",
        "subtitulo": "Procedimiento parametrizado y restricciones activas",
        "texto": (
            "Para evitar inyección SQL, creamos un procedimiento almacenado parametrizado. El parámetro "
            "tiene tipo VARCHAR y se usa como valor; no concatenamos SQL ni ejecutamos consultas dinámicas "
            "con PREPARE. "
            "Al probar la cadena comilla simple, OR, comilla simple, uno, comilla simple, igual, comilla "
            "simple, uno, comilla simple, el procedimiento la trata como un dato literal y devuelve cero "
            "filas, en lugar de devolver todos los clientes. "
            "También verificamos las restricciones de integridad: CHECK rechaza estados inválidos, la "
            "clave foránea impide referencias a clientes inexistentes y UNIQUE evita duplicados."
        ),
        "grupos": [[0, 1], [2, 3]],
        "capturas": [
            {"archivo": "39_inyeccion_bloqueada.png", "epigrafe": "Intento de inyección tratado como dato literal."},
            {"archivo": "37_integr_check.png", "epigrafe": "CHECK rechazando un estado inválido."},
        ],
    },
    {
        "id": "j2",
        "alumno": "josue",
        "kicker": "Bloque 3 · Transacciones",
        "titulo": "COMMIT y ROLLBACK sobre el stock",
        "subtitulo": "SELECT FOR UPDATE y validaciones de negocio",
        "texto": (
            "Para registrar una venta completa implementamos el procedimiento registrar venta. El "
            "procedimiento controla el stock con una transacción, bloquea la fila del producto con SELECT "
            "FOR UPDATE, valida las condiciones de negocio y confirma con COMMIT o revierte con ROLLBACK. "
            "En el caso exitoso, el stock pasa de cincuenta a cuarenta y cinco. Si no hay stock suficiente, "
            "se ejecuta el rollback y el stock queda sin cambios. También se valida que el cliente esté "
            "activo y que el producto exista; si una condición falla, no se persiste la venta. La estrategia "
            "de mantenibilidad transaccional para cargas masivas también se validó con consultas técnicas "
            "sobre métodos robustos de bulk insert en MySQL."
        ),
        "capturas": [
            {"archivo": "47_tx_commit.png", "epigrafe": "COMMIT: stock actualizado."},
            {"archivo": "48_tx_stock_insuficiente.png", "epigrafe": "ROLLBACK por stock insuficiente."},
        ],
        "grupos": [[0, 1, 2], [3, 4, 5]],
    },
    {
        "id": "j3",
        "alumno": "josue",
        "kicker": "Bloque 3 · Concurrencia",
        "titulo": "Deadlock, reintentos y aislamiento",
        "subtitulo": "Dos sesiones, error 1213 y niveles de aislamiento",
        "texto": (
            "Para probar concurrencia simulamos un deadlock con dos sesiones. La sesión A bloquea el "
            "producto uno y la sesión B bloquea el producto dos. Después cada una intenta actualizar el "
            "producto bloqueado por la otra. InnoDB detecta el ciclo y aborta una transacción con el error "
            "mil doscientos trece. El procedimiento contempla este error y reintenta hasta tres veces con "
            "una espera incremental. "
            "También comparamos los niveles REPEATABLE READ y READ COMMITTED. En REPEATABLE READ, una "
            "segunda lectura dentro de la misma transacción conserva la primera imagen de los datos. En "
            "READ COMMITTED, la segunda lectura puede ver los cambios confirmados por otra transacción. "
            "En conclusión, implementamos las etapas del trabajo con trescientas cuarenta y cinco mil diez "
            "registros, consultas optimizadas, vistas y roles de seguridad, validaciones contra inyección y "
            "manejo transaccional del stock y la concurrencia. Los scripts permiten reproducir las pruebas "
            "y las capturas documentan sus resultados. Muchas gracias por su atención."
        ),
        "capturas": [
            {"archivo": "53_deadlock.png", "epigrafe": "Deadlock entre dos sesiones."},
            {"archivo": "54_deadlock_innodb.png", "epigrafe": "Error 1213 detectado por InnoDB."},
            {"archivo": "55_isolation.png", "epigrafe": "REPEATABLE READ frente a READ COMMITTED."},
        ],
        "grupos": [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9, 10]],
    },
]


def escenas_de(alumno):
    return [e for e in ESCENAS if e["alumno"] == alumno]
