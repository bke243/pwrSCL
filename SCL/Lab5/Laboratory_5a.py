from os import path, getcwd
import shlex
import logging
import json
# i will use import werkzeug module to generate and hash a password
from werkzeug.security import check_password_hash, generate_password_hash

# create the the log file path that works on all OS
file_path = path.join(getcwd(), 'logData.txt')

# Create logger
LOG_FORMAT = '%(levelname)s %(asctime)s %(filename)s - %(message)s'
logging.basicConfig(filename=file_path, level=logging.DEBUG, format=LOG_FORMAT)
# root logger
logger = logging.getLogger()


def get_config_parameter(param_name):
    """ Allow be to get the an input from the user"""
    assert isinstance(param_name, str), 'the paramter is {}'.format(param_name)
    value = str()
    value = input('{} : '.format(param_name))
    return value


def create_json_config_file():
    """ The function has the purpose of creating
    a json configuration file"""
    logger.info("Creating JSON Configuration file")
    config_param = {'server_log_name':
                    'Enter valid server log file name',
                    'http_method': 'Enter a valid HTTP method',
                    'logging_level': 'Enter a logging level as a number only',
                    'line_number': 'Enter the number of lines to be displayed',
                    'password': 'Enter the password of at least 8 characters'}
    # getting paramters
    http_methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                    'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
    logging_levels = ['0', '10', '20', '30', '40', '50']
    server_log_name = str()
    http_method = str()
    logging_level = int()
    line_number = int()
    password = str()
    # processing server name
    while(True):
        server = get_config_parameter(config_param.get('server_log_name'))
        if(len(server.strip()) > 0):
            server_log_name = server
            break
        print('Invalid server name retry')
    while(True):
        method = get_config_parameter(config_param.get('http_method'))
        if(method.strip().upper() in http_methods):
            http_method = method.strip().upper()
            break
        print('Invalid http method retry')
    while(True):
        level = get_config_parameter(config_param.get('logging_level'))
        if(level.strip() in logging_levels):
            logging_level = level.strip()
            break
        print('Invalid logging level name retry')
    while(True):
        number = get_config_parameter(config_param.get('line_number'))
        if(number.strip().isdigit() and int(number.strip()) >= 0):
            line_number = number.strip()
            break
        print('Invalid line numbers retry')
    while(True):
        psswd = get_config_parameter(config_param.get('password'))
        if(len(psswd.strip()) >= 8):
            password = psswd.strip()
            break
        print('Invalid password lenght should be >= 8 retry')
    # saving information
    hashed_password = generate_password_hash(password)
    config_information = {
        'server_name': server_log_name,
        'http_method': http_method,
        'logging_level': logging_level,
        'line_number': number,
        'password': hashed_password
    }
    try:
        with open('config_file.json', 'w', encoding='utf-8') as out_file:
            json.dump(config_information, out_file)
    # normally could not occur because if file does not exist python created it
    except OSError:
        logger.info("Could not write and/or open the file config_file.json ")
        print('Sorry, the operation could not be done')
        exit()


# app enty point
if __name__ == '__main__':
    logger.info("App Started")
    create_json_config_file()
# THE FISRT APPLICATION ENDS HERE
