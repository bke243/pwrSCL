# -*- coding: UTF-8 -*-
from os import path, getcwd
import shlex
import re
import logging
import sys


# Task 2
def read_config():
    """ Read the config file for fyther processing"""
    file_content = []
    config_info = {}
    logging_levels = {'NOTSET': 0, 'DEBUG': 10, 'INFO': 20, 'WARNING': 30,
                      'ERROR': 40, 'CRITICAL': 50}
    http_methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                    'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
    try:
        # read the file content
        with open('lab6.config', encoding='utf-8') as infile:
            # read the file content at once
            file_content = infile.read()
            # define patter for each case
            name_pattern = re.compile(r"(name\=)(\w.*)")
            level_pattern = re.compile(r"(debug\=)(\w.*)")
            lines_pattern = re.compile(r"(lines\=)(\d*)")
            separator_pattern = re.compile(r"(separator\=)(\W.*)")
            filter_pattern = re.compile(r"(filter\=)(\w.*)")
            # search for pattern
            name = name_pattern.search(file_content)
            level = level_pattern.search(file_content)
            lines = lines_pattern.search(file_content)
            separator = separator_pattern.search(file_content)
            filter_method = filter_pattern.search(file_content)
        # print(file_content)
    except OSError:
        print("The file does not exist or could not acquire necessary"
              "resources to open the file")
        sys.exit()
    finally:
        server_name = str()
        logging_level = str()
        num_lines = int()
        separator_char = str()
        method_filter = str()
        # check if name was found found
        if(name is None):
            server_name = "access_log-20201025"
        else:
            server_name = "_".join(str(name.group(2)).split())
        # check logging level
        if(level is None):
            logging_level = "INFO"
        else:
            if(str(level.group(2)).upper in logging_levels):
                logging_level = str(name.group(2)).upper
            else:
                logging_level = "INFO"
        # check lines
        if(lines is None):
            num_lines = 5
        else:
            if(str(lines.group(2)).isdigit):
                num_lines = int(lines.group(2))
            else:
                num_lines = 5
        # check separator
        if(separator is None):
            separator_char = '|'
        else:
            separator_char = separator.group(2)
        # check method
        if(filter_method is None):
            method_filter = 'GET'
        else:
            if(str(filter_method.group(2).upper) in http_methods):
                method_filter = str(filter_method.group(2)).upper
            else:
                method_filter = 'GET'
        # prepare the final content
        config_info['LogFile'] = server_name + '.txt'
        config_info['Config'] = logging_levels.get(logging_level)
        config_info['Display'] = {}
        config_info['Display']['lines'] = num_lines
        config_info['Display']['separator'] = separator_char
        config_info['Display']['filter'] = method_filter
        return config_info


configuration_map = read_config()
FILENAME = configuration_map.get('LogFile')
DISPLAY = configuration_map.get('Display')
LEVEL = configuration_map.get('Config')
# create the the log file path that works on all OS
file_path = path.join(getcwd(), 'logdData.txt')

# Create logger
LOG_FORMAT = '%(levelname)s %(asctime)s %(filename)s - %(message)s'
logging.basicConfig(filename=file_path, level=LEVEL, format=LOG_FORMAT)
# root logger
logger = logging.getLogger()
logger.info('The config informations are {}'.format(configuration_map))


# Task 3
def read_log():
    """Reads and returns the content of the log file"""
    file_content = None
    try:
        with open(FILENAME, encoding='utf-8') as infile:
            file_content = infile.readlines()
    except OSError:
        print("Could not open the file {} the require resources unvalaible or"
              "file does not exists".format(FILENAME))
        # leave the app
        sys.exit()
    else:
        return file_content


# Task 4
def parse_content(log_data):
    """ Takes a list of log data and return a
    list of tuples of the same log parsed"""
    parsed_content = list()
    for line in log_data:
        pattern = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) - -'
                             r' \[(\w.*)\] \"(\w.*)\" (\d+) (\d+)')
        find = pattern.search(line)
        if(find is None):
            continue
        else:
            ip = find.group(1)
            time_stamp = find.group(2)
            http_request = find.group(3)
            status_code = int(find.group(4))
            resources_size = int(find.group(5))
            parsed_content.append((ip, time_stamp, http_request, status_code,
                                   resources_size))
    return parsed_content


# Task 5
def print_19(log_data):
    """print request with (277227 % 16) + 8 = 11 + 8 = 19
    my ip is 192.168.01 and gives the subnetMask 255.255.224.0 = 19 ones"""
    subnet = '255.255.224.0'
    for index in range(len(log_data)):
        pattern = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) - -'
                             r' \[(\w.*)\] \"(\w.*)\" (\d+) (\d+)')
        find = pattern.search(log_data[index])
        if(find is None):
            continue
        else:
            ip = find.group(1)
            if(is_in_range(ip, subnet)):
                print("{} {} {} {} {} ".format(find.group(1), find.group(2),
                                               find.group(3), find.group(4),
                                               find.group(5)))
        if(((index + 1) % DISPLAY['lines']) == 0):
            print('\n')
            ask = input('press q or quit to stop and else to continue: ')
            if(ask.lower == 'q' or ask.lower == 'quit'):
                break


def is_in_range(ip, ip_subnet):
    """for a given ip checks if the ip is in the range"""
    ip_add = ip.split('.')
    subnet = ip_subnet.split('.')
    if(len(ip_add) != len(subnet)):
        return False
    for i, j in zip(ip_add, subnet):
        is_digit = (i.isdigit and j.isdigit)
        if(is_digit and int(i) < int(j)):
            continue
        else:
            return False
    return True


# Task 6
def print_filter(log_data):
    """The functions takes a list of log data and print the total
    bytes used for a givet ip method request"""
    bytes_sum = int(0)
    method_filter = DISPLAY['filter']
    lines = DISPLAY['lines']
    separator = DISPLAY['separator']
    for line in log_data:
        string = r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) - - \[(\w.*)\] \"%s\W.*\" (\d+) (\d+)' % (method_filter)
        patteren = re.compile(string)
        find = patteren.search(line)
        if(find is None):
            continue
        else:
            byte = int(find.group(4))
            bytes_sum += byte
    res = method_filter + separator + str(bytes_sum)
    return res


def main():
    """ The main function"""
    logger.info('Start')
    log_data = read_log()
    parsed_content = parse_content(log_data)
    filter_param = print_filter(log_data)
    print(filter_param)
    print_19(log_data)


if __name__ == '__main__':
    main()
