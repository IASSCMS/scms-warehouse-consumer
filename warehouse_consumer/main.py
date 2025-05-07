import json
import psycopg2
import time
import math
from confluent_kafka import Consumer, KafkaException, KafkaError
from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'broker:9092'})


# 🕒 Wait for Postgres to be ready
def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                host="db",       # match Docker Compose service name
                dbname="s1",
                user="s1",
                password="s1"
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
    # 🔍 Step 1: Check current stock
    cursor.execute("""
        SELECT quantity
        FROM oltp.warehouse_inventory
        WHERE warehouse_id = %s AND product_id = %s
    """, (warehouse_id, product_id))
    result = cursor.fetchone()

    if not result:
        return False  # product not found

    current_qty = result[0]

    if current_qty >= qty:
        # ✅ Step 2: Reduce quantity
        cursor.execute("""
            UPDATE oltp.warehouse_inventory
            SET quantity = quantity - %s
            WHERE warehouse_id = %s AND product_id = %s
        """, (qty, warehouse_id, product_id))
        conn.commit()
        return True  # success
    else:
        # ❌ Not enough stock
        return False

# def reduce_quantity(warehouse_id, product_id, qty,action):
#     if action == "reduce":
#         cursor.execute("""
#             UPDATE oltp.warehouse_inventory
#             SET quantity = quantity - %s
#             WHERE warehouse_id = %s AND product_id = %s
#         """, (qty, warehouse_id, product_id))
#
#
#     elif action == "restore":
#         cursor.execute("""
#             UPDATE oltp.warehouse_inventory
#             SET quantity = quantity + %s
#             WHERE warehouse_id = %s
#             AND product_id = %s
#         """, (qty, warehouse_id, product_id))
#     conn.commit()

def main():
    print("🟢 Kafka Consumer is running...")
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:

                print("lolo")
                continue
            if msg.error():
                print("⚠️ Kafka error:", msg.error())

                if msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    print("⏳ Topic not found. Waiting and retrying...")
                    time.sleep(5)
                    continue

                raise KafkaException(msg.error())

            data = json.loads(msg.value().decode('utf-8'))
            print("📥 Received:", data)
            order_id = data['order_id']
            location_x = data["location_x"]
            location_y = data["location_y"]
            product_id = data["product_id"]
            quantity = data["quantity"]
            action = data["action"]

            nearest_warehouse_id = find_nearest_warehouse(location_x, location_y)
            print(f"🏬 Nearest warehouse: {nearest_warehouse_id}")
            if action == "reduce":
                success = reduce_quantity(nearest_warehouse_id, product_id, quantity)

                status = "approved" if success else "failed"

                order_message = {
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "location_x": location_x,
                    "location_y": location_y,
                    "status": status
                    # Add "order_id" if available in incoming message
                }

                producer.produce("inventory_ack", json.dumps(order_message).encode('utf-8'))
                producer.flush()

                print(f"📤 Sent inventory confirmation to 'inventory_ack' with status: {status}")

            elif action == "restore":
                cursor.execute("""
                    UPDATE oltp.warehouse_inventory
                    SET quantity = quantity + %s
                    WHERE warehouse_id = %s
                    AND product_id = %s
                """, (quantity, nearest_warehouse_id, product_id))
            conn.commit()
            #
            # reduce_quantity(nearest_warehouse_id, product_id, quantity,action)
            # print(f"✅ Reduced {quantity} of product {product_id} at warehouse {nearest_warehouse_id}")

    except KeyboardInterrupt:
        print("🛑 Consumer stopped")
    finally:
        consumer.close()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
