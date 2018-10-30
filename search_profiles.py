from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from linked_in import config
from builtins import print
import time


class search_in_linkedin:
    #
    # def linkedin_login(self):
    #
    #     print("entering into login page...!!!")
    #     config.driver.get(config.linked_in_login_page)
    #     if config.driver.find_element_by_xpath(config.username_class):
    #         config.driver.find_element_by_xpath(config.username_class).send_keys(config.user_name)
    #     else:
    #         print("username class changed...")
    #     if config.driver.find_element_by_xpath(config.password_class):
    #         config.driver.find_element_by_xpath(config.password_class).send_keys(config.password)
    #     else:
    #         print("password class changed...")
    #     if config.driver.find_element_by_xpath(config.login_button):
    #         config.driver.find_element_by_xpath(config.login_button).click()
    #     else:
    #         print("login_button class changed...")
    @staticmethod
    def modify_search():
        # config.driver =
        config.linkedin_login()
        time.sleep(10)
        # if config.driver.find_element_by_xpath('//*[@id="ember1216"]/input'):
        # in_put = config.driver.find_element_by_xpath('//*[@id="ember901"]/input')
        # config.driver.fin
        if config.driver.find_element_by_xpath('//*[@id="extended-nav"]/div'):
            print("nav-bar verified..!!")
            config.driver.find_element_by_xpath('//*[@id="ember901"]/input').click()
            print("search-input clicked..!!")
            config.driver.find_element_by_xpath('//*[@id="ember901"]/input').send_keys("vivo")
            config.driver.find_element_by_xpath('//*[@id="ember901"]/input').click()


            # config.driver.find_element_by_xpath('//*[@id="ember901"]/input').click()
            # config.driver.find_element_by_xpath('//*[@id="ember901"]/input').send_keys("vivo")
            # config.driver.find_element_by_xpath('//*[@id="ember901"]/input').click()
            # config.driver.find_element_by_xpath('//*[@id="ember901"]/input').send_keys(Keys.ENTER)
        


if __name__ == '__main__':
    sil = search_in_linkedin()
    sil.modify_search()