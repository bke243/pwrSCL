import sys
import logging
import os
# create and configure logger in the current working dir
# works for all os
LOG_FORMAT = '%(levelname)s %(asctime)s %(filename)s - %(message)s'
logging.basicConfig(filename=os.path.join(os.getcwd(), 'logdata.txt'),
                    level=logging.DEBUG, format=LOG_FORMAT)
# root logger
logger = logging.getLogger()
logger.info("START")


def analize_log_file(login_list):
    'takes a list containing a lists of log information and analyaze them'
    logger.info('analize_log_file({})'.format(login_list))
    max_resource_path = str()
    max_resource_time = 0
    total_failed_request = 0
    total_bytes_sent = 0
    total_rousource_time = 0
    total_request_sent = 0
    log_info_line = str()
    for (path, status_code, size, time) in login_list:

        if(int(time) > max_resource_time):
            max_resource_time = int(time)
            max_resource_path = path
        if(int(status_code) == 404):
            log_info_line = '!{} {} {}'
            total_failed_request += 1
        else:
            log_info_line = '{} {} {}'
        total_bytes_sent += int(size)
        total_rousource_time += int(time)
        total_request_sent += 1
        print(log_info_line.format(path, status_code, size, time))

    show_log_statistic(max_resource_path, max_resource_time,
                       total_failed_request, total_bytes_sent,
                       total_rousource_time, total_request_sent)


def show_log_statistic(max_resource_path='', max_resource_time=0,
                       total_failed_request=0, total_bytes_sent=0,
                       total_rousource_time=0,
                       totalt_request_sent=0):
    """Print a formatted message displaying the statical information of
    the log file"""
    logger.info('show_log_statistic({}, {}, {}, {}, {}, {})'.format(
                max_resource_path, max_resource_time, total_failed_request,
                total_bytes_sent, total_rousource_time, totalt_request_sent))
    request_mean = 0
    if(total_bytes_sent != 0):
        request_mean = total_rousource_time / totalt_request_sent
    print('\n=====STATISITCS OF THE LOG FILE=====\n')
    print('the path: {} has the largest processing time which is: {}'.
          format(max_resource_path, max_resource_time))
    print('the total number of failed request is: {}'.
          format(total_failed_request))
    print('The total number of bytes sent is: {}'.format(total_bytes_sent))
    print('The total number of Kilobytes sent is: {}'.
          format(total_bytes_sent * 0.001))
    print('The mean processing time of a single request is: {}'.
          format(request_mean))
    print('\n=====END OF THE LOG FILE=====')


def is_Empty(lines):
    'Check if the lines are empty lines'
    not_empty = True
    for i in lines:
        if(len(i.strip()) == 0):
            not_empty = False
            break
    return not not_empty


lines = sys.stdin.readlines()
if(is_Empty(lines)):
    logger.error('Wrong input logging data information')
    print('Wrong input log data')
    exit(1)
else:
    new_lines = [i.split() for i in lines]
    analize_log_file(new_lines)
# https://docs.python.org/3/library/logging.html
# https://youtu.be/g8nQ90Hk328
