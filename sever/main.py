import socket
import psycopg2

# Neon DB connection
conn_db = psycopg2.connect(
    "postgresql://neondb_owner:npg_rWgwpPyfn15X@ep-late-bird-ampt1of9-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)
cursor = conn_db.cursor()

HOST = "127.0.0.1"
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print("Server is running...")

def get_one_value(sql):
    cursor.execute(sql)
    result = cursor.fetchone()[0]

    if result is None:
        return None

    return float(result)


def run_query(user_query):
    user_query = user_query.lower()

    if "moisture" in user_query or "fridge" in user_query:
        result = get_one_value("""
            SELECT AVG(value::float)
            FROM sensor_data_virtual,
            LATERAL json_each_text(payload::json) AS j(key, value)
            WHERE key LIKE 'Moisture Meter%';
        """)

        if result is None:
            return "No moisture data found."

        return f"Average fridge moisture: {result:.2f}%"

    elif "water" in user_query or "dishwasher" in user_query:
        result = get_one_value("""
            SELECT AVG(value::float)
            FROM sensor_data_virtual,
            LATERAL json_each_text(payload::json) AS j(key, value)
            WHERE key LIKE 'Water Consumption Sensor%';
        """)

        if result is None:
            return "No water consumption data found."

        return f"Average dishwasher water consumption: {result:.2f}"

    elif "electricity" in user_query or "consumed" in user_query:
        cursor.execute("""
            SELECT
              CASE
                WHEN payload::json->>'topic' LIKE '%barry910801%' THEN 'House A'
                WHEN payload::json->>'topic' LIKE '%maskedshifter%' THEN 'House B'
                ELSE 'Unknown'
              END AS house,
              SUM(value::float) AS total
            FROM sensor_data_virtual,
            LATERAL json_each_text(payload::json) AS j(key, value)
            WHERE key LIKE 'Anmeter%'
            GROUP BY house;
        """)

        rows = cursor.fetchall()

        if len(rows) == 0:
            return "No electricity data found."

        if len(rows) == 1:
            return f"Only one house has electricity data so far: {rows[0][0]} = {rows[0][1]:.2f}"

        house1, value1 = rows[0]
        house2, value2 = rows[1]

        value1 = float(value1)
        value2 = float(value2)

        if value1 > value2:
            diff = value1 - value2
            return f"{house1} consumed more electricity than {house2} by {diff:.2f}. ({house1}: {value1:.2f}, {house2}: {value2:.2f})"
        else:
            diff = value2 - value1
            return f"{house2} consumed more electricity than {house1} by {diff:.2f}. ({house1}: {value1:.2f}, {house2}: {value2:.2f})"

    else:
        return "Sorry, this query cannot be processed. Please try one of the supported queries."


while True:
    conn, addr = server.accept()
    print(f"Connected by {addr}")

    data = conn.recv(4096)
    message = data.decode()
    print("Received:", message)

    response = run_query(message)

    conn.sendall(response.encode())
    conn.close()
