
# remember to run your venv and set virtual en variable pwremail
# pwrpassword using export in the /myenv
import os
import sys
import argparse
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pip._vendor import requests
import urllib
import bs4 as bs

# get environment varible and set them as global variables
EMAIL_ADDRESS = os.environ.get('pwremail')
EMAIL_PASSWORD = os.environ.get('pwrpassword')

parser = argparse.ArgumentParser(description="The email send and web Api lab")
parser.add_argument('-m', '--mail', help="The message to be sent",
                    type=str)
parser.add_argument('-cf', '--cat-facts', help="The message to be sent",
                    type=int)
parser.add_argument('-tc', '--teachers', help='get you list of researchers',
                    type=str)
args = parser.parse_args()


# Task 1
def send_mail(message):
    """Takes a message  as parameter and send message top the prof"""
    # starting the server
    msg = EmailMessage()
    msg["Subject"] = "From "
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "Professorname"
    footer = "Kind regards,\nUser student \n"
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    msg.set_content(f"{message}\n{footer}\n{current_datetime}")
    smtpSrv = smtplib.SMTP("mail.pwr.wroc.pl", 587)
    smtpSrv.starttls()
    smtpSrv.ehlo
    # login
    smtpSrv.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    body = message
    result = smtpSrv.send_message(msg)
    smtpSrv.quit()


# Task 2
def get_cat_facts(number_of_facts):
    """Givem a fact number and rerturns randomly
    select facts from the server and print them , not more than 500 cats"""
    req_baseURL = "https://cat-fact.herokuapp.com/facts/random"
    if number_of_facts <= 0 or number_of_facts > 499:
        print("The APi does not support such number")
        sys.exit()
    query_parm = {"animal_type": "cat", "amount": number_of_facts}
    r = requests.get(req_baseURL, params=query_parm)
    if not r.status_code == 200:
        print("Something Went wrong")
        sys.exit()
    # get the json data
    res_facts = r.json()
    for fact in res_facts:
        print(fact['text'])


# Task 3
def print_teachers(characters):
    """Takes a characer and print thier names"""
    TEACHER_BASEURL = 'https://wiz.pwr.edu.pl/pracownicy?letter='
    page = urllib.request.urlopen(TEACHER_BASEURL + characters)
    page_content = page.read()
    page_bs_parsed = bs.BeautifulSoup(page_content, features='html.parser')
    teachers = page_bs_parsed.find_all("div", {"class": "news-box"})
    print(f"The list of researchers - {characters}")
    if(len(teachers) >= 1):
        for teacher in teachers:
            teacher_name = teacher.find('a', {"class": "title"})
            teacher_email = teacher.find('p')
            print(teacher_name["title"], teacher_email.contents[0])
    else:
        print("Theres is not a resaecher with that names")


# main function of my app
def main():
    """The main program of my app"""
    mail_message = args.mail
    cat_facts_number = args.cat_facts
    teacher_filter = args.teachers
    if mail_message:
        send_mail(mail_message)
    if cat_facts_number:
        get_cat_facts(cat_facts_number)
    if teacher_filter:
        print_teachers(teacher_filter)


if __name__ == '__main__':
    main()
