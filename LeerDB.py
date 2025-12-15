def read_last_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT temperature, humidity FROM weather ORDER BY id DESC LIMIT 1"
    )
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data