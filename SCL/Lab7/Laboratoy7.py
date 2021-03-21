# -*- coding: UTF-8 -*-
from os import path, getcwd
import re
import logging
import sys
import datetime
import ipaddress

# create the the log file path that works on all OS
file_path = path.join(getcwd(), 'logging.txt')
# Create logger
LOG_FORMAT = '%(levelname)s %(asctime)s %(filename)s - %(message)s'
logging.basicConfig(filename=file_path, level=logging.DEBUG, format=LOG_FORMAT)
# root logger
logger = logging.getLogger()
# task 1 done
# task 2 done
# task 3 done


# Task 4
def generate_timestamp(timestamp_string):
    """takes string of the datetime format and returns its object"""
    # date ranges: month 1 - 12, year 1 - 9999, day 1 - 31
    parrtern = re.compile(r'(\d\d)/(\w*)/(\d\d\d\d):(\d\d):(\d\d):(\d\d)')
    tmstp = parrtern.search(timestamp_string)
    months_dict = generate_month()
    if(tmstp is None):
        logger.info('The timestamp format is not good'
                    .format(timestamp_string))
        raise ValueError('Wrong date time stamp'.format(timestamp_string))
    else:
        new_date = None
        try:
            date_day = int(tmstp.group(1))
            # can be None remember
            date_month = months_dict.get(tmstp.group(2))
            date_year = int(tmstp.group(3))
            date_hour = int(tmstp.group(4))
            date_minutes = int(tmstp.group(5))
            date_secondes = int(tmstp.group(6))
            # creati9ng the date object
            new_date = datetime.datetime(date_year, date_month, date_day,
                                         date_hour, date_minutes,
                                         date_secondes)
        except ValueError:
            logger.info('The timestamp format is not good'
                        .format(timestamp_string))
            raise
        return new_date


def generate_month():
    """Return a dictionary of months and thier number"""
    months_choices = {}
    for index in range(1, 13):
        month = datetime.date(2008, index, 1).strftime('%b')
        months_choices[month] = index
    return months_choices


# Task 5
class Http:
    def __init__(self, http_request):
        self.__http_request = http_request

    # overloaded Operator
    def __str__(self):
        """informal string representation"""
        string = "http method : {} requested resource : {}"
        return string.format(self.get_request_method(), self.get_resource())

    def __repr__(self):
        """Canonical String representation"""
        return self.__str__()

    def to_string(self):
        """Return an bobjec in string representation"""
        return self.__str__()

    def get_request_method(self):
        """Return the request method of the current http object"""
        http_methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                        'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
        req_m = self.__http_request
        req_list = req_m.split(" ", 1)
        if(len(req_list) > 0 and req_list[0].upper() in http_methods):
            return req_list[0].upper()
        else:
            "-"
    def get_resource(self):
        """Returns the resources requested"""
        req_m = self.__http_request
        req_list = req_m.split(" ", 1)
        if(len(req_list) == 2):
            return req_list[1]
        else:
            "-"


# Task 6
class LogEntry:
    def __init__(self, ip, time_stamp, http_request, status_code,
                 resource_size, ipaddress_2, browser):
        # all filed will be encapsulate and lock to prevent outside
        # modificatgion which does not make sense when manipulating
        #  log acvcording to business logic
        self.__ip = ipaddress.IPv4Address(ip)
        # using hour time generator function
        self.__time_stamp = generate_timestamp(time_stamp)
        self.__http_request = Http(http_request)
        self.__status_code = status_code
        self.__resource_size = resource_size
        self.__ipaddress_2 = ipaddress_2
        self.__browser = browser

    def get_timestamp(self):
        """Return the time stamp attribute to be used in the task 10"""
        return self.__time_stamp

    # overloaded Operator
    def __str__(self):
        """informal string representation"""
        string = """Http : from : {} at : {} requested : {}
        response status : {} data_size : {} ip_2 : {} from browser : {}"""
        return string.format(self.__ip, self.__time_stamp,
                             self.__http_request,
                             self.__status_code, self.__resource_size,
                             self.__ipaddress_2, self.__browser)

    def __repr__(self):
        """Canonical String representation"""
        return self.__str__()

    def string(self):
        """Return an bobjec in string representation"""
        return self.__str__()


