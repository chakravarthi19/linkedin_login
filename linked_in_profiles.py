from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from linked_in import config
from builtins import print
from bson import ObjectId
import traceback
import datetime
import random
import time
import sys
import re


class LinkedIn:

    def __init__(self):
        print("start_time:", datetime.datetime.now())
        self.driver = config.driver
        self.base_url = "https://in.linkedin.com"

    def google_search(self):
        # first 100 docs in some docs are not scraped
        for docs in config.db.find({"flags.cd_scraped": True,
                                    "recruiter_details.company_name": {"$ne": None and str(" ")},
                                    # "flags.linkedin": True,
                                    "flags.linkedin": {"$exists": False}
                                    # "_id": ObjectId('5bbcd8c2e91c5c3d0d18f28f')
                                    }, no_cursor_timeout=True):
            try:
                # phone_no = docs['recruiter_details']['phone_no']
                # email_id = docs['recruiter_details']['email_id']
                i_d = str(docs['_id'])
                print(i_d)
                # if phone_no is not None or email_id is not None:
                company_name = docs['recruiter_details']['company_name']
                print("company_name: >><<", company_name)
                self.driver.get(config.input_url)
                input_element = self.driver.find_element_by_xpath('//*[@id="lst-ib"]')
                input_element.send_keys(company_name)
                time.sleep(2)
                input_element.send_keys(Keys.ENTER)
                time.sleep(10)
                soup = BeautifulSoup(self.driver.page_source, "lxml")
                srg = soup.find(config.div_tag, config.srg_class)
                links = []
                if srg.find_all(config.div_tag, config.rc_class):
                    for r_value in srg.find_all(config.div_tag, config.rc_class):
                        a_tag = r_value.find(config.a_tag)[config.href]
                        if self.base_url in a_tag:
                            links.append(a_tag)
                        elif "https://www.linkedin.com" in a_tag:
                            links.append(a_tag)
                print(links)
                # if len(links) is 0:
                #
                self.linked_search_page(links, i_d)
            except Exception as e:
                    print("error:", str(e))
    @staticmethod
    def linkedin_login():
        config.linkedin_login()
        # print("entering into login page...!!!")
        # config.driver.get(config.linked_in_login_page)
        # if config.driver.find_element_by_xpath(config.username_class):
        #     config.driver.find_element_by_xpath(config.username_class).send_keys(config.user_name)
        # else:
        #     print("username class changed...")
        # if config.driver.find_element_by_xpath(config.password_class):
        #     config.driver.find_element_by_xpath(config.password_class).send_keys(config.password)
        # else:
        #     print("password class changed...")
        # if config.driver.find_element_by_xpath(config.login_button):
        #     config.driver.find_element_by_xpath(config.login_button).click()
        # else:
        #     print("login_button class changed...")

    def linked_search_page(self, links, i_d):
        for l_in_k in links:
            file = open(config.f_name, "w")
            self.driver.get(l_in_k)
            print(l_in_k)
            # random.randint(7, 10)
            time.sleep(10)
            random.randint(5, 15)
            self.driver.find_element_by_xpath(config.company_details_btn).click()
            random.randint(8, 16)
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            file.write(str(soup))
            print("clicked...!!!")
            self.file_open(l_in_k, i_d)
        # self.driver.close()

    def file_open(self, l_in_k, i_d):
        fp = open(config.f_name, "rb")
        soup = BeautifulSoup(fp, "lxml")
        u_id = l_in_k.replace(self.base_url+"/company/", "").replace(self.base_url+"/jobs/", "")
        d = {"company_name": None, "organization": None, "location": None, "followers": None, "emp_count": None,
             "desc": None, "website": None, "head_office": None, "company_type": None, "started_year": None,
             "company_size": {"min": None, "max": None}, "company_speciality": None, "from_google_link": None,
             'from_google_link': l_in_k, "unique_id": u_id}

        try:
            if soup.find(config.h1_tag, config.c_name):
                d['company_name'] = soup.find(config.h1_tag, config.c_name).text.replace("\n", "").strip()
            if soup.find(config.span_tag, config.c_org):
                d['organization'] = soup.find(config.span_tag, config.c_org).text.replace("\n", "").strip()
            if soup.find(config.span_tag, config.c_location):
                d['location'] = soup.find(config.span_tag, config.c_location).text.replace("\n", "").strip()
            if soup.find(config.span_tag, config.c_followers):
                c_followers = soup.find(config.span_tag, config.c_followers).text.replace("\n", "").strip()\
                    .replace(",", "")
                d['followers'] = int(re.match("\d+", c_followers).group())
            if soup.find(config.span_tag, config.emp_count):
                c_emp_count = soup.find(config.span_tag, config.emp_count).text.replace("\n", "").strip()\
                    .replace("See all ", "").replace(" employees on LinkedIn", "").replace(",", "")
                d['emp_count'] = int(c_emp_count)
                # d['emp_count'] = re.match("\d+", c_emp_count).group()
            if soup.find(config.p_tag, config.desc):
                d['desc'] = str(soup.find(config.p_tag, config.desc).text)
            if soup.find(config.a_tag, config.websitte):
                d['website'] = soup.find(config.a_tag, config.websitte)[config.href]
            if soup.find(config.p_tag, config.headquarters):
                d['head_office'] = soup.find(config.p_tag, config.headquarters).text.replace("\n", "").strip()
            if soup.find(config.p_tag, config.established_year):
                d['started_year'] = soup.find(config.p_tag, config.established_year).text.replace("\n", "").strip()
            if soup.find(config.p_tag, config.c_type):
                d['company_type'] = soup.find(config.p_tag, config.c_type).text.replace("\n", "").strip()
            if soup.find(config.p_tag, config.staff_count):
                sas = soup.find(config.p_tag, config.staff_count).text.replace("\n", "").strip()\
                    .replace(" employees", "").replace(",", "").replace("+", "").split("-")
                if len(sas) == 1:
                    d['company_size']['min'] = int(sas[0])
                elif len(sas) == 2:
                    d['company_size']['min'] = int(sas[0])
                    d['company_size']['max'] = int(sas[1])

            if soup.find(config.p_tag, config.specialities):
                d['company_speciality'] = soup.find(config.p_tag, config.specialities).text.replace("\n", "").\
                    strip().split(",")
            d["from_doc_details"] = {"db_name": config.db_naukri, "collection_name": config.coll_naukri,
                                     "doc_id": ObjectId(i_d)}
            try:
                x = config.linkedin_db.find_one({"from_google_link": l_in_k})
                if x:
                    print('Duplicate link ', l_in_k)
                else:
                    # print("count:", count, "json:", json)
                    print("### INSERT-ID:", config.linkedin_db.insert(d))
            except Exception as e:
                config.logger.error(str(e))
                print("error:" + str(e))

        except Exception as e:
            print("error:", str(e))
            traceback.print_exc(file=sys.stdout)
            print("error_time:--", datetime.datetime.now())
        print(d)
        print(config.db.update({"_id": ObjectId(i_d)}, {"$set": {"flags.linkedin": True}}))
        print("end time:--", datetime.datetime.now())
        print("***************************************************************************************************")


if __name__ == '__main__':
    lin = LinkedIn()
    lin.linkedin_login()
    lin.google_search()
    time.sleep(50)
    config.driver.close()
