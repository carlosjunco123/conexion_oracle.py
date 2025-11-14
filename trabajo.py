import oracledb

# =========================
# CONFIGURAR THICK MODE
# =========================
instant_client_path = r"C:\Users\regio\Desktop\instantclient-basic-windows.x64-19.29.0.0.0dbru\instantclient_19_29"

try:
    oracledb.init_oracle_client(lib_dir=instant_client_path)
    print("✅ Thick mode activado correctamente.")
except Exception as e:
    print("❌ Error activando Thick mode:", e)

# =========================
# FUNCIÓN PARA CONEXIÓN
# =========================
def conectar():
    try:
        conn = oracledb.connect(
            user="system",
            password="Junco",
            dsn="localhost/XE"
        )
        print("✅ Conexión exitosa")
        return conn
    except oracledb.Error as e:
        print("❌ Error al conectar:", e)
        return None

# =========================
# LIMPIAR REGISTROS DE PRUEBA
# =========================
def limpiar_usuarios():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario >= 3")
        conn.commit()
        cursor.close()
        conn.close()

def limpiar_libros():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM libros WHERE id_libro >= 5")
        conn.commit()
        cursor.close()
        conn.close()

def limpiar_prestamos():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prestamos WHERE id_prestamo >= 4")
        conn.commit()
        cursor.close()
        conn.close()

# =========================
# FUNCIONES CRUD
# =========================

# --- USUARIOS ---
def insertar_usuario(id_usuario, nombre, correo):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (id_usuario, nombre, correo) VALUES (:1, :2, :3)",
            (id_usuario, nombre, correo)
        )
        conn.commit()
        print(f"Usuario '{nombre}' insertado")
        cursor.close()
        conn.close()

def mostrar_usuarios():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY id_usuario")
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]} | Nombre: {row[1]} | Correo: {row[2]}")
        cursor.close()
        conn.close()

def actualizar_correo(id_usuario, nuevo_correo):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET correo = :1 WHERE id_usuario = :2",
            (nuevo_correo, id_usuario)
        )
        conn.commit()
        print(f"Correo del usuario {id_usuario} actualizado")
        cursor.close()
        conn.close()

def eliminar_usuario(id_usuario):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = :1", (id_usuario,))
        conn.commit()
        print(f"Usuario {id_usuario} eliminado")
        cursor.close()
        conn.close()

# --- LIBROS ---
def insertar_libro(id_libro, titulo, id_autor, anio):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO libros (id_libro, titulo, id_autor, anio_publicacion) VALUES (:1, :2, :3, :4)",
            (id_libro, titulo, id_autor, anio)
        )
        conn.commit()
        print(f"Libro '{titulo}' insertado")
        cursor.close()
        conn.close()

def mostrar_libros():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_libro, titulo, id_autor, anio_publicacion FROM libros ORDER BY id_libro")
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]} | Titulo: {row[1]} | Autor ID: {row[2]} | Año: {row[3]}")
        cursor.close()
        conn.close()

# --- PRÉSTAMOS ---
def insertar_prestamo(id_prestamo, id_usuario, id_libro, fecha_prestamo, fecha_devolucion):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prestamos (id_prestamo, id_usuario, id_libro, fecha_prestamo, fecha_devolucion) "
            "VALUES (:1, :2, :3, TO_DATE(:4,'YYYY-MM-DD'), TO_DATE(:5,'YYYY-MM-DD'))",
            (id_prestamo, id_usuario, id_libro, fecha_prestamo, fecha_devolucion)
        )
        conn.commit()
        print(f"Préstamo de Usuario {id_usuario} Libro {id_libro} insertado")
        cursor.close()
        conn.close()

def mostrar_prestamos():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_prestamo, u.nombre, l.titulo, p.fecha_prestamo, p.fecha_devolucion
            FROM prestamos p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            JOIN libros l ON p.id_libro = l.id_libro
            ORDER BY p.id_prestamo
        """)
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]} | Usuario: {row[1]} | Libro: {row[2]} | Desde: {row[3]} | Hasta: {row[4]}")
        cursor.close()
        conn.close()

# =========================
# BLOQUE DE PRUEBA
# =========================
if __name__ == "__main__":
    # Limpiar registros de prueba
    limpiar_prestamos()
    limpiar_usuarios()
    limpiar_libros()

    # Usuarios
    insertar_usuario(3, "Ana Torres", "ana@email.com")
    mostrar_usuarios()
    actualizar_correo(3, "ana.nuevo@email.com")
    mostrar_usuarios()
    eliminar_usuario(3)
    mostrar_usuarios()

    # Libros
    insertar_libro(5, "Libro de Prueba", 1, 2025)
    mostrar_libros()

    # Préstamos
    insertar_prestamo(4, 1, 5, "2025-11-14", "2025-11-21")
    mostrar_prestamos()

    input("\nPresiona ENTER para salir...")
