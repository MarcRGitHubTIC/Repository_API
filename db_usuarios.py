from client import db_client

def check_connection():
    """Verifica la conexión a la base de datos."""
    try:
        conn = db_client()
        conn.close()
        return {"status": 1, "message": "Conexión exitosa"}
    except Exception as e:
        return {"status": -1, "message": f"Error al conectar: {e}"}


def read_users():
    """Obtiene todos los usuarios de la tabla Usuarios."""
    conn = db_client()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario")
        data = cursor.fetchall()
        return {"status": 1, "data": data}
    except Exception as e:
        return {"status": -1, "message": f"Error en la consulta: {e}"}
    finally:
        conn.close()


def read_user_by_id(id_usuario: int):
    """Obtiene un usuario específico por su ID."""
    conn = db_client()
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM usuario WHERE userid = %s"
        cursor.execute(query, (id_usuario,))
        data = cursor.fetchone()
        return {"status": 1, "data": data}
    except Exception as e:
        return {"status": -1, "message": f"Error en la consulta: {e}"}
    finally:
        conn.close()


def read_aulas():
    """Obtiene todas las aulas de la tabla Aulas."""
    conn = db_client()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM aula")
        data = cursor.fetchall()
        return {"status": 1, "data": data}
    except Exception as e:
        return {"status": -1, "message": f"Error en la consulta: {e}"}
    finally:
        conn.close()


def insert_data(table_name: str, data: dict):
    """Inserta un registro en la tabla especificada."""
    conn = db_client()
    try:
        cursor = conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        return {"status": 1, "id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        return {"status": -1, "message": f"Error en la consulta: {e}"}
    finally:
        conn.close()

  
def read_fichajes():
    """Obtiene todos los registros de fichajes."""
    conn = db_client()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fichaje")
        rows = cursor.fetchall()
        return {"status": 1, "data": rows}
    except Exception as e:
        return {"status": -1, "message": f"Error al leer fichajes: {e}"}
    finally:
        conn.close()


def update_data(table_name: str, data: dict, condition: dict):
    """Actualiza un registro en la tabla especificada basado en una condición."""
    conn = db_client()
    try:
        cursor = conn.cursor()
        # Crear las cláusulas SET y WHERE dinámicamente
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        where_clause = " AND ".join([f"{key} = %s" for key in condition.keys()])
        
        # Crear la consulta SQL
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        
        # Ejecutar la consulta con los valores correspondientes
        cursor.execute(query, tuple(list(data.values()) + list(condition.values())))
        conn.commit()
        
        # Si todo fue bien, retornar mensaje de éxito
        return {"status": 1, "message": "Registro actualizado exitosamente"}
    
    except Exception as e:
        # Si ocurre un error, hacer rollback de la transacción
        conn.rollback()
        return {"status": -1, "message": f"Error en la consulta: {e}"}
    
    finally:
        # Asegurarse de cerrar la conexión
        conn.close()

def select_data(table_name: str):
    """Realiza una consulta SELECT sobre la tabla especificada."""
    conn = db_client()
    try:
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        data = cursor.fetchall()
        return {"status": 1, "data": data}
    
    except Exception as e:
        # Si ocurre un error, hacer rollback de la transacción
        conn.rollback()
        return {"status": -1, "message": f"Error en la consulta: {e}"}
    
    finally:
        # Asegurarse de cerrar la conexión
        conn.close()

