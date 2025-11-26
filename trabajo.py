import oracledb
from datetime import datetime

# =======================================
#  ACTIVAR MODO THICK PARA ORACLE 11g
# =======================================
oracledb.init_oracle_client(
    lib_dir=r"C:\Users\regio\Desktop\instantclient-basic-windows.x64-19.29.0.0.0dbru (1)\instantclient_19_29"
)

# =======================================
#  CONEXIÓN A ORACLE
# =======================================
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

# =======================================
#  GENERAR ID AUTOMÁTICO
# =======================================
def generar_id(tabla, id_col):
    conn = conectar()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT NVL(MAX({id_col}),0) FROM {tabla}")
        max_id = cursor.fetchone()[0]
        return max_id + 1
    finally:
        cursor.close()
        conn.close()

# =======================================
#  VERIFICAR EXISTENCIA
# =======================================
def existe_usuario(correo):
    conn = conectar()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE correo = :correo", [correo])
        return cursor.fetchone()[0] > 0
    finally:
        cursor.close()
        conn.close()

def existe_libro(titulo):
    conn = conectar()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM libros WHERE titulo = :titulo", [titulo])
        return cursor.fetchone()[0] > 0
    finally:
        cursor.close()
        conn.close()

# =======================================
#  INSERTAR DATOS
# =======================================
def insertar_usuario(nombre, correo):
    if existe_usuario(correo):
        print(f"⚠️ Usuario con correo {correo} ya existe. Se omite inserción.")
        return
    idu = generar_id("usuarios", "id_usuario")
    if not idu:
        return
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc("sp_insertar_usuario", [idu, nombre, correo])
            conn.commit()
            print(f"👤 Usuario insertado: {nombre} (ID {idu})")
        except oracledb.Error as e:
            print("❌ Error al insertar usuario:", e)
        finally:
            cursor.close()
            conn.close()

def insertar_libro(titulo, anio, id_autor):
    if existe_libro(titulo):
        print(f"⚠️ Libro con título '{titulo}' ya existe. Se omite inserción.")
        return
    idl = generar_id("libros", "id_libro")
    if not idl:
        return
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc("sp_insertar_libro", [idl, titulo, anio, id_autor])
            conn.commit()
            print(f"📘 Libro insertado: {titulo} (ID {idl})")
        except oracledb.Error as e:
            print("❌ Error al insertar libro:", e)
        finally:
            cursor.close()
            conn.close()

def insertar_prestamo(id_usuario=None, id_libro=None, fecha_str="2025-11-26"):
    # Si no se pasa usuario o libro, usar los últimos insertados
    if not id_usuario:
        id_usuario = generar_id("usuarios", "id_usuario") - 1
    if not id_libro:
        id_libro = generar_id("libros", "id_libro") - 1
    idp = generar_id("prestamos", "id_prestamo")
    if not idp:
        return
    try:
        fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError as ve:
        print("❌ Formato de fecha incorrecto:", ve)
        return
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc("sp_insertar_prestamo", [idp, id_usuario, id_libro, fecha_dt])
            conn.commit()
            print(f"📚 Préstamo insertado (ID {idp})")
        except oracledb.Error as e:
            print("❌ Error al insertar préstamo:", e)
        finally:
            cursor.close()
            conn.close()

# =======================================
#  MOSTRAR VISTAS
# =======================================
def mostrar_vista(vista_nombre):
    conn = conectar()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {vista_nombre}")
        filas = cursor.fetchall()
        if not filas:
            print(f"⚠️ La vista {vista_nombre} no tiene registros.")
            return
        print(f"\n📄 VISTA: {vista_nombre}\n")
        for fila in filas:
            print(fila)
    except oracledb.Error as e:
        print(f"❌ Error al mostrar vista {vista_nombre}: {e}")
    finally:
        cursor.close()
        conn.close()

# =======================================
#  PRUEBA AUTOMÁTICA
# =======================================
if __name__ == "__main__":

    print("\n===== INSERTANDO DATOS =====")
    insertar_usuario("Carlos", "carlos@gmail.com")
    insertar_libro("Libro Python", 2025, 1)
    insertar_prestamo()  # Usará automáticamente el último usuario y libro

    print("\n===== MOSTRANDO VISTAS =====")
    mostrar_vista("vw_libros_detalle")
    mostrar_vista("vw_prestamos_detalle")

    print("\n===== FIN DE PRUEBA =====")
