# -*- coding: UTF-8 -*-
from os import path, getcwd
import re
import logging
import sys
import datetime


# use regular expression to pparse log lines
def read_parse_log():
    """Reads the log file, and return a list of lines"""
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

    def parse_logs_data(log_lines):
        """Take a list of log  return those matching the pattern"""
        pattern = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) - - '
                             r'\[(\w.*)\] \"(\w.*)\" (\d+|-) (\d+|-) '
                             r'\"(\w.*|\W.*)\" \"(\w.*|\W.*)\"')
        # list of tuples
        parsed_list = list()
        for line in log_lines:
            parsed_line = pattern.search(line)
            if(parsed_line is None):
                continue
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
                parsed_list.append((ip, time_stamp, http_request, status_code,
                                    resources_size, ip_origin, browser))
        return parsed_list
    parsed_log_data = parse_logs_data(file_content)
    return parsed_log_data


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
        return None
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
            print('the time stamp {] is not the correct format'
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
    def __init__(self, ipaddress, time, http_request, status_code,
                 resource_size, ipaddress_2, browser):
        # all filed will be encapsulate and lock to prevent outside
        # modificatgion which does not make sense when manipulating
        #  log acvcording to business logic
        self.__ipaddress = ipaddress
        # using hour time generator function
        self.__time = generate_timestamp(time)
        self.__http_request = http_request
        self.__status_code = status_code
        self.__resource_size = resource_size
        self.__ipaddress_2 = ipaddress_2
        self.__browser = browser

    # overloaded Operator
    def __str__(self):
        """informal string representation"""
        string = """Http : from : {} at : {} requested : {}
        response status : {} data_size : {} ip_2 : {} from browser : {}"""
        return string.format(self.__ipaddress, self.__time,
                             self.__http_request,
                             self.__status_code, self.__resource_size,
                             self.__ipaddress_2, self.__browser)

    def __repr__(self):
        """Canonical String representation"""
        string = '{} {} {} {} {} {} {}'
        return string.format(self.__ipaddress, self.__time,
                             self.__http_request,
                             self.__status_code, self.__resource_size,
                             self.__ipaddress_2, self.__browser)

    def string(self):
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
    def __init__(self, filename):
        self.filename = filename
        # should be use http reqest
        self.http_resuqests = []

    def __str__(self):
        string = "file name . {}".format()
        # convert all http to strings a long string
        reuqests = "\n".join(item.__str__() for item in self.http_resuqests)
        return string + reuqests

    def string(self):
        """string representation """
        return self.__str__()


def generate_http(paresed_log):
    """Generatr http from parsed log data"""
    http_objects = []
    for req in paresed_log:
        ip = req[0]
        time_stamp = req[1]
        http_request = req[2]
        status_code = req[3]
        resources_size = req[4]
        ip_origin = req[5]
        browser = req[6]
        new_http = Http(ip, time_stamp, http_request, status_code,
                        resources_size, ip_origin, browser)
        http_objects.append(new_http)
    return http_objects


def main():
    """Main """
    parsed_file_content = read_parse_log()
    date = generate_timestamp('18/Oct/2020:01:30:42 +0200')
    print("I am {} and belongs to the class {}".format(date, type(date)))
    http_objects = generate_http(parsed_file_content)
    for obj in http_objects:
        print(obj.get_request_method(), obj.get_resource())


if __name__ == '__main__':
    main()
