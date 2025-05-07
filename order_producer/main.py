import json
import random
import string
from confluent_kafka import Producer

def get_producer():
    return Producer({
        'bootstrap.servers': 'localhost:29092',
    })

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Failed to deliver message: {msg.key()}: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def generate_random_order():
    # Generate random uppercase coordinates (e.g., "AB", "XY")
    def rand_coord():
        return ''.join(random.choices(string.ascii_uppercase, k=2))

    return {
        "order_id": 2,
        "location_x": 10,
        "location_y": 20,
        "product_id":101,
        "quantity": 200,
        "action": "reduce"
    }

def main():
    producer = get_producer()
    topic = "topic"

    order = generate_random_order()

    print(f"📦 Sending order: {order}")

    producer.produce(
        topic=topic,
        key=f"product-{order['product_id']}",
        value=json.dumps(order),
        callback=delivery_report
    )

    producer.poll(1)
    producer.flush()

if __name__ == "__main__":
    main()
