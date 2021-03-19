"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping
будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел
должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес
сетевого узла должен создаваться с помощью функции ip_address().
"""
from subprocess import Popen, PIPE
from ipaddress import ip_address
from pprint import pprint

def host_ping(addr_list, timeout, requests_quantity):
    all_addr_dict = {'Доступные узлы': '', 'Недоступные узлы': ''}
    for address in addr_list:
        try:
            ip_addr = ip_address(address)
        except ValueError:
            ip_addr = address

        reply_from_host = Popen(f'ping {ip_addr} -w {timeout} -n {requests_quantity}', shell=False, stdout=PIPE,
                                stderr=PIPE)
        completion_code = reply_from_host.wait()
        if completion_code == 0:
            print(f'Узел {address} доступен')
            all_addr_dict['Доступные узлы'] += f'{str(address)} \n'
        else:
            print(f'Узел {address} недоступен')
            all_addr_dict['Недоступные узлы'] += f'{str(address)} \n'
    return all_addr_dict

if __name__ == '__main__':
    addresses_list = ['192.168.1.1', '192.168.1.3', '192.168.1.4', '8.8.8.8', '127.0.0.1', 'localhost', 'www.yandex.ru']
    pprint(host_ping(addresses_list, 500, 1))