# Task 7
def create_log_entry(log_line):
    """Takes a log line and returns a log entry object"""
    pattern = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) - - '
                         r'\[(\w.*)\] \"(\w.*)\" (\d+|-) (\d+|-) '
                         r'\"(\w.*|\W.*)\" \"(\w.*|\W.*)\"')
    parsed_line = pattern.search(log_line)
    if(parsed_line is None):
        return None
    else:
        ip = parsed_line.group(1)
        time_stamp = parsed_line.group(2)
        http_request = parsed_line.group(3)
        status_code = 0
        # to avoid - for the line with no status code
        if(parsed_line.group(4).isdigit()):
            status_code = int(parsed_line.group(4))
        else:
            status_code = 0
        resources_size = 0
        # to avoid - for resources size in this case
        if(parsed_line.group(5).isdigit()):
            resources_size = int(parsed_line.group(5))
        else:
            resources_size = 0
        ip_origin = parsed_line.group(6)
        browser = parsed_line.group(7)
        new_log_entry = LogEntry(ip, time_stamp, http_request, status_code,
                                 resources_size, ip_origin, browser)
    return new_log_entry


# Task 8
# use regular expression to pparse log lines
def create_log_entries():
    """Reads the log file, and return a list of log entries"""
    file_name = "access_log-20201025.txt"
    file_content = None
    try:
        with open(file_name, encoding='utf-8') as infile:
            file_content = infile.readlines()
    except OSError:
        print("Could not open the file {} the require resources unvalaible or"
              "file does not exists".format(file_name))
        logger.info('The file {} does not exists'.format(file_name))
        # leave the app
        sys.exit()
    log_entries = []
    for log_line in file_content:
        log_obj = create_log_entry_modified(log_line)
        if(log_obj is not None):
            log_entries.append(log_obj)
    return log_entries


# Task 9
class MalformedHttp(Exception):
    """Raised when the http does not match correctly"""
    pass


# Task 9 a log entry creator
def create_log_entry_modified(log_line):
    """Takes a log line and returns a log entry object"""
    pattern = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) - - '
                         r'\[(\w.*)\] \"(\w.*)\" (\d+|-) (\d+|-) '
                         r'\"(\w.*|\W.*)\" \"(\w.*|\W.*)\"')
    parsed_line = pattern.search(log_line)
    new_log_entry = None
    try:
        ip = parsed_line.group(1)
        time_stamp = parsed_line.group(2)
        http_request = parsed_line.group(3)
        status_code = int(parsed_line.group(4)) 
        resources_size = int(parsed_line.group(5))
        ip_origin = parsed_line.group(6)
        browser = parsed_line.group(7)
        new_log_entry = LogEntry(ip, time_stamp, http_request, status_code,
                                 resources_size, ip_origin, browser)
    except ValueError:
        logger.info('ValueError value was raised')
        raise MalformedHttp(log_line)
    except AttributeError:
        logger.info('AttributeError value was raised')
        raise MalformedHttp(log_line)
    return new_log_entry


# Task 9 b
def create_log_entries_modified():
    """Reads the log file, and return a list of log entries"""
    file_name = "access_log-20201025.txt"
    file_content = None
    try:
        with open(file_name, encoding='utf-8') as infile:
            file_content = infile.readlines()
    except OSError:
        print("Could not open the file {} the require resources unvalaible or"
              "file does not exists".format(file_name))
        # leave the app
        sys.exit()
    log_entries = []
    count_malformed = 0
    for log_line in file_content:
        try:
            log_obj = create_log_entry_modified(log_line)
        except MalformedHttp:
            count_malformed += 1
        finally:
            if(log_obj is not None):
                log_entries.append(log_obj)
    logger.info('{} malformed http'.format(count_malformed))
    return log_entries


# Task 10
def display_between(tmstp_1, tmstp_2):
    """ Print lines between intervalls"""
    # since we are working on logfile
    # with the lack of eg from the question
    # i assume it will be passed as in task 4 timestamp format
    # 18/Oct/2020:01:30:42 +0200
    date_from = generate_timestamp(tmstp_1)
    date_to = generate_timestamp(tmstp_2)
    if(date_to <= date_from):
        print('The date is not a correct interval')
    else:
        log_entries = create_log_entries_modified()
        for log_entry in log_entries:
            if(log_entry.get_timestamp is not None):
                if(log_entry.get_timestamp() > date_from and
                   log_entry.get_timestamp() < date_to):
                    print(log_entry)


def main():
    """Main """
    logger.info('START APP')
    parsed_file_content = create_log_entries_modified()
    date = generate_timestamp('18/Oct/2020:01:30:42 +0200')
    print("I am {} and belongs to the class {}".format(date, type(date)))
    # http_objects = generate_http(parsed_file_content)
    for obj in parsed_file_content:
        print(obj)
    display_between('19/Oct/2020:09:59:11 +0200', '21/Oct/2020:21:58:58 +0200')


if __name__ == '__main__':
    main()
