import json
import logging
import threading
from flask import Flask, render_template, jsonify
from kafka import KafkaConsumer, errors as kafka_errors

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(threadName)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

bus_data = {}

def consume_data():
    try:
        consumer = KafkaConsumer(
            "bus_location",
            bootstrap_servers="10.0.61.208:9092",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="latest",
            enable_auto_commit=True,
            consumer_timeout_ms=10000
        )
        logger.info("Kafka consumer started, listening to 'bus_location' topic...")
    except kafka_errors.NoBrokersAvailable as e:
        logger.error(f"Kafka broker not available: {e}")
        return
    except Exception as e:
        logger.exception(f"Failed to create KafkaConsumer: {e}")
        return

    try:
        for msg in consumer:
            try:
                bus = msg.value.get("bus_no")
                if bus:
                    bus_data[bus] = msg.value
                    logger.info(f"Consumed bus data: {msg.value}")
                else:
                    logger.warning(f"Received message without 'bus_no': {msg.value}")
            except Exception as e:
                logger.exception(f"Error processing Kafka message: {e}")
    except Exception as e:
        logger.exception(f"Kafka consumer loop error: {e}")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed.")

threading.Thread(target=consume_data, daemon=True, name="KafkaConsumerThread").start()

@app.route("/")
def index():
    try:
        buses = list(bus_data.keys())
        return render_template("index.html", buses=buses)
    except Exception as e:
        logger.exception(f"Error rendering index: {e}")
        return "Internal Server Error", 500

@app.route("/bus/<bus_no>")
def get_bus(bus_no):
    try:
        data = bus_data.get(bus_no)
        if not data:
            logger.warning(f"No data found for bus {bus_no}")
            return jsonify({"error": "No data yet"}), 404
        return jsonify(data)
    except Exception as e:
        logger.exception(f"Error fetching bus data for {bus_no}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    try:
        logger.info("Starting Flask app...")
        app.run(debug=True)
    except Exception as e:
        logger.exception(f"Flask app failed to start: {e}")
