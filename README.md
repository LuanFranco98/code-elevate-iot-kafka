# code-elevate-iot-kafka
## Monitoramento de Sensores IoT

### Descrição do Problema
Você precisa criar um sistema de monitoramento de sensores IoT que envia dados de sensores em tempo real para um tópico Kafka (producer) e consome esses dados para processamento e armazenamento (consumer).

1. **Criar o Producer**
    - Desenvolver um script em Python (ou outra linguagem de sua escolha) que gera dados falsos de sensores IoT e envia esses dados para um tópico Kafka.
    - Utilizar uma biblioteca como faker para gerar dados falsos.

2. **Criar o Consumer**
    - Desenvolver um script que consome os dados do tópico Kafka e processa esses dados.
    - Armazenar os dados consumidos em um banco de dados.


## Docker: 
- Build:
    - $ docker compose up --build

- deletar containers
    - $ docker compose down 

- List runing:
    - $ docker ps -a

- Show logs:
    - $  docker logs -f " hash do CONTAINER ID

- fazer consulta no bd (postgres):
    - docker exec -it postgres psql -U iotuser iotdb 
         - listar databases: \dt
         - table schema: \d sensor_data
         - SELECT * FROM sensor_data LIMIT 5;


SELECT * FROM sensor_data where sensor_id='d6390e14-e96c-4201-9479-22d0d53aeedf';