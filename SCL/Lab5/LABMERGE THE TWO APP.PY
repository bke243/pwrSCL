from os import path, getcwd
import shlex
import logging
import json
from json.decoder import JSONDecodeError

# ========== STAR APP 1
print("STARTING APP 1")

def get_config_parameter(param_name):
    """ Allow be to get the an input from the user"""
    assert isinstance(param_name, str), 'the paramter is {}'.format(param_name)
    value = str()
    value = input('{} : '.format(param_name))
    return value


def create_json_config_file():
    """ The function has the purpose of creating
    a json configuration file"""
    config_param = {'server_log_name':
                    'Enter valid server log file name',
                    'http_method': 'Enter a valid HTTP method',
                    'logging_level': 'Enter a logging level as a number only',
                    'line_number': 'Enter the number of lines to be displayed',
                    'mine': 'Enter the personal parameter of at least 1 characters'}
    http_methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                    'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
    logging_levels = ['0', '10', '20', '30', '40', '50']
    server_log_name = str()
    http_method = str()
    logging_level = int()
    line_number = int()
    mine = str()
    
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
        parms = get_config_parameter(config_param.get('mine'))
        if(len(parms.strip()) >0):
            password = parms.strip()
            break
        print('Invalid password lenght should be >= 8 retry')
    
    config_information = {
        'server_name': server_log_name,
        'http_method': http_method,
        'logging_level': logging_level,
        'line_number': number,
        'password': mine
    }
    try:
        with open('config_file.json', 'w', encoding='utf-8') as out_file:
            json.dump(config_information, out_file)
    # normally could not occur because if file does not exist python created it
    except OSError:
        print('Sorry, the operation could not be done')

create_json_config_file()

print("\nENDING APP 1")

# =========== End APP 1

# =========== STAR APP2

file_path = path.join(getcwd(), 'log.txt')

# global variables
SERVER_LOG_NAME = str()
HTTP_METHOD = str()
LOGGING_LEVEL = int()
LINE_NUMBER = int()
PASSWORD = str()

# Task 2
def read_json():
    """ Read the kson config file and proccess it"""
    file_name = 'config_file.json'
    data = {}
    try:
        with open(file_name, encoding='utf-8') as in_file:
            data = json.load(in_file)
    # handle OS errors 
    except OSError as exception:
        print('Could not read the file {} because it does not exists '
              .format(file_name))
    # handle bad format
    except JSONDecodeError as e:
        print('The json file format is not good')
    # get the logging level
    try:
        log_level = int(data.get('logging_level'))
        line_num = int(data.get('line_number'))
    except ValueError:
        print('The logging level is not correct'
              .format(data.get('logging_level')))
    else:
        data['logging_level'] = log_level
        data['line_number'] = line_num
        return data

file_config_data = read_json()
SERVER_LOG_NAME = file_config_data.get('server_name')
HTTP_METHOD = file_config_data.get('http_method')
LOGGING_LEVEL = file_config_data.get('logging_level')
LINE_NUMBER = file_config_data.get('line_number')
PASSWORD = file_config_data.get('password')

# Task 3 logger
LOG_FORMAT = '%(levelname)s %(asctime)s %(filename)s - %(message)s'
logging.basicConfig(filename=file_path, level=LOGGING_LEVEL, format=LOG_FORMAT)
# root logger
logger = logging.getLogger()


# this is my main function which 
def run():
    """ The main function """
    logger.info("START")
    log_data = read_log()
    print_index(log_data)
    print_method(log_data)


# Task 4
def read_log():
    
    dict_file_content = dict()
    file_content = None
    ip_ctn = 0
    # reading the file in a safe way
    try:
        with open(SERVER_LOG_NAME) as infile:
            file_content = infile.readlines()
    except OSError:
        logger.info("The file does not exists")
        print('File does not exists exiting')
        exit()
    # processing file content for spliting and retreiving the IP address
    for line in file_content:
        line_content = line.split(" - - ")
        # i assume that they all be of legth 2 and ip is a string
        ip_addr = line_content[0]
        req_info = read_Log_helper(line_content[1])
        if ip_addr in dict_file_content:
            dict_file_content[ip_addr].append(req_info)
        else:
            dict_file_content[ip_addr] = [req_info]
            ip_ctn += 1
    logger.info(f"The file contains {ip_ctn} different ip keys")
    return dict_file_content


def read_Log_helper(req_details):

    assert isinstance(req_details, str), 'the paramter is {}'.format(req_details)
    # retrieve the date 1 means split only the first occurence
    req_detail = req_details.split("]", 1)
    # remove the [ leating
    req_date = req_detail[0].lstrip("[")
    # get the rest on the information from the line
    req_info = shlex.split(req_detail[1])
    (req_resource, req_status, req_size, req_other_ip, req_browser) = tuple(
     req_info)
    if(req_status.strip().isnumeric()):
        req_status = int(req_status)
    else:
        req_status = 0
    if(req_size.strip().isnumeric()):
        req_size = int(req_size)
    else:
        req_size = 0

    return (req_date, req_resource, req_status, req_size, req_other_ip,
            req_browser)


# Task 4
def print_index(log_data):
 
    assert isinstance(log_data, dict), 'the paramter is {}'.format(log_data)
    requests_list = []
    # check the condition and store the data
    for ip in log_data:
        for request_resource in log_data.get(ip):
            req_resource = request_resource[1]
            key_word = 'index.html'
            if(key_word in req_resource):
                requests_list.append(req_resource)
            # note that the method request here is coming from the JSON config
    #pring the result
    if(len(requests_list) == 0):
        print('There is not such resource(s)')
    for index in range(len(requests_list)):
        print(requests_list[index])


# Task 5
def print_method(log_data):
    assert isinstance(log_data, dict), 'the paramter is {}'.format(log_data)
    requests_list = []
    # check the condition and store the data
    if(LINE_NUMBER == 0):
        return
    for ip in log_data:
        for request_resource in log_data.get(ip):
            req_resource = request_resource[1]
            # note that the method request here is coming from the JSON config
            if(req_resource.startswith(HTTP_METHOD)):
                requests_list.append(req_resource)
    # pring the result this not good 
    # because i could print it while processing it 
    # just doing what was asked
    if(len(requests_list) == 0):
        print('There is not such resource(s)')
    for index in range(len(requests_list) ):
        print(requests_list[index])
        if(( index + 1) % LINE_NUMBER == 0):
            should_continue = input('Enter q or quit to stop and other to continue : ')
            if(should_continue.strip().lower() in ['q', 'quit']):
                break
            print('\n')


# Task 6 missing

# app entry point
if __name__ == '__main__':
    run()