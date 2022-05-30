import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from page_element import base_element
from datetime import datetime
import logging
import sys


class imperva_github:
    """
    Program to fetch information from Github with selenium.
    """

    def __init__(self):
        """
        Initializer values.
        """
        logging.basicConfig(level=logging.INFO)
        if sys.platform == "Windows":
            logging.info("Executing test on Windows os...")
        elif sys.platform == "Linux":
            logging.info("Executing test on Linux os...")
        else:
            print("Sorry, we don't currently have support for the " + sys.platform + "OS")
        self.project_path = os.getcwd()
        self.tool_path = os.path.join(self.project_path, 'tools')
        if sys.platform == "Linux":
            self.driver = webdriver.Chrome(self.tool_path + '/chromedriver')
        else:
            self.driver = webdriver.Chrome(self.tool_path + '\chromedriver.exe')
        self.date_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

    def get_title(self, parent_element, selector, range):
        logging.info("fetching title name...")
        data = parent_element[0].find_elements(By.CSS_SELECTOR, selector.format(range))[0].text
        return data

    def get_description(self, parent_element, selector, range):
        logging.info("fetching description name...")
        if parent_element[0].find_elements(By.CSS_SELECTOR, selector.format(range)):
            description = parent_element[0].find_elements(By.CSS_SELECTOR, selector.format(range))[0].text
            return description
        else:
            return None

    def get_tag(self, parent_element, selector):
        logging.info("fetching tags name...")
        if parent_element[0].find_elements(By.CSS_SELECTOR, selector):
            tags = parent_element[0].find_elements(By.CSS_SELECTOR, selector)
            return ','.join(v.text for v in tags)
        else:
            return None

    def get_language(self, parent_element, selector):
        logging.info("fetching language name...")
        if parent_element[0].find_elements(By.CSS_SELECTOR, selector):
            language = parent_element[0].find_elements(By.CSS_SELECTOR, selector)[0]
            return language.text
        else:
            return None

    def get_stars(self, parent_element, selector):
        logging.info("fetching stars count...")
        stars = parent_element[0].find_elements(By.CSS_SELECTOR, selector)[0]
        return stars.text

    def get_license(self, parent_element, selector):
        logging.info("fetching license name...")
        if parent_element[0].find_elements(By.CSS_SELECTOR, selector):
            lincencedBy = parent_element[0].find_elements(By.CSS_SELECTOR, selector)[0]
            if 'license' in lincencedBy.text:
                return lincencedBy.text
            else:
                return None
        else:
            return None

    def get_updateTime(self, parent_element, selector):
        logging.info("fetching updateTime name...")
        if parent_element[0].find_elements(By.CSS_SELECTOR, selector):
            updateTime = parent_element[0].find_elements(By.CSS_SELECTOR, selector)[0]
            return updateTime.text
        else:
            if parent_element[0].find_elements(By.CSS_SELECTOR, selector.replace('3', '2')):
                updateTime = parent_element[0].find_elements(By.CSS_SELECTOR, selector.replace('3', '2'))[0]
                return updateTime.text
            else:
                return None

    def json_gen(self, data, date_time):
        with open(r'SecurityResultGitHub-{}.json'.format(date_time), 'w') as fl:
            fl.write("{}".format(data))
        return "SecurityResultGitHub-{}.json".format(date_time)

    def json_append(self, data, filename):
        with open(filename, 'a', encoding="utf-8") as fl:
            fl.write("{}\n".format(data))

    def runner(self):
        filename = self.json_gen("", self.date_time)
        for num in range(1, int(base_element.pages) + 1):

            if num == 1:
                self.driver.get(base_element.base_url)
                self.driver.maximize_window()
                search_bar = self.driver.find_element(By.CSS_SELECTOR, base_element.search_bar)
                search_bar.clear()
                search_bar.send_keys('security')
                time.sleep(2)
                suggestion = self.driver.find_element(By.CSS_SELECTOR, base_element.suggestion)
                suggestion.click()
                time.sleep(2)
            else:
                self.driver.get(base_element.api_query.format(num))
                self.driver.maximize_window()

            # try:
            for result_cnt in range(1, base_element.per_page_result + 1):
                parent_oject = self.driver.find_elements(By.CSS_SELECTOR, base_element.search_result.format(result_cnt))

                title = self.get_title(parent_oject, base_element.title, result_cnt)
                description = self.get_description(parent_oject, base_element.description, result_cnt)
                tag = self.get_tag(parent_oject, base_element.tag)
                stars = self.get_stars(parent_oject, base_element.stars)
                language = self.get_language(parent_oject, base_element.language)
                lincencedBy = self.get_license(parent_oject, base_element.lincencedBy)
                if not lincencedBy:
                    logging.info("license name not available...")
                    logging.info("fetching updatetime with same element...")
                    updateTime = self.get_updateTime(parent_oject, base_element.lincencedBy)
                    data = title,description,tag,stars,language,lincencedBy,updateTime
                    self.json_append(data, filename)
                    continue
                updateTime = self.get_updateTime(parent_oject, base_element.updateTime)
                data = title,description,tag,stars,language,lincencedBy,updateTime
                logging.info('dumping data into json file..')
                self.json_append(data, filename)
        logging.info("closing initialized browser...")
        self.driver.quit()
        logging.info("Test Completed...")
        logging.info("Open Json file here : {}".format(os.path.join(self.project_path,filename)))

main = imperva_github()
main.runner()
