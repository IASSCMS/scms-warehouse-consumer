from confluent_kafka.admin import (AdminClient, NewTopic)

def create_topic(topic):
    admin = AdminClient({'bootstrap.servers': 'localhost:29092'})
    new_topic = NewTopic(topic, num_partitions=1, replication_factor=1)
    result_dict = admin.create_topics([new_topic])
    for topic, future in result_dict.items():
        try:
            future.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))

