import mysql.connector

def db_client():
    try:
        dbname = "Proyecto"
        user = "root"
        password = "pirineus"
        host = "192.168.22.1"
        port = "3306"
        collation="utf8mb4_general_ci"
        
        return mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname,
            collation=collation
        )
        
    except Exception as e:
        # Convertir el error a texto para evitar problemas de formato
        return {"status": -1, "message": f"Error de conexión: {str(e)}"}
