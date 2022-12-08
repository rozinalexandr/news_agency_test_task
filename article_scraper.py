import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By


class ArticleScraper:
    def __init__(self, companies_list: list):
        self._companies_list = companies_list
        self._path_to_data_dir = "raw_data/"
        self._data_file_name = "output.csv"

    def test_save_to_csv(self, company_name, article_title, article_link, resource_name):
        fieldnames = ["company_name", "article_title", "article_link", "resource_name"]
        row = {
            "company_name": company_name,
            "article_title": article_title,
            "article_link": article_link,
            "resource_name": resource_name
        }
        with open("data/test.csv", 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(row)
            f.close()

    def _save_row_to_csv(self, company_name, article_title, article_link, resource_name):
        fieldnames = ["company_name", "article_title", "article_link", "resource_name"]
        row = {
            "company_name": company_name,
            "article_title": article_title,
            "article_link": article_link,
            "resource_name": resource_name
        }
        with open(self._path_to_data_dir + self._data_file_name, 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(row)
            f.close()

    def _check_data_storage_exists(self):
        if not os.path.exists(self._path_to_data_dir):
            os.mkdir(self._path_to_data_dir)

        if not os.path.exists(self._path_to_data_dir + self._data_file_name):
            fieldnames = ["company_name", "article_title", "article_link", "resource_name"]
            with open(self._path_to_data_dir + self._data_file_name, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                csvfile.close()

    def get_links_pharmatutor(self):
        self._check_data_storage_exists()

        resource_name = "https://www.pharmatutor.org/articles"
        base_url = "https://www.pharmatutor.org/search/node?keys="
        driver = webdriver.Chrome()

        for company in self._companies_list:
            company_name_for_url = company.replace(" ", "%20").replace("&", "%26")
            driver.get(base_url + company_name_for_url + "&_wrapper_format=html&page=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0"
                                                         "%2C0%2C0%2C0")
            try:
                navigation_buttons = driver.find_element(By.CLASS_NAME, "pager").find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")
                last_page_number_link = navigation_buttons[-1].find_element(By.TAG_NAME, "a").get_attribute('href')
                last_page_number = int(last_page_number_link.split("=")[-1].split("%")[0])
            except:
                last_page_number = 0

            for page in range(last_page_number + 1):
                driver.get(base_url + company_name_for_url +
                           f"&_wrapper_format=html&page={page}%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0")

                try:
                    articles = driver.find_element(By.CLASS_NAME, "search-results.node_search-results").find_elements(By.TAG_NAME, "li")
                    for article in articles:
                        article_link = article.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute('href')
                        article_title = article.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").text
                        self._save_row_to_csv(company, article_title, article_link, resource_name)
                except:
                    self._save_row_to_csv(company, "", "", resource_name)

    def get_links_labiotech(self):
        self._check_data_storage_exists()

        resource_name = "https://www.labiotech.eu"
        base_url = "https://www.labiotech.eu/?s="
        driver = webdriver.Chrome()

        for company in self._companies_list:
            company_name_for_url = company.replace(" ", "+").replace("&", "%26")
            driver.get(base_url + company_name_for_url)

            try:
                navigation_buttons = driver.find_element(By.CLASS_NAME, "navigation").find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")
                number_of_last_page = int(navigation_buttons[-2].find_element(By.TAG_NAME, "a").text)
            except:
                number_of_last_page = 1

            for page_number in range(1, number_of_last_page + 1):
                driver.get(f"https://www.labiotech.eu/page/{page_number}/?s={company_name_for_url}")

                try:
                    articles = driver.find_elements(By.TAG_NAME, "article")
                    for article in articles:
                        article_link = article.find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, 'a').get_property('href')
                        article_title = article.find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, 'a').text
                        self._save_row_to_csv(company, article_title, article_link, resource_name)
                except:
                    self._save_row_to_csv(company, "", "", resource_name)

    def get_links_venturebeat(self):
        self._check_data_storage_exists()

        resource_name = "https://venturebeat.com"
        base_url = "https://venturebeat.com/?s="
        driver = webdriver.Chrome()

        for company in self._companies_list:
            company_name_for_url = company.replace(" ", "+").replace("&", "%26")
            driver.get(base_url + company_name_for_url)

            try:
                navigation_buttons = driver.find_elements(By.CLASS_NAME, "page-numbers")
                number_of_last_page = int(navigation_buttons[-2].text)
            except:
                number_of_last_page = 1

            for page in range(1, number_of_last_page + 1):
                driver.get(f"https://venturebeat.com/page/{page}/?s={company_name_for_url}")

                try:
                    articles = driver.find_elements(By.TAG_NAME, "article")
                    for article in articles:
                        article_link = article.find_element(By.TAG_NAME, "a").get_attribute('href')
                        article_title = article.find_element(By.TAG_NAME, "header").find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, "a").text

                        self._save_row_to_csv(company, article_title, article_link, resource_name)
                except:
                    self._save_row_to_csv(company, "", "", resource_name)

    def get_links_hitconsultant(self):
        self._check_data_storage_exists()

        resource_name = "https://hitconsultant.net"
        base_url = "https://hitconsultant.net/?s="
        driver = webdriver.Chrome()

        for company in self._companies_list:
            company_name_for_url = company.replace(" ", "+").replace("&", "%26")
            driver.get(base_url + company_name_for_url)

            try:
                navigation_buttons = driver.find_element(By.CLASS_NAME, "archive-pagination.pagination").find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")
                number_of_last_page = int(navigation_buttons[-2].find_element(By.TAG_NAME, "a").text)
            except:
                number_of_last_page = 1

            for page in range(1, number_of_last_page + 1):
                driver.get(f"https://hitconsultant.net/page/{page}/?s={company_name_for_url}")

                try:
                    articles = driver.find_element(By.TAG_NAME, "main").find_elements(By.TAG_NAME, "article")
                    for article in articles:
                        article_link = article.find_element(By.CLASS_NAME, "entry-title-link").get_attribute('href')
                        article_title = article.find_element(By.CLASS_NAME, "entry-title-link").text
                        self._save_row_to_csv(company, article_title, article_link, resource_name)
                except:
                    self._save_row_to_csv(company, "", "", resource_name)

    def get_links_techcrunch(self):
        self._check_data_storage_exists()

        resource_name = "https://techcrunch.com"
        base_url = "https://techcrunch.com/search"
        driver = webdriver.Chrome()

        for company in self._companies_list:
            driver.get(base_url)
            driver.find_element(By.CLASS_NAME, "form-field__input.form-field__input--text.search-box-form__input").send_keys(f"{company}\n")

            try:
                amount_of_articles = int(driver.find_element(By.CLASS_NAME, "compPagination").find_element(By.TAG_NAME, "span").text.split()[0])
                amount_of_pages = amount_of_articles // 10 + 1
                for page in range(1, amount_of_pages + 1):
                    articles = driver.find_element(By.CLASS_NAME, "compArticleList").find_elements(By.TAG_NAME, "li")
                    for article in articles:
                        article_link = article.find_element(By.CLASS_NAME, "pb-10").find_element(By.TAG_NAME, "a").get_attribute('href')
                        article_title = article.find_element(By.CLASS_NAME, "pb-10").find_element(By.TAG_NAME, "a").text
                        self._save_row_to_csv(company, article_title, article_link, resource_name)
                    try:
                        driver.find_element(By.CLASS_NAME, "compPagination").find_element(By.CLASS_NAME, "next").click()
                    except:
                        pass

            except:
                self._save_row_to_csv(company, "", "", resource_name)
