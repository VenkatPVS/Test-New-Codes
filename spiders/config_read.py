import configparser
settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('ibex.ctl')
# print settings.sections()
print settings.items()
server = settings.get('Volume','URL')
port = settings.get('Volume','E_METHOD')
enabled = settings.set('Volume','TYPE',"1")
enabled = settings.get('Volume','TYPE')
print server
print port
print enabled
