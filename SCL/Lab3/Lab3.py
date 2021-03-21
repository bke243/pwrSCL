from os import path, getcwd
import sys
import logging

# create the the log file path that works on all OS
file_path = path.join(getcwd(), 'logdata.txt')

# Create logger
LOG_FORMAT = '%(levelname)s %(asctime)s %(filename)s - %(message)s'
logging.basicConfig(filename=file_path, level=logging.DEBUG, format=LOG_FORMAT)
# root logger
logger = logging.getLogger()


def html_entries(list_entries):
    """takes a list of entries and return a list of successfull ones
    with html extension"""
    sucees_read = successful_reads(list_entries)
    html_resources = list()
    for line in list_entries:
        list_line = line.split()
        if(list_entries[0].endswith(".html")):
            html_resources.append(line)
    return sucees_read


def print_html_entries(list_entries):
    """list all the html resources that are successfully retrieved"""
    html_resources = html_entries(list_entries)
    print(html_resources)
    if(len(html_resources) == 0):
        logger.debug("No html resources success fully retrieved")
    else:
        for line in html_resources:
            print(line)


# I assumed data are of type : ["line enttry 1 ", "line enttry 2 "]
def successful_reads(list_entries):
    """takes a list of entries and logs information succeed request"""
    sucess_logs = list()
    for index in range(len(list_entries)):
        line = list_entries[index]
        list_line = line.rstrip("\n").strip().split()
        if(len(list_line) == 4):
            status_code = list_line[1]
            if(status_code.startswith('2') and len(status_code) == 3):
                sucess_logs.append(line.rstrip("\n").strip())
    logger.info("The number of successful request is {}"
                .format(len(sucess_logs)))
    return sucess_logs


def failed_reads(list_entries):
    """ takes a list of entries and logs information of failed request"""
    failed_logs_4 = list()
    failed_logs_5 = list()
    for line in list_entries:
        list_line = line.rstrip("\n").strip().split()
        if(len(list_line) == 4):
            status_code = list_line[1]
            if(status_code.startswith('4') and len(status_code) == 3):
                failed_logs_4.append(line.rstrip("\n").strip())
            elif(status_code.startswith('5') and len(status_code) == 3):
                failed_logs_5.append(line.rstrip("\n").strip())
    logger.info("The number of failed resourse with code starting with 5 is {}"
                .format(len(failed_logs_5)))
    logger.info("The number of failed resourse with code starting with 4 is {}"
                .format(len(failed_logs_4)))
    newList = failed_logs_4 + failed_logs_5
    return newList


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
            (path, status_code, size, time) = line_parts
            new_status_code = int(status_code)
            new_size = int(size)
            new_time = int(time)
            formated_log_data.append((path.strip(), new_status_code,
                                      new_size, new_time))
    # log information
    logger.debug("The log file contains {} real log information "
                 .format(len(formated_log_data)))
    return formated_log_data


def run():
    """ The main function that has all the application logic"""
    logger.info("START")
    data = read_log()
    print(data)


# ensure that it works fine incase it it imported
if(__name__ == '__main__'):
    run()
    x = sys.stdin.readlines()
    print(failed_reads(x))
    print(successful_reads(x))
    print(html_entries(x))
    print_html_entries(x)
