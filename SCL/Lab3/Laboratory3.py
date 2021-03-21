from os import path, getcwd
import sys
import logging

# create the the log file path that works on all OS
file_path = path.join(getcwd(), 'lodData.txt')

# Create logger
LOG_FORMAT = '%(levelname)s %(asctime)s %(filename)s - %(message)s'
logging.basicConfig(filename=file_path, level=logging.DEBUG, format=LOG_FORMAT)
# root logger
logger = logging.getLogger()


# Task 3
def run():
    """ The main function that has all the application logic"""
    logger.info("START")
    list_entries = read_log()
    sucessful_read(list_entries)
    failed_reads(list_entries)
    html_entries(list_entries)
    print_html_entries(list_entries)


# Task 4
def read_log():
    """ Read the log info and return an array containing the information"""
    formated_log_data = list()
    log_data = sys.stdin.readlines()
    # log information
    logger.debug("The log file contains {} lines in total"
                 .format(len(log_data)))
    for line in log_data:
        line_parts = line.rstrip("\n").strip().split()
        # make sure that all the four parameters are there
        if (len(line_parts) == 4):
            (path, status_code, size, time) = line_parts     # unpacking
            new_status_code = int(status_code)
            new_size = int(size)
            new_time = int(time)
            formated_log_data.append((path.strip(), new_status_code,
                                      new_size, new_time))
    # log information
    logger.debug("The log file contains {} real log information "
                 .format(len(formated_log_data)))
    return formated_log_data


# Task 5
def sucessful_read(list_entries):
    """takes a list of entries and logs information succeed request"""
    sucess_logs = list()
    for line in list_entries:
        (path, status_code, size, time) = line   # unpack it
        if(status_code >= 200 and status_code < 300):
            sucess_logs.append(line)
    logger.info("The number of successful request is {}"
                .format(len(sucess_logs)))
    return sucess_logs


# Task 6
def failed_reads(list_entries):
    """takes a list of entries and logs information succeed request"""
    failed_logs_4 = list()
    failed_logs_5 = list()
    failed_logs = list()
    for entry in list_entries:
        (path, status_code, size, time) = entry   # unpack the entry
        if(status_code >= 400 and status_code < 500):
            failed_logs_4.append(entry)
        elif(status_code >= 500 and status_code < 600):
            failed_logs_5.append(entry)
    logger.info("The number of failed resourses failed with code 5xx is {}"
                .format(len(failed_logs_5)))
    logger.info("The number of failed resourses failed with code 4xx is {}"
                .format(len(failed_logs_4)))
    failed_logs.extend(failed_logs_4)
    failed_logs.extend(failed_logs_5)
    return failed_logs


# Task 7
def html_entries(list_entries):
    """takes a list of entries and return a list of successfull ones
    with html extension"""
    succeess_read = sucessful_read(list_entries)
    html_resources = list()
    for entry in succeess_read:
        (path, status_code, size, time) = entry   # unpack the entry
        if(path.endswith(".html") or path.endswith(".html/")):
            html_resources.append(entry)
    logger.info("The number of succeed html resources is {}"
                .format(len(html_resources)))
    return html_resources


# Task 8
def print_html_entries(list_entries):
    """list all the html resources that are successfully retrieved"""
    html_resources = html_entries(list_entries)
    if(len(html_resources) == 0):
        print("No entry matches the criteria")
    else:
        for index in range(len(html_resources)):
            (path, status_code, size, time) = html_resources[index]  # unpack
            print("{0} {1:4d} {2:4d} {3:4d}"
                  .format(path, status_code, size, time))


# Task 9
# all the can be run multiple times. but it will depends of the case we would
# like to use it because a function is a reusable peice of code.

# run : can be run mupltile times as long as a falid log file is provided

# the rest of nthe function can also be run multiple function but requires a
# valid input format in the form of list of tuples

# ensure that it works fine incase it it imported
if(__name__ == '__main__'):
    run()
