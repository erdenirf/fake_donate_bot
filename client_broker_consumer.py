from broker_rabbitmq import Broker
from config_reader import config

broker = Broker()

channel = broker.channel

# Функция, которая будет вызвана при получении сообщения
def callback(ch, method, properties, body):
    bodyMessage = body.decode('utf-8')
    print(f"Received: '{bodyMessage}'")

# Подписка на очередь и установка обработчика сообщений
channel.basic_consume(
    queue=config.rabbitmq_topicname,
    on_message_callback=callback,
    auto_ack=True  # Автоматическое подтверждение обработки сообщений
)

print('Waiting for messages. To exit, press Ctrl+C')
channel.start_consuming() 