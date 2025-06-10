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

## ler isso aqui:
https://medium.com/creditas-tech/desvendando-o-kafka-parte-3-partitions-e-replication-23b36bb88c80

### 1. Preventing Data Loss and Enhancing Durability

https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html

**enable_idempotence (bool)** – When set to **True**, the producer will ensure that exactly one copy of each message is written in the stream. If False, producer retries due to broker failures, etc., may write duplicates of the retried message in the stream. Default: False.
Note that enabling idempotence requires **max_in_flight_requests_per_connection** to be set to 1 and **retries** cannot be zero. Additionally, **acks** must be set to ‘all’. If these values are left at their defaults, the producer will override the defaults to be suitable. If the values are set to something incompatible with the idempotent producer, a KafkaConfigurationError will be raised.


## Todo:

- Criar classes pros consumers e producers
- Colocar metodo de recuperar informacao no kafka
- colocar visualizacao do dado no redis
- checar formato do dado antes de salvar no consumer, formatar as string s dedata, esse tipo, conferir o tipo esse tipo de coisa
- testes

- criar arquitetura medalhao na parte 1
- silver mudando os formatos, filtrando por dt_Refe nao nulos, ese tipo de coisa
- gold fazendo o agrupamento
- terminar testes