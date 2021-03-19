"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""
from ipaddress import ip_address
from pprint import pprint
from task_1 import host_ping

def host_range_ping():
    addr_list = []
    while True:
        start_ip = input('Введите начальный ip-адрес, учтите последний октет не может быть более 254: ')
        try:
            checked_ip = ip_address(start_ip)
            break
        except ValueError:
            print('Вы ввели некорректный ip-адрес')

    while True:
        addr_quantity = input('Введите количество адресов для проверки: ')
        if not addr_quantity.isnumeric():
            print('Введите целое положительное число')
        else:
            if int(start_ip.split('.')[3]) + int(addr_quantity) > 254:
                print(f'Максимальное количество адресов не может быть более 254, сейчас осталось '
                      f'{254 - int(start_ip.split(".")[3])}')
            else:
                for i in range(0, int(addr_quantity)):
                    addr_list.append(checked_ip)
                    checked_ip += 1
                return host_ping(addr_list, 500, 1)

if __name__ == '__main__':
    pprint(host_range_ping())