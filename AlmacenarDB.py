def save_to_db(temp, hum):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO weather (temperature, humidity) VALUES (%s, %s)",
        (temp, hum)
    )
    conn.commit()
    cursor.close()
    conn.close()