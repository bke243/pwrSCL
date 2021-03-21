from os import path, getcwd
import shlex
import logging

# create the the log file path that works on all OS
file_path = path.join(getcwd(), 'logData.txt')

# Create logger
LOG_FORMAT = '%(levelname)s %(asctime)s %(filename)s - %(message)s'
logging.basicConfig(filename=file_path, level=logging.DEBUG, format=LOG_FORMAT)
# root logger
logger = logging.getLogger()


# Task 3
def run():
    """ The main function that has all the application logic"""
    logger.info("START")
    log_data = read_log()
    num_req_ip = ip_requests(log_data)
    most_exp = ip_find(log_data, True)
    least_exp = ip_find(log_data, False)
    non_existent_path = non_existent(log_data)
    print(num_req_ip)
    print(most_exp)
    print(least_exp)
    print(longest_request(log_data))
    print(non_existent_path)


# Task 4
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
    except FileNotFoundError:
        logger.info("The file does not exists")
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


# Task 5
def ip_requests(log_data_entries):
    """ Takes a dictionary of log entries and returns a dictionary of number
    of requests for each Ip"""
    ip_requested = {}
    # loop over ip addresses
    for ip in log_data_entries:
        ip_requested[ip] = len(log_data_entries.get(ip))
    # get the object view values and sum them
    numbers_request = sum(list(ip_requested.values()))
    logger.info("The data has {} diffrents ip address requests".
                format(numbers_request))
    return ip_requested


# Task 6
def ip_find(log_data_entries, most_active):
    """ Taskes a dictionary and a parameter returns most or least active ip"""
    ip_requests_dict = ip_requests(log_data_entries)
    # object view method
    number_requests = list(ip_requests_dict.values())

    request_find = dict()
    req_n = 0
    if(most_active):
        req_n = max(number_requests)
    else:
        req_n = min(number_requests)
    for ip, ip_req_number in ip_requests_dict.items():
        if ip_req_number == req_n:
            request_find[ip] = ip_req_number
    return request_find


# Task 7
def longest_request(log_data_entries):
    """Returns the longest data entry line from the list
    of longest one with random choice"""
    longest_req = str()
    longest_list = list()
    for key in log_data_entries:
        # get the longest line per Ip adress key
        x = max(log_data_entries[key], key=lambda
                my_tuple: my_tuple[3])[:]
        # unpack the tuple
        (req_date, req_resource, req_status, req_size, req_other_ip,
         req_browser) = x
        line = (key, req_resource, req_size)
        longest_list.append(line)
    longest_request_size = max(longest_list, key=lambda my_tuple: my_tuple[2])
    logger.info("The longest request is {} {} {}".format(
                longest_request_size[0], longest_request_size[1],
                longest_request_size[2]))
    return " ".join((longest_request_size[0], longest_request_size[1],
                     str(longest_request_size[2])))


def stringy_req(request):
    """get a request tuples and return its string version"""
    (req_date, req_resource, req_status, req_size, req_other_ip,
     req_browser) = request
    if req_status == 0:
        req_status = "-"
    else:
        req_status = str(req_status)
    if req_size == 0:
        req_size = "-"
    else:
        req_size = str(req_size)
    line = " ".join((req_date, req_resource, req_status,
                     req_size, req_other_ip, req_browser))
    return line


# Task 8
def non_existent(log_data_entries):
    """ Takes the log data from the as parameter and returns a list of
    page not found resources"""
    page_not_found = list()
    request_entry = set()
    for key in log_data_entries:
        for req in log_data_entries[key]:
            (req_date, req_resource, req_status, req_size, req_other_ip,
             req_browser) = req
            if req_status == 404 and req_resource not in request_entry:
                request_entry.add(req_resource)
                line = " ".join((req_resource, str(req_status)))
                page_not_found.append(line)
    logger.info("There is {} different reuqest with status not found".
                format(len(page_not_found)))
    return page_not_found


# ensure that it works fine incase it it imported
if(__name__ == '__main__'):
    run()
# https://docs.python.org/3/library/shlex.html
