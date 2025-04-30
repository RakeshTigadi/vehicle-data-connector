import random
import time
import uuid
import json
import os
from datetime import datetime
from confluent_kafka import Producer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "my-cluster-kafka-bootstrap.kafka.svc:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "payment-streams")
INTERVAL_SECONDS = float(os.getenv("INTERVAL_SECONDS", "3"))
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME", "by0bl57qw19qnewv91wg0wsig")
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD", "GyB6AGkXzDDQr66pv9FnCVyNVDAwpSYr")

producer_config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS
}

if KAFKA_USERNAME and KAFKA_PASSWORD:
    producer_config.update({
        "security.protocol": "SASL_PLAINTEXT",
        "sasl.mechanism": "SCRAM-SHA-512",
        "sasl.username": KAFKA_USERNAME,
        "sasl.password": KAFKA_PASSWORD,
    })

producer = Producer(producer_config)

sensor_types = ["POS_Terminal", "Mobile_App", "Wearable_Device", "Kiosk", "NFC_Tag"]
card_types = ["Visa", "MasterCard", "Amex", "Discover", "RuPay"]

def generate_transaction():
    return {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "sensor_type": random.choice(sensor_types),
        "card_type": random.choice(card_types),
        "amount_usd": round(random.uniform(3, 200), 2)
    }

def delivery_report(err, msg):
    if err:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Sent to {msg.topic()} [Partition {msg.partition()}]")

def stream_transactions():
    while True:
        txn = generate_transaction()
        txn_json = json.dumps(txn)
        producer.produce(KAFKA_TOPIC, key=txn["transaction_id"], value=txn_json, callback=delivery_report)
        producer.poll(0)
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    print(f"🚀 Streaming to topic '{KAFKA_TOPIC}' every {INTERVAL_SECONDS}s")
    try:
        stream_transactions()
    except KeyboardInterrupt:
        print("🛑 Stopped by user.")
    finally:
        producer.flush()
