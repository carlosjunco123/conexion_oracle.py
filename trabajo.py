import oracledb

try:
    # Conexión a Oracle
    conexion = oracledb.connect(
        user="system",               # Cambia por tu usuario si quieres
        password="Junco",            # Contraseña del usuario
        dsn="192.168.1.42:1522/FREE" # Host:Puerto/Servicio (según tu listener)
    )

    print("✅ Conexión exitosa a la base de datos Oracle")

    # Crear cursor y listar tablas del usuario
    cursor = conexion.cursor()
    cursor.execute("SELECT table_name FROM user_tables")

    print("📋 Tablas del usuario SYSTEM:")
    for tabla in cursor:
        print(" -", tabla[0])

    # Cerrar conexión
    cursor.close()
    conexion.close()
    print("🔒 Conexión cerrada correctamente")

except Exception as e:
    print("❌ Error al conectar o ejecutar la consulta:")
    print(e)
