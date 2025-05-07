import json
import psycopg2
import time
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException

# Kafka setup
consumer = Consumer({
    'bootstrap.servers': 'broker:9092',
    'group.id': 'order-consumer-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['inventory_ack'])

producer = Producer({'bootstrap.servers': 'broker:9092'})

# DB connection
def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                host="order_db",
                dbname="s2",
                user="s2",
                password="s2"
            )
            print("✅ Connected to Postgres (Order DB)")
            return conn
        except psycopg2.OperationalError:
            print("⏳ Waiting for PostgreSQL...")
            time.sleep(5)

conn = wait_for_postgres()
cursor = conn.cursor()

def main():
    print("🟢 Order Consumer is running...")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                print("⚠️ Kafka error:", msg.error())
                if msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    print("⏳ Topic not found. Retrying...")
                    time.sleep(5)
                    continue
                raise KafkaException(msg.error())

            data = json.loads(msg.value().decode('utf-8'))
            print("📥 Received Inventory Ack:", data)

            order_id = data.get("order_id")
            status = data["status"]

            if order_id is None:
                print("⚠️ No order_id provided. Skipping...")
                continue

            # Check if order exists
            cursor.execute("SELECT * FROM oltp.orders WHERE order_id = %s", (order_id,))
            order = cursor.fetchone()

            if order:
                # ✅ Update order status
                cursor.execute("""
                    UPDATE oltp.orders
                    SET status = %s
                    WHERE order_id = %s
                """, (status, order_id))
                conn.commit()
                print(f"✅ Updated order {order_id} to status '{status}'")
            else:
                # ❌ Order not found – send restore message
                restore_message = {
                    "product_id": data["product_id"],
                    "quantity": data["quantity"],
                    "location_x": data["location_x"],
                    "location_y": data["location_y"],
                    "action": "restore"
                }

                producer.produce("topic", json.dumps(restore_message).encode('utf-8'))
                producer.flush()
                print(f"📤 Sent restore message for unknown order_id {order_id}")

    except KeyboardInterrupt:
        print("🛑 Order consumer stopped.")
    finally:
        consumer.close()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
