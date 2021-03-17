import argparse
import json
import select
import sys
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import get_configs, get_message, send_message, read_requests, write_responses
from log.server_log import server_logger
from log.log_decor import Log

CONFIGS = get_configs()


# функция проверки сообщения клиента
@Log('DEBUG')
def check_message(message):
    if CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('USER') in message \
            and message[CONFIGS.get('USER')][CONFIGS.get("ACCOUNT_NAME")] == 'di-mario':
        server_logger.info('сообщение клиента успешно проверено. привет, клиент')
        return {
            CONFIGS.get('RESPONSE'): 200,
            CONFIGS.get('ALERT'): 'Привет, клиент!'
        }
    server_logger.error('сообщение от клиента некорректно')
    return {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad request'
    }

@Log('DEBUG')
# функция проверки сообщения клиента
def check_message_from_chat_client(message, messages_list, CONFIGS):
    if CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS.get('MESSAGE') \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('ACCOUNT_NAME') in message \
            and message[CONFIGS.get('ACCOUNT_NAME')] == 'di-mario':
        server_logger.info('сообщение клиента успешно проверено. привет, клиент')
        messages_list.append({
            CONFIGS.get('RESPONSE'): 200,
            CONFIGS.get('ALERT'): message[CONFIGS.get('MESSAGE_TEXT')]
        })
    else:
        server_logger.error('сообщение от клиента некорректно')
        messages_list.append({
            CONFIGS.get('RESPONSE'): 400,
            CONFIGS.get('ERROR'): 'Bad request'
        })

# параметры командной строки скрипта server.py -p <port>, -a <addr>:
parser = argparse.ArgumentParser(description='command line server parameters')
parser.add_argument('-a', '--addr', type=str, default='', help='ip address')
parser.add_argument('-p', '--port', type=int, default=CONFIGS.get('DEFAULT_PORT'), help='tcp-port')
args = parser.parse_args()
print(args)


def main():

    # проверка параметров вызова ip-адреса и порта из командной строки
    try:
        if '-a' or '--addr' in sys.argv:
            listen_address = args.addr
        else:
            listen_address = ''
    except IndexError:
        # print('После \'-a\' - необходимо указать адрес')
        server_logger.critical('После \'-a\' - необходимо указать адрес')
        sys.exit(1)

    try:
        if '-p' or '--port' in sys.argv:
            listen_port = args.port
        else:
            listen_port = CONFIGS.get('DEFAULT_PORT')
        if not 65535 >= listen_port >= 1024:
            raise ValueError
    except IndexError:
        # print('После -\'p\' необходимо указать порт')
        server_logger.critical('После -\'p\' необходимо указать порт')
        sys.exit(1)
    except ValueError:
        # print('Порт должен быть указан в пределах от 1024 до 65535')
        server_logger.critical('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    # сервер создаёт сокет
    sock = socket(AF_INET, SOCK_STREAM)
    # привязывает сокет к IP-адресу и порту машины
    sock.bind((listen_address, listen_port))
    # готов принимать соединения
    sock.listen(CONFIGS.get('MAX_CONNECTIONS'))
    # Таймаут для операций с сокетом
    sock.settimeout(0.5)

    clients = []
    messages = []

    while True:
        try:
            # принимает запрос на установку соединения
            client, addr = sock.accept()
        except OSError as e:
            pass  # timeout вышел
        else:
            server_logger.info(f'Установлено соединение с: {str(addr)}')
            clients.append(client)

        r_list = []
        w_list = []
        try:
            if clients:
                r_list, w_list, e_list = select.select(clients, clients, [], 2)
        except OSError:
            # Ничего не делать, если какой-то клиент отключился
            pass

        # проверяем "пишущих" клиентов
        if r_list:
            for client_with_message in r_list:
                # ловим от них сообщение и проверяем его на корректность, добавляем в список ответов (200 или 400)
                try:
                    check_message_from_chat_client(get_message(client_with_message, CONFIGS), messages, CONFIGS)
                except:
                    server_logger.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        # если есть сообщения в списке ответов после проверки (200 или 400) и есть слушающие клиенты
        if messages and w_list:

            # формируем ответное сообщение
            message = {
                CONFIGS.get('RESPONSE'): 200,
                CONFIGS.get('ALERT'): messages[0]['alert'],
            }
            # удаляем сообщение из списка ответов после проверки (200 или 400)
            del messages[0]

            # отправляем ждущим ответа клиентам сформированное сообщение
            for waiting_client in w_list:
                # print(f' waiting_client --- {waiting_client}\n')
                try:
                    send_message(waiting_client, message, CONFIGS)
                except:
                    server_logger.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)

if __name__ == '__main__':
    main()