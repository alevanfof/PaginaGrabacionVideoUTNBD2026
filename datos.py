# -*- coding: utf-8 -*-
"""Datos de la presentación: voces, escenas, textos y capturas.

Cada escena equivale a una diapositiva y a un fragmento de audio.
El texto es el guion que se sintetiza; la web nunca lo muestra.
"""

VOCES = {
    "alejandro": {
        "nombre": "Alejandro Fernández",
        "voces_alternativas": [
            {"id": "principal", "voz": "es-AR-TomasNeural", "pitch": "0Hz", "rate": "-5%", "descripcion": "Voz normal"},
            {"id": "agudo", "voz": "es-AR-TomasNeural", "pitch": "+15Hz", "rate": "-3%", "descripcion": "Más agudo/ytho"},
            {"id": "grave", "voz": "es-AR-TomasNeural", "pitch": "-10Hz", "rate": "-7%", "descripcion": "Más grave"},
        ],
        "bloque": "Bloque 1 · Sistema, modelo e índices",
        "comision": "Comisión 2 · Grupo 3",
        "codigo": "C2-3",
        "intro_principal": (
            "Hola, soy Alejandro Fernández, y en este bloque presento el sistema y el modelo de datos "
            "del trabajo final."
        ),
    },
    "gabriel": {
        "nombre": "Gabriel Di Lorenzo",
        "voces_alternativas": [
            {"id": "principal", "voz": "es-CO-GonzaloNeural", "pitch": "0Hz", "rate": "-5%", "descripcion": "Voz normal"},
            {"id": "agudo", "voz": "es-CO-GonzaloNeural", "pitch": "+12Hz", "rate": "-4%", "descripcion": "Más agudo/tenso"},
            {"id": "grave", "voz": "es-CO-GonzaloNeural", "pitch": "-15Hz", "rate": "-6%", "descripcion": "Más grave/cálido"},
        ],
        "bloque": "Bloque 2 · Carga masiva, consultas y roles",
        "comision": "Comisión 2 · Grupo 3",
        "codigo": "C2-3",
        "intro_principal": (
            "Hola, soy Gabriel Di Lorenzo, y en este bloque presento la carga masiva de datos, "
            "las consultas y los roles de acceso."
        ),
    },
    "josue": {
        "nombre": "Josue Gallardo",
        "voces_alternativas": [
            {"id": "principal", "voz": "es-MX-JorgeNeural", "pitch": "0Hz", "rate": "-5%", "descripcion": "Voz normal"},
            {"id": "agudo", "voz": "es-MX-JorgeNeural", "pitch": "+18Hz", "rate": "-3%", "descripcion": "Más agudo/dulce"},
            {"id": "grave", "voz": "es-MX-JorgeNeural", "pitch": "-12Hz", "rate": "-8%", "descripcion": "Más grave/maduro"},
        ],
        "bloque": "Bloque 3 · Seguridad, transacciones y concurrencia",
        "comision": "Comisión 2 · Grupo 12",
        "codigo": "C2-12",
        "intro_principal": (
            "Hola, soy Josué Gallardo, y en este bloque presento la seguridad, las transacciones "
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
            "pedido, detalle de pedido, producto y categoría. El recorrido principal conecta esas "
            "entidades en ese orden. Aplicamos once correcciones al DER para reforzar la integridad: "
            "CHECK valida rangos, UNIQUE evita categorías duplicadas, y agregamos fechas por defecto y "
            "stock en producto. Guardamos el precio unitario en cada detalle para conservar el valor "
            "histórico de la venta aunque cambie el precio del producto. El total del pedido se calcula "
            "en una vista, evitando duplicar datos. Usamos MySQL ocho punto cero punto cuarenta y dos, "
            "en una instancia portable, puerto tres mil trescientos siete, con InnoDB y codificación "
            "UTF ocho EME BE cuatro."
        ),
        "grupos": [[0, 1], [2, 3, 4, 5]],
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
            "El script cero uno crea las cinco tablas y sus restricciones. Nombramos explícitamente "
            "claves y restricciones con prefijos pe ka, efe ka, u cu y che ka, para facilitar su "
            "identificación. En cliente, id cliente es la clave primaria y el DNI es único. También "
            "validamos el formato del email con CHECK. Las claves foráneas usan ON DELETE RESTRICT para "
            "impedir borrar registros relacionados. Elegimos CHECK nativo de MySQL ocho en lugar de "
            "triggers, y dejamos las reglas de integridad declaradas en el esquema. InnoDB administra "
            "las referencias y sus bloqueos. Las evidencias muestran una inserción válida y tres rechazos: "
            "categoría duplicada por UNIQUE, stock negativo por CHECK y cliente inexistente por clave "
            "foránea. Ahora ejecutamos SHOW CREATE TABLE cliente y probamos los cuatro casos para "
            "observar cómo cada restricción acepta o rechaza la operación."
        ),
        "pausas_despues": {
            3: {
                "ms": 35000,
                "mensaje": "Ejecutar SHOW CREATE TABLE y probar inserción válida, UNIQUE, CHECK y clave foránea.",
            }
        },
        "capturas": [
            {"archivo": "01_ok_insert_1.png", "epigrafe": "Inserción válida sobre cliente."},
            {"archivo": "03_err_unique.png", "epigrafe": "Rechazo por UNIQUE: categoría duplicada."},
            {"archivo": "04_err_check.png", "epigrafe": "Rechazo por CHECK: stock negativo."},
            {"archivo": "05_err_fk.png", "epigrafe": "Rechazo por clave foránea: cliente inexistente."},
        ],
        "grupos": [[0, 1, 2], [3, 4], [5, 6], [7, 8]],
    },
    {
        "id": "a3",
        "alumno": "alejandro",
        "kicker": "Bloque 1 · Índices",
        "titulo": "Consultas medidas con y sin índice",
        "subtitulo": "Igualdad, rango y JOIN sobre 80.000 pedidos",
        "texto": (
            "Creamos cinco índices para optimizar las consultas: dos sobre pedido, uno para los JOIN por "
            "cliente y dos sobre detalle de pedido y producto. Medimos tres consultas con y sin índices, "
            "con tres ejecuciones por caso y comparación de medianas. La igualdad mejoró una coma cinco "
            "veces, el rango dos coma dos y el JOIN cuatro coma cuatro. EXPLAIN muestra el acceso por "
            "índice; sin él, se recorren las ochenta mil filas de pedido. Ahora ejecutamos la consulta "
            "de igualdad y comparamos EXPLAIN y EXPLAIN ANALYZE con y sin índice; esperamos las "
            "mediciones antes de comparar resultados. El índice compuesto filtra por estado y fecha, "
            "y el de cliente acelera las uniones con pedidos."
        ),
        "pausas_despues": {
            3: {
                "ms": 25000,
                "mensaje": "Ejecutar EXPLAIN y EXPLAIN ANALYZE con y sin índice; comparar el plan y las mediciones.",
            }
        },
        "capturas": [
            {"archivo": "13_indices.png", "epigrafe": "Definición de los cinco índices."},
            {"archivo": "29_tiempos_indices.png", "epigrafe": "Comparación de tiempos con y sin índice."},
            {"archivo": "20_explain_e1_con.png", "epigrafe": "EXPLAIN con índice: acceso por índice."},
            {"archivo": "22_analyze_e1_sin.png", "epigrafe": "EXPLAIN ANALYZE sin índice: recorrido completo."},
        ],
        "grupos": [[0, 1], [2], [3], [4, 5]],
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
            "Para la carga masiva usamos SQL, sin procedimientos. Una CTE recursiva genera los dígitos "
            "del cero al nueve y CROSS JOIN produce hasta diez mil combinaciones. Así cargamos "
            "trescientos cuarenta y cinco mil diez registros: veinte mil clientes, cinco mil productos, "
            "ochenta mil pedidos y doscientos cuarenta mil detalles. MOD y CASE definen distribuciones, "
            "como la cantidad de productos por categoría. Verificamos los conteos, la ausencia de claves "
            "foráneas huérfanas, las fechas entre dos mil veinte y dos mil veintiséis, y la distribución "
            "de estados. Los detalles dan un promedio de tres productos por pedido. Ahora ejecutamos "
            "los conteos y las consultas de coherencia para comprobar los resultados. El script permite "
            "regenerar el conjunto de forma reproducible. Los datos semilla incluyen categorías y "
            "productos antes de crear pedidos; cada detalle debe apuntar a un pedido y un producto "
            "existentes."
        ),
        "pausas_despues": {
            2: {
                "ms": 20000,
                "mensaje": "Ejecutar los conteos por tabla y las consultas de coherencia de claves y pedidos.",
            }
        },
        "grupos": [[0, 1], [2, 3], [4, 5, 6, 7, 8]],
        "capturas": [
            {"archivo": "07_catalogos.png", "epigrafe": "Catálogos semilla cargados."},
            {"archivo": "08_verif_conteos.png", "epigrafe": "Conteos por tabla tras la carga masiva."},
            {"archivo": "12_verif_coherencia.png", "epigrafe": "Coherencia entre pedidos y detalles."},
        ],
    },
    {
        "id": "g4",
        "alumno": "gabriel",
        "portada": False,
        "kicker": "Bloque 2 · Análisis de rendimiento",
        "titulo": "Commits grupales para carga masiva",
        "subtitulo": "Estrategia de escalabilidad y optimización",
        "texto": (
            "La carga masiva usa transacciones controladas para limitar bloqueos prolongados. Agrupamos "
            "los cambios en commits de cinco mil filas, en lugar de confirmar cada fila por separado. "
            "Así reducimos operaciones de confirmación y mantenemos la coherencia referencial. Las "
            "consultas posteriores tardan menos de dos segundos en el entorno probado con SSD."
        ),
        "capturas": [
            {"archivo": "08_verif_conteos.png", "epigrafe": "Verificación de conteos tras carga masiva."},
            {"archivo": "12_verif_coherencia.png", "epigrafe": "Coherencia entre pedidos y detalles."},
        ],
        "grupos": [[0, 1], [2, 3]],
    },
    {
        "id": "g2",
        "alumno": "gabriel",
        "kicker": "Bloque 2 · Consultas y vistas",
        "titulo": "Seis consultas y cuatro vistas",
        "subtitulo": "JOIN, GROUP BY con HAVING, subconsultas y enmascaramiento",
        "texto": (
            "Implementamos seis consultas de negocio: cuatro requeridas —dos con JOIN, una con GROUP BY "
            "y HAVING, y una subconsulta—, más dos adicionales. Mostramos los diez pedidos de mayor "
            "monto, las ventas por categoría y los clientes VIP con más de diez mil pesos en compras. "
            "Creamos cuatro vistas: resumen de pedidos con total calculado, ventas por categoría y dos "
            "vistas para enmascarar datos. La vista pública muestra el nombre parcialmente y oculta parte "
            "del email y el teléfono. Ahora ejecutamos las consultas de pedidos y ventas, y consultamos "
            "la vista para comprobar el enmascaramiento. Las vistas permiten publicar los campos "
            "necesarios sin exponer directamente toda la información de las tablas."
        ),
        "pausas_despues": {
            3: {
                "ms": 25000,
                "mensaje": "Ejecutar las consultas de pedidos y ventas; consultar la vista pública y verificar el enmascaramiento.",
            }
        },
        "capturas": [
            {"archivo": "14_q1_join_top_pedidos.png", "epigrafe": "Top de pedidos por monto."},
            {"archivo": "16_q3_having_clientes_vip.png", "epigrafe": "Clientes VIP con HAVING."},
            {"archivo": "15_q2_join_ventas_categoria.png", "epigrafe": "Ventas agregadas por categoría."},
            {"archivo": "32_vista_cliente_publico.png", "epigrafe": "Vista de cliente público con datos enmascarados."},
        ],
        "grupos": [[0], [1], [2], [3, 4, 5]],
    },
    {
        "id": "g3",
        "alumno": "gabriel",
        "kicker": "Bloque 2 · Roles y acceso",
        "titulo": "Privilegios mínimos por rol",
        "subtitulo": "Analista sobre vistas, vendedor sobre pedidos",
        "texto": (
            "Creamos dos roles: analista, con SELECT sobre vistas de reporting, y vendedor, que consulta "
            "e inserta pedidos y detalles sin acceder a tablas maestras. El usuario TFI analista puede "
            "consultar tres vistas, pero no las tablas base. La consulta directa a cliente falla por "
            "permisos; a través de la vista funciona. Ahora ejecutamos ambas consultas y revisamos los "
            "privilegios efectivos para comprobar la diferencia. Cada rol recibe sólo las operaciones "
            "que necesita para su tarea."
        ),
        "pausas_despues": {
            1: {
                "ms": 20000,
                "mensaje": "Ejecutar una consulta directa a cliente y la misma consulta mediante la vista pública; revisar los permisos.",
            }
        },
        "capturas": [
            {"archivo": "42_grants_analista.png", "epigrafe": "Privilegios del rol analista."},
            {"archivo": "45_acceso_restringido.png", "epigrafe": "Acceso denegado a la tabla base."},
        ],
        "grupos": [[0, 1], [2, 3, 4]],
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
            "Para evitar inyección SQL usamos un procedimiento almacenado parametrizado: el valor "
            "VARCHAR no se concatena ni se ejecuta como SQL dinámico. La entrada de prueba comilla, OR, "
            "comilla, uno, comilla, igual, comilla, uno se trata como dato literal y devuelve cero filas. "
            "También comprobamos que CHECK, la clave foránea y UNIQUE rechacen valores inválidos o "
            "duplicados. Ahora probamos el procedimiento con un DNI válido y con la entrada de prueba."
        ),
        "pausas_despues": {
            1: {
                "ms": 15000,
                "mensaje": "Ejecutar la búsqueda con un DNI válido y con la entrada de prueba para confirmar que no se interpreta como SQL.",
            }
        },
        "capturas": [
            {"archivo": "39_inyeccion_bloqueada.png", "epigrafe": "Intento de inyección tratado como dato literal."},
            {"archivo": "37_integr_check.png", "epigrafe": "CHECK rechazando un estado inválido."},
        ],
        "grupos": [[0, 1], [2, 3]],
    },
    {
        "id": "j2_1",
        "alumno": "josue",
        "kicker": "Bloque 3 · Transacciones",
        "titulo": "COMMIT y ROLLBACK sobre el stock",
        "subtitulo": "SELECT FOR UPDATE y validaciones de negocio",
        "texto": (
            "sp_registrar_venta controla el stock en una transacción, bloquea la fila con SELECT FOR "
            "UPDATE y valida las reglas de negocio. COMMIT confirma y ROLLBACK revierte si algo falla. "
            "En el caso exitoso, el stock pasa de cincuenta a cuarenta y cinco; ahora lo ejecutamos y "
            "revisamos ambos valores. Si falta stock, el cliente no está activo o el producto no existe, "
            "la venta no se confirma. Probamos el rollback por falta de stock y comprobamos que no "
            "queden cambios."
        ),
        "pausas_despues": {
            0: {
                "ms": 15000,
                "mensaje": "Ejecutar la venta válida y comparar el stock antes y después del COMMIT.",
            },
            1: {
                "ms": 15000,
                "mensaje": "Ejecutar la venta sin stock y verificar que el ROLLBACK no deje cambios.",
            },
        },
        "capturas": [
            {"archivo": "47_tx_commit.png", "epigrafe": "COMMIT: stock actualizado."},
            {"archivo": "48_tx_stock_insuficiente.png", "epigrafe": "ROLLBACK por stock insuficiente."},
        ],
        "grupos": [[0, 1, 2], [3, 4]],
    },
    {
        "id": "j2_2",
        "alumno": "josue",
        "kicker": "Bloque 3 · Propiedades ACID",
        "titulo": "Las cuatro propiedades ACID explicadas",
        "subtitulo": "Atomicidad, Consistencia, Aislamiento y Durabilidad",
        "texto": (
            "La transacción cumple ACID. Atomicidad: BEGIN y COMMIT agrupan los pasos, y ROLLBACK elimina los cambios parciales si falla una validación. Consistencia: exige stock suficiente, cliente activo y producto existente, además de respetar los CHECK. Aislamiento: SELECT FOR UPDATE bloquea la fila del producto y evita vender simultáneamente la última unidad. Durabilidad: InnoDB registra los cambios confirmados en su redo log."
        ),
        "capturas": [
            {"archivo": "47_tx_commit.png", "epigrafe": "COMMIT garantiza persistencia ACID."},
            {"archivo": "50_tx_cliente_inexistente.png", "epigrafe": "Rollback por cliente inexistente."},
        ],
        "grupos": [[0, 1, 2], [3, 4]],
    },
    {
        "id": "j2_3",
        "alumno": "josue",
        "kicker": "Bloque 3 · Nivel de aislamiento",
        "titulo": "Niveles de aislamiento: REPEATABLE READ vs READ COMMITTED",
        "subtitulo": "Comparación y efectos prácticos",
        "texto": (
            "El script ocho documenta las validaciones. InnoDB usa REPEATABLE READ por defecto. En una "
            "sesión leemos un valor, lo cambiamos y confirmamos desde otra; repetimos con READ COMMITTED "
            "para comparar las lecturas."
        ),
        "pausas_despues": {
            1: {
                "ms": 15000,
                "mensaje": "Comparar la segunda lectura en dos sesiones con REPEATABLE READ y READ COMMITTED.",
            }
        },
        "capturas": [
            {"archivo": "55_isolation.png", "epigrafe": "REPEATABLE READ vs READ COMMITTED."},
            {"archivo": "47_tx_commit.png", "epigrafe": "Snapshot de InnoDB bajo REPEATABLE READ."},
        ],
        "grupos": [[0], [1, 2]],
    },
    {
        "id": "j3",
        "alumno": "josue",
        "kicker": "Bloque 3 · Concurrencia",
        "titulo": "Deadlock, reintentos y aislamiento",
        "subtitulo": "Dos sesiones, error mil doscientos trece y recuperación",
        "texto": (
            "Simulamos un deadlock con dos sesiones: cada una bloquea un producto e intenta actualizar el "
            "que retiene la otra. Ahora reproducimos el bloqueo y observamos la respuesta de InnoDB. "
            "InnoDB detecta el ciclo y aborta una operación con el error mil doscientos trece. El "
            "procedimiento reintenta hasta tres veces con espera incremental. En síntesis, el trabajo "
            "integra carga de datos, consultas, roles, anti-inyección y concurrencia."
        ),
        "pausas_despues": {
            0: {
                "ms": 20000,
                "mensaje": "Ejecutar las dos sesiones en orden para provocar el deadlock y observar el error 1213.",
            },
        },
        "capturas": [
            {"archivo": "53_deadlock.png", "epigrafe": "Deadlock entre dos sesiones."},
            {"archivo": "54_deadlock_innodb.png", "epigrafe": "Error mil doscientos trece detectado por InnoDB."},
            {"archivo": "55_isolation.png", "epigrafe": "REPEATABLE READ frente a READ COMMITTED."},
        ],
        "grupos": [[0, 1], [2, 3], [4]],
    },
]


def escenas_de(alumno):
    return [e for e in ESCENAS if e["alumno"] == alumno]
