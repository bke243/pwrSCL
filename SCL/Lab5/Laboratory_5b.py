# THE SECOND APPLICATION START HERE
from os import path, getcwd
import shlex
import logging
import json
# to check the password
from werkzeug.security import check_password_hash
from json.decoder import JSONDecodeError
# create the the log file path that works on all OS
file_path = path.join(getcwd(), 'logData.txt')

# reading the json file to get logging level and usre it
SERVER_LOG_NAME = str()
HTTP_METHOD = str()
LOGGING_LEVEL = int()
LINE_NUMBER = int()
PASSWORD = str()


# Task 0
def read_json():
    """ Read the kson config file and proccess it"""
    file_name = 'config_file.json'
    data = {}
    try:
        with open(file_name, encoding='utf-8') as in_file:
            data = json.load(in_file)
    # handle OS errors : file not found ...
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

# Task 3 Create logger
LOG_FORMAT = '%(levelname)s %(asctime)s %(filename)s - %(message)s'
logging.basicConfig(filename=file_path, level=LOGGING_LEVEL, format=LOG_FORMAT)
# root logger
logger = logging.getLogger()


# this is my function which
def run():
    """ The main function that has all the application logic"""
    logger.info("START")
    log_data = read_log()
    print_index(log_data)
    print_method(log_data)


def read_log():
    """ Reads the log file content and return its content as a
    dictionary where keys are IP addreess and the rest are list of tuples"""
    dict_file_content = dict()
    file_content = None
    ip_ctn = 0
    # reading the file in a safe way
    try:
        with open("access_log.txt") as infile:
            file_content = infile.readlines()
    except OSError:
        logger.info("The file does not exists")
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
    """ Takes a request details and return a tuple with the right format
    of its information"""
    assert isinstance(req_details, str), """the paramter is {}
                                         """.format(req_details)
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
    """ the function takes a dictionary of request and print
    those index.hml inside"""
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
    # pring the result
    if(len(requests_list) == 0):
        print('There is not such resource(s)')
    for index in range(len(requests_list)):
        print(requests_list[index])


# Task 5
def print_method(log_data):
    """Takes a dict of data and print all with the
    same method as in the config file"""
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
    for index in range(len(requests_list)):
        print(requests_list[index])
        if((index + 1) % LINE_NUMBER == 0):
            should_continue = input("Enter q or quit to stop and other "
                                    "to continue : ")
            if(should_continue.strip().lower() in ['q', 'quit']):
                break
            print('\n')


# Task 6
def login_user():
    """Ask the user to enter the password stored in the config file and
    process it according to the previously asked tasks"""
    # get thyew user his password
    user_password = input("Enter your password defined when"
                          "creating the config file : ")
    # check it the hashed password mathces with the hoter one
    ispassword = check_password_hash(PASSWORD, user_password)
    if(ispassword):
        run()
    else:
        print('You have not the right to use the json configuration file')


# ensure that it works fine incase it it imported
if(__name__ == '__main__'):
    login_user()
# https://docs.python.org/3/library/shlex.html
