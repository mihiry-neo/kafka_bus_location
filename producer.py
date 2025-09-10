import time
import json
import random
import logging
from kafka import KafkaProducer, errors as kafka_errors

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(threadName)s - %(message)s"
)
logger = logging.getLogger(__name__)

try:
    producer = KafkaProducer(
        bootstrap_servers="10.0.61.208:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        retries=5
    )
    logger.info("Kafka producer created successfully.")
except kafka_errors.NoBrokersAvailable as e:
    logger.error(f"Kafka broker not available: {e}")
    exit(1)
except Exception as e:
    logger.exception(f"Failed to create Kafka producer: {e}")
    exit(1)

buses = [
    "BUS101", "BUS102", "BUS103", "BUS104", "BUS105",
    "BUS106", "BUS107", "BUS108", "BUS109", "BUS110"
]

locations = {
    "BUS101": [19.0760, 72.8777],
    "BUS102": [19.2183, 72.9781],
    "BUS103": [19.0436, 72.8633],
    "BUS104": [19.1333, 72.9350],
    "BUS105": [18.9647, 72.8258],
    "BUS106": [19.1071, 72.8364],
    "BUS107": [19.2307, 72.8567],
    "BUS108": [18.9894, 72.8365],
    "BUS109": [19.1551, 72.8490],
    "BUS110": [18.9388, 72.8354]
}

try:
    while True:
        for bus in buses:
            try:
                lat, lon = locations[bus]

                lat += random.uniform(-0.001, 0.001)
                lon += random.uniform(-0.001, 0.001)
                locations[bus] = [lat, lon]

                data = {"bus_no": bus, "latitude": lat, "longitude": lon}

                future = producer.send("bus_location", value=data)
                future.add_errback(lambda exc: logger.error(f"Send failed for {bus}: {exc}"))
                logger.info(f"Sent: {data}")

            except Exception as e:
                logger.exception(f"Error generating/sending message for {bus}: {e}")

        time.sleep(2)
except KeyboardInterrupt:
    logger.info("Producer stopped by user.")
except Exception as e:
    logger.exception(f"Unexpected error in producer loop: {e}")
finally:
    try:
        producer.close()
        logger.info("Kafka producer closed.")
    except Exception as e:
        logger.exception(f"Error closing Kafka producer: {e}")
