from selenium import webdriver
import logging
from logging.handlers import RotatingFileHandler
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
from builtins import print


logfile = "/home/kalyan/Kalyan_working_dir/PycharmProjects/Naukri_Recruiters/linked_in/linkedin_log.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s | %(lineno)s| %(funcName)s | %(message)s')
handler = RotatingFileHandler(logfile, maxBytes=100000, backupCount=1)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

db_naukri = 'naukri_recruiters'
coll_naukri = "naukri_recruiters_Modify"
db = MongoClient("localhost", 27017)[db_naukri][coll_naukri]
linkedin_db = MongoClient("localhost", 27017)['linkedin']['company_info']

firefox_path = "/home/kalyan/geckodriver"
phantomjs_path = "/home/kalyan/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
crome_path = "/home/kalyan/chromedriver"

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
# driver = webdriver.Chrome(executable_path=crome_path, chrome_options=chrome_options)
driver = webdriver.Firefox(executable_path=firefox_path)
# driver = webdriver.PhantomJS(executable_path=phantomjs_path)

linked_in_login_page = "https://www.linkedin.com/"
username_class = '//*[@id="login-email"]'
user_name = "alexandersharma@mail.com"
password_class = '//*[@id="login-password"]'
password = "Alexander@69"
login_button = '//*[@id="login-submit"]'
search_id_class = '//*[@id="ember901"]/input'

# soup classes:--
href = 'href'
h1_tag = "h1"
span_tag = "span"
p_tag = "p"
a_tag = "a"
c_name = {"class": "org-top-card-module__name t-24 t-black t-light"}
c_org = {"class": "company-industries org-top-card-module__dot-separated-list"}
c_location = {"class": "org-top-card-module__location org-top-card-module__dot-separated-list"}
c_followers = {"class": "org-top-card-module__followers-count org-top-card-module__dot-separated-list"}
emp_count = {"class": "org-company-employees-snackbar__see-all-employees-link"}
desc = {"class": "org-about-us-organization-description__text description mb5 pre-wrap t-14 t-black--light t-normal"}
websitte = {"class": "org-about-us-company-module__website mb3 link-without-visited-state ember-view"}
headquarters = {"class": "org-about-company-module__headquarters t-14 t-black--light t-normal mb3"}
c_type = {"class": "org-about-company-module__company-type t-14 t-black--light t-normal mb3"}
established_year = {"class": "org-about-company-module__founded t-14 t-black--light t-normal mb3"}
staff_count = {"class": "org-about-company-module__company-staff-count-range t-14 t-black--light t-normal mb3"}
specialities = {"class": "org-about-company-module__specialities mb5 t-14 t-black--light t-normal mb3"}

company_details_btn = '//*[@id="org-about-company-module__show-details-btn"]/span[1]'

f_name = "/home/kalyan/Kalyan_working_dir/PycharmProjects/Naukri_Recruiters/linked_in/page.html"


# google search classes
input_url = "https://www.google.com/"
search_input_class = '//*[@id="lst-ib"]'
srg_class = {"class": "srg"}
div_tag = 'div'
rc_class = {"class": "rc"}



def linkedin_login():
    print("entering into login page...!!!")
    driver.get(linked_in_login_page)
    if driver.find_element_by_xpath(username_class):
        driver.find_element_by_xpath(username_class).send_keys(user_name)
    else:
        print("username class changed...")
    if driver.find_element_by_xpath(password_class):
        driver.find_element_by_xpath(password_class).send_keys(password)
    else:
        print("password class changed...")
    if driver.find_element_by_xpath(login_button):
        driver.find_element_by_xpath(login_button).click()
    else:
        print("login_button class changed...")