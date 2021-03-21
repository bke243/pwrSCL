from os import path, getcwd
import sys
import logging

# create the the log file path that works on all OS
file_path = path.join(getcwd(), 'looging.txt')

# Create logger
LOG_FORMAT = '%(levelname)s %(asctime)s %(filename)s - %(message)s'
logging.basicConfig(filename=file_path, level=logging.DEBUG, format=LOG_FORMAT)

# root logger
logger = logging.getLogger()
logger.info("START")


def read_standard_input():
    """ this function reads from standard input and return the data red in an
    array"""
    std_data = list()
    for line in sys.stdin:
        # get ride of the \n characters here better
        std_data.append(line.split('\n')[0])
    return std_data


def process_standard(std_data=list()):
    """Get a list of user data asuming they are in a good format
    and process it"""
    processed_data = list()
    for line in std_data:
        try:
            (path, status_code, size, time) = line.split()
            # trying the explicit casting of integer
            new_status_code = int(status_code)
            new_size = int(size)
            new_time = int(time)
            processed_data.append([path, new_status_code, new_size, new_time])
        except ValueError as identifier:
            logger.error("""Error : {} the line : {} is not the appropriate
                         format""".format(identifier, line))

    return processed_data


def show_log_statistic(max_resource_path, max_resource_time,
                       total_failed_request, total_bytes_sent,
                       total_rousource_time,
                       total_request_sent):
        """Print a formatted message displaying the statical information of
        the log file"""
        logger.info('show_log_statistic({}, {}, {}, {}, {}, {})'.format(
                max_resource_path, max_resource_time, total_failed_request,
                total_bytes_sent, total_rousource_time, total_request_sent))

        mean_request = 0
        if(total_bytes_sent != 0):
            mean_request = total_rousource_time / total_request_sent
        # I will go with multiples print
        print('\n=====STATISITCS OF THE LOG FILE=====\n')
        print('the path: {} has the largest processing timewhich is: {}'.
              format(max_resource_path, max_resource_time))
        print('the total number of failed request is: {}'.
              format(total_failed_request))
        print('The total number of bytes sent is: {}'.format(total_bytes_sent))
        print('The total number of Kilobytes sent is: {}'.
              format(total_bytes_sent * 0.001))
        print('The mean processing time of a single request is: {}'.
              format(mean_request))
        print('\n=====END OF THE LOG FILE=====')
        # final logger
        logger.info("END")


def analize_log_data(log_data):
    """get a list of log data, process it and display its
    statiscial information"""
    # prevent the function to be used somehow with wrong parameters
    assert isinstance(log_data, list)

    max_resource_path = str()
    max_resource_time = 0
    cnt_failed_requests = 0
    total_bytes_sent = 0
    total_resource_time = 0
    total_number_request = 0
    total_failed_request = 0
    log_line = str()
    for log in log_data:
        (path, status_code, size, time) = log
        if(time > max_resource_time):
            max_resource_time = time
            max_resource_path = path
        if(status_code == 404):
            log_line = '!{} {} {}'
            total_failed_request += 1
        else:
            log_line = ' {} {} {}'
        total_bytes_sent += size
        total_resource_time += time
        total_number_request += 1
        # display the log infomrations
        print(log_line.format(path, status_code, size, time))
    # finaly display the statisical informations
    show_log_statistic(max_resource_path, max_resource_time,
                       total_failed_request, total_bytes_sent,
                       total_resource_time, total_number_request)


# this allow to import this file in other programs
# without worring of running this application
def main():
    'main function of my program'
    std_data = read_standard_input()
    processed_std_data = process_standard(std_data)
    if(len(processed_std_data) == 0):
        logger.error("""The Log information provided can not be
                     analized not correct format or emtty""")
    else:
        logger.info("good log resouces data")

    analize_log_data(processed_std_data)


# ensure that it works fine incase it it imported
if(__name__ == '__main__'):
    main()
# Documentation used
# https://docs.python.org/3/library/logging.html
# https://youtu.be/g8nQ90Hk328
