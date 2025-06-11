# Monitoramento de Sensores IoT

## Problem description
Você precisa criar um sistema de monitoramento de sensores IoT que envia dados de sensores em tempo real para um tópico Kafka (producer) e consome esses dados para processamento e armazenamento (consumer).

1. **Criar o Producer**
    - Desenvolver um script em Python (ou outra linguagem de sua escolha) que gera dados falsos de sensores IoT e envia esses dados para um tópico Kafka.
    - Utilizar uma biblioteca como faker para gerar dados falsos.

2. **Criar o Consumer**
    - Desenvolver um script que consome os dados do tópico Kafka e processa esses dados.
    - Armazenar os dados consumidos em um banco de dados.

## 📁 Project Structure
```
.
├── docker-compose.yml
├── db/
│   └── init.sql
├── producer/
│   ├── Dockerfile.producer
│   └── producer_class.py
├── consumer/
│   ├── Dockerfile.consumer
│   ├── consumer_class.py
|   ├── run.py
|   └── clients/
|       ├── postgres_client_class.py
|       └── redis_client_class.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Getting Started
1. Clone the repository:
``` bash
git clone https://github.com/LuanFranco98/code-elevate-iot-kafka.git
cd code-elevate-iot-kafka
```
2. Start the project:
``` bash
docker-compose up --build
```

This will start:
- Kafka + Zookeeper
- Redis
- PostgreSQL (with schema initialization)
- Producer 
- Consumer 

## 📊 Data Flow
1. Producer (producer_class.py):
    - Generates fake sensor data using Faker
    - Sends it to Kafka topic iot-sensor-data

2. Consumer (consumer_class.py):
    - Consumes data from Kafka
    - Stores:
        - Latest readings in Redis
        - Full history in PostgreSQL


## 🧪 How to Check Data
**Redis (latest sensor values)**

```bash
docker exec -it redis redis-cli
> KEYS *
> GET sensor:<sensor_id>
```

**PostgreSQL (historical data)**
```bash
docker exec -it postgres psql -U iotuser iotdb 
iotdb=# SELECT * FROM sensor_data LIMIT 5;
```

## 🛠 Environment Variables
Defined inside docker-compose.yml for PostgreSQL, Redis and Kafka.


## 👤 Author
**Luan Silveira Franco**<br/>
*Data Engineer* 