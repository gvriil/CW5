from configparser import ConfigParser

def config(filename="database.ini", section="postgresql"):
    """
    Получение параметров подключения к базе данных из конфигурационного файла.

    :param filename: Имя конфигурационного файла (по умолчанию "database.ini").
    :param section: Секция с параметрами подключения (по умолчанию "postgresql").
    :return: Словарь с параметрами подключения к базе данных.
    :raises Exception: Если секция не найдена в файле конфигурации.
    """
    # создаем парсер
    parser = ConfigParser()
    # читаем конфигурационный файл
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Секция {0} не найдена в файле {1}.'.format(section, filename))
    return db
