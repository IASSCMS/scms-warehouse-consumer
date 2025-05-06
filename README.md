#  Supply Chain warehouse Kafka Consumer

This project is a microservice built in **Python** that consumes order data from **Apache Kafka**, processes it, and updates **PostgreSQL** accordingly. It is part of a larger Smart Supply Chain Management System and is fully containerized using **Docker Compose**.

---

## 📌 Features

- 🔁 Kafka consumer using `confluent-kafka`
- 🗃️ PostgreSQL integration via `psycopg2`
- 🧠 Logic to find the nearest warehouse and update inventory
- 📦 Dockerized infrastructure for Kafka , PostgreSQL,consumer and pgAdmin

---

## 🧰 Tech Stack

- Python 3.10+
- Kafka 
- PostgreSQL
- pgAdmin
- Docker & Docker Compose

---

## 📂 Project Structure

```bash
SCMS_Warehouse/
├── .env                # Environment variables
├── docker-compose.yml              # Container orchestration
├── init.sql                  # PostgreSQL table setup
├── Kafka_config/              # Kafka topic and config scripts
├── order_producer/             # Kafka order producer
├── warehouse_consumer/             # Kafka warehouse consumer service
├── databse/                           # Database init scripts and config
└── .gitignore
---
```
## 🚀 Getting Started
### 1. Clone the Repository

```bash
git clone https://github.com/your-org/smart-supplychain-kafka-consumer.git
cd smart-supplychain-kafka-consumer
```

### 2. Install Python Dependencies (Optional for development )
#### (Use pycharm to avoid this configs)
Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
Install dependencies:
```
```bash
pip install -r requirements.txt
```
If not using requirements.txt, install directly:

```bash
pip install confluent-kafka psycopg2-binary
```
## 🐳 Running with Docker
1. Build and Start the System

```bash
docker-compose up --build
```
