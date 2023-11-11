# config.py
API_KEY_HH = "API_KEY_HH"
PER_PAGE = 10

DB_PARAMS = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '12345',
    'dbname': 'cw5',
    'port': 5433
}


# from configparser import ConfigParser
#
# API_KEY_HH = "API_KEY_HH"
# PER_PAGE = 10
#
#
# def config(filename="database.ini", section="postgresql"):
#     # create a parser
#     parser = ConfigParser()
#     # read config file
#     parser.read(filename)
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception(
#             'Section {0} is not found in the {1} file.'.format(section, filename))
#     return db
