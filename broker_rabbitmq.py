import pika
from config_reader import config

class Broker:

    def __init__(self) -> None:
        # Параметры подключения
        connection_params = pika.ConnectionParameters(
            host=config.rabbitmq_host,  # Замените на адрес вашего RabbitMQ сервера
            port=config.rabbitmq_port,          # Порт по умолчанию для RabbitMQ
            virtual_host='/',   # Виртуальный хост (обычно '/')
            credentials=pika.PlainCredentials(
                username=config.rabbitmq_username,  # Имя пользователя по умолчанию
                password=config.rabbitmq_password   # Пароль по умолчанию
            )
        )
        self.channel = None
        self.connection = None

        try:
            # Установка соединения
            self.connection = pika.BlockingConnection(connection_params)

            # Создание канала
            self.channel = self.connection.channel()
        except Exception as e:
            print(e)

    #Деструктор
    # def __del__(self):
    #     # Закрытие соединения
    #     self.connection.close()