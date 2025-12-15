def get_connection():
    return pymysql.connect(
        host="localhost",
        user="adm_user",
        password="1228",
        database="ProyectoMDS2025"
    )