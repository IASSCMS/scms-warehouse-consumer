# SCMS Warehouse Consumer

A microservice for Smart Supply Chain Management System that consumes order data from Apache Kafka, processes it, and updates PostgreSQL inventory. The system is containerized using Docker Compose.

---

## Features

- Kafka consumer and producer using `confluent-kafka`
- PostgreSQL integration via `psycopg2`
- Logic to find the nearest warehouse and update inventory
- Dockerized infrastructure for Kafka, PostgreSQL, consumers, and pgAdmin

---

## Tech Stack

- Python 3.10+
- Apache Kafka
- PostgreSQL
- Docker & Docker Compose
- pgAdmin

---

## Project Structure

```
scms-warehouse-consumer/
├── docker-compose.yml
├── README.md
├── db-init/
│   └── inventory.sql
├── Kafka_config/
│   ├── init.py
│   └── main.py
├── order_consumer/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── order_producer/
│   └── main.py
├── order-init/
│   └── order.sql
├── warehouse_consumer/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/scms-warehouse-consumer.git
cd scms-warehouse-consumer
```

### 2. (Optional) Install Python Dependencies for Development

Create a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

Install dependencies:

```bash
pip install -r warehouse_consumer/requirements.txt
pip install -r order_consumer/requirements.txt
```

Or install directly:

```bash
pip install confluent-kafka psycopg2-binary
```

---

## Running with Docker

Build and start all services:

```bash
docker-compose up --build
```

---

## Kafka Topics

- `topic`: Main order topic for producer/consumer
- `inventory_ack`: Used for inventory acknowledgment

---

## Main Components

- **order_producer**: Publishes order messages to Kafka.
- **warehouse_consumer**: Consumes orders, finds nearest warehouse, updates inventory in PostgreSQL.
- **order_consumer**: Listens for inventory acknowledgments and updates order status.
- **Kafka_config**: Kafka topic creation and configuration scripts.

---

## License

MIT

---
