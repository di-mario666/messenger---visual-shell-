import dis

# Метакласс для проверки соответствия сервера:
class ServerVerifier(type):
    def __init__(cls, cls_name, bases, cls_dict):
        # Список методов, которые используются в функциях класса:
        methods_list = []
        # Атрибуты, используемые в функциях классов
        attrs_list = []
        for func in cls_dict:
            # Пробуем
            try:
                return_iter = dis.get_instructions(cls_dict[func])
            except TypeError:
                pass
            else:
                for instruction in return_iter:
                    if instruction.opname == 'LOAD_GLOBAL':
                        if instruction.argval not in methods_list:
                            # заполняем список методами, использующимися в функциях класса
                            methods_list.append(instruction.argval)
                    elif instruction.opname == 'LOAD_ATTR':
                        if instruction.argval not in attrs_list:
                            # заполняем список атрибутами, использующимися в функциях класса
                            attrs_list.append(instruction.argval)
        print(f'список методов класса {cls_name} (информация от метакласса) {methods_list}')
        print(f'список атрибутов класса {cls_name} (информация от метакласса) {attrs_list}')
        # Если обнаружено использование недопустимого метода connect, бросаем исключение:
        if 'connect' in methods_list:
            raise TypeError('Использование метода connect недопустимо в серверном классе')
        # Если сокет не инициализировался константами SOCK_STREAM(TCP) AF_INET(IPv4), тоже исключение.
        if not ('SOCK_STREAM' in attrs_list and 'AF_INET' in attrs_list):
            raise TypeError('Некорректная инициализация сокета. Нужна инициализация по TCP')
        # Обязательно вызываем конструктор предка:
        super().__init__(cls_name, bases, cls_dict)

class ClientVerifier(type):
    def __init__(cls, cls_name, bases, cls_dict):
        # список для методов класса
        methods_list = []
        for func in cls_dict:
            try:
                return_iter = dis.get_instructions(cls_dict[func])
            except TypeError:
                pass
            else:
                for instruction in return_iter:
                    if instruction.opname == 'LOAD_GLOBAL':
                        if instruction.argval not in methods_list:
                            # заполняем список методами, использующимися в функциях класса
                            methods_list.append(instruction.argval)

        print(f'список методов класса {cls_name} (информация от метакласса) {methods_list}')
        for method in methods_list:
            if method == 'accept' or method == 'listen':
                raise TypeError('Использование метода accept, listen недопустимо в клиенте')

        super().__init__(cls_name, bases, cls_dict)