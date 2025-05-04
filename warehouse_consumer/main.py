import json
import psycopg2
import time
import math
from confluent_kafka import Consumer, KafkaException

# 🕒 Wait for Postgres to be ready
def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                host="db",       # match Docker Compose service name
                dbname="scms",
                user="newone",
                password="password123"
            )
            print("✅ Connected to Postgres!")
            return conn
        except psycopg2.OperationalError:
            print("⏳ Waiting for PostgreSQL...")
            time.sleep(5)

# 🚀 Connect to PostgreSQL (after it's ready)
conn = wait_for_postgres()
cursor = conn.cursor()

# 📡 Kafka config
consumer = Consumer({
    'bootstrap.servers': 'broker:9092',
    'group.id': 'warehouse-consumer-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['topic'])

def find_nearest_warehouse(x, y):
    cursor.execute("SELECT warehouse_id, location_x, location_y FROM oltp.warehouse")
    warehouses = cursor.fetchall()

    min_dist = float('inf')
    nearest_id = None

    for warehouse in warehouses:
        wid, wx, wy = warehouse
        dist = math.sqrt((float(wx) - x)**2 + (float(wy) - y)**2)
        if dist < min_dist:
            min_dist = dist
            nearest_id = wid

    return nearest_id

def reduce_quantity(warehouse_id, product_id, qty):
    cursor.execute("""
        UPDATE oltp.warehouse_inventory
        SET quantity = quantity - %s
        WHERE warehouse_id = %s AND product_id = %s
    """, (qty, warehouse_id, product_id))
    conn.commit()

def main():
    print("🟢 Kafka Consumer is running...")
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:

                print("lolo")
                continue
            if msg.error():
                raise KafkaException(msg.error())

            data = json.loads(msg.value().decode('utf-8'))
            print("📥 Received:", data)

            location_x = data["location_x"]
            location_y = data["location_y"]
            product_id = data["product_id"]
            quantity = data["quantity"]

            nearest_warehouse_id = find_nearest_warehouse(location_x, location_y)
            print(f"🏬 Nearest warehouse: {nearest_warehouse_id}")

            reduce_quantity(nearest_warehouse_id, product_id, quantity)
            print(f"✅ Reduced {quantity} of product {product_id} at warehouse {nearest_warehouse_id}")

    except KeyboardInterrupt:
        print("🛑 Consumer stopped")
    finally:
        consumer.close()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
