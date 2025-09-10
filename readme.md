# Bus Tracker

A real-time school bus tracking web application built with **Flask**, **Kafka**, and **Leaflet.js**. This project simulates bus locations and displays them on a live map with automatic updates every 2 seconds.

---

## Features

- Real-time bus location tracking on a map.
- Each bus is represented by a marker on the map (Leaflet's default marker).
- Click on a bus marker to view latitude, longitude, and last update timestamp.
- Select a bus from the dropdown to focus on it.
- Automatic updates every 2 seconds using Kafka as the message broker.
- Robust logging and error handling for both producer and consumer.

---

## Architecture

```
Producer (KafkaProducer)
       |
       v
Kafka Topic: bus_location
       |
       v
Consumer (KafkaConsumer)
       |
       v
Flask Backend (stores latest bus locations in memory)
       |
       v
Frontend (Leaflet.js map)
```

### Components

1. **Producer (`producer.py`)**
   - Simulates 10 buses with latitude and longitude coordinates in Mumbai.
   - Sends random location updates to Kafka every 2 seconds.
   - Uses `KafkaProducer` with retry and error handling.

2. **Consumer / Flask App (`app.py`)**
   - Consumes messages from the Kafka topic `bus_location`.
   - Stores the latest bus locations in a dictionary (`bus_data`).
   - Provides REST endpoint `/bus/<bus_no>` to fetch bus data.
   - Serves the `index.html` frontend with the list of buses.

3. **Frontend (`index.html`)**
   - Uses **Leaflet.js** to render a map of Mumbai.
   - Displays bus markers and updates their positions in real-time.
   - Dropdown menu to select and focus on a specific bus.

---

## Installation

### Requirements

- Python 3.8+
- Kafka (running locally or on a network)
- Flask
- kafka-python

### Install Python Dependencies

```bash
pip install flask kafka-python
```

### Start Kafka

Make sure Kafka broker is running at `KAFKA_BROKER_IP:PORT` (update the IP in `app.py` and `producer.py` if needed).  

---

## Usage

1. **Start the producer** (simulates bus movements):

```bash
python producer.py
```

2. **Start the Flask app** (serves frontend and consumes Kafka messages):

```bash
python app.py
```

3. **Open the app in a browser**:

```
http://127.0.0.1:5000/
```

4. Select a bus from the dropdown and focus on it. Markers update automatically.

---

## Project Structure

```
.
├── app.py          # Flask application & Kafka consumer
├── producer.py     # Kafka producer simulating bus movements
├── templates/
│   └── index.html  # Frontend with Leaflet.js map
├── README.md       # This file
```

---

## Logging

- Both producer and consumer use Python's `logging` module.
- Logs include info about messages sent/consumed and any errors.
- Helpful for debugging real-time updates.

---
