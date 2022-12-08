from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os


class ArticleScraper:
    """
    This class provides the ability to download the necessary information about the news of various companies from
    several news resources, and saves the data in the .csv format.
    The data, which is downloaded using this class should call 'raw' data, so it needs further preparation and cleanup
    before beginning to extract certain information from articles.
    """
    def __init__(self, companies_list: list):
        """
        :param companies_list: List of companies, which should be passed to the class as an input parameter
        :param path_to_data_dir: Path to directory, where the 'raw' data would be stored
        :param data_file_name: Name of the .csv file with 'raw' data
        """
        self._companies_list = companies_list
        self._path_to_data_dir = "raw_data/"
        self._data_file_name = "output.csv"

    def _save_row_to_csv(self, company_name: str, article_title: str, article_link: str, resource_name: str):
        """
        Method saves information about one article into a .csv file.
        Method adds new row in the end of .csv file. Using this method, we do not store a large amount of data about
        several articles at once. Instead, we save each article as soon as we have the necessary data. So no additional
        memory would be used.
        :param company_name: Name of the company whose articles need to be collected
        :param article_title: Title of an article
        :param article_link: Link which leads to the full article
        :param resource_name: Name of the news resource, from which the data is collected
        """
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
        """
        Method checks if the directory and the .csv file with data exists. If not, this method will create both of them,
        or if the directory exists and the .csv file not - then it will create only a .csv file with required column
        names.
        """
        if not os.path.exists(self._path_to_data_dir):
            os.mkdir(self._path_to_data_dir)

        if not os.path.exists(self._path_to_data_dir + self._data_file_name):
            fieldnames = ["company_name", "article_title", "article_link", "resource_name"]
            with open(self._path_to_data_dir + self._data_file_name, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                csvfile.close()

    def get_links_pharmatutor(self):
        """
        Method scraps the data from this news resource: https://www.pharmatutor.org/articles
        After this method scraps one article, it saves data into the .csv file immediately.
        If there are no articles af some company, method will save only the company name and news resource into a data
        file, leaving some fields (which are related to the existing article) empty.
        """
        self._check_data_storage_exists()

        resource_name = "https://www.pharmatutor.org/articles"
        base_url = "https://www.pharmatutor.org/search/node?keys="
        driver = webdriver.Chrome()

        for company in self._companies_list:
            # convert company name so that it could be found using http request
            company_name_for_url = company.replace(" ", "%20").replace("&", "%26")
            driver.get(base_url + company_name_for_url + "&_wrapper_format=html&page=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0"
                                                         "%2C0%2C0%2C0")
            # some companies have a lot of news articles, and they are located on several pages. Here we find out,
            # how many pages a company has using navigation panel (with a number of the last page).
            try:
                navigation_buttons = driver.find_element(By.CLASS_NAME, "pager").find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")
                last_page_number_link = navigation_buttons[-1].find_element(By.TAG_NAME, "a").get_attribute('href')
                last_page_number = int(last_page_number_link.split("=")[-1].split("%")[0])
            except:
                last_page_number = 0

            # going through each page, we collect information of all articles that are placed on a single page
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
                    # if there are no articles of a company, we will save into .csv file only a company and resource
                    # name, leaving article title and article link empty
                    self._save_row_to_csv(company, "", "", resource_name)

    def get_links_labiotech(self):
        """
        Method scraps the data from this news resource: https://www.labiotech.eu
        After this method scraps one article, it saves data into the .csv file immediately.
        If there are no articles af some company, method will save only the company name and news resource into a data
        file, leaving some fields (which are related to the existing article) empty.
        """
        self._check_data_storage_exists()

        resource_name = "https://www.labiotech.eu"
        base_url = "https://www.labiotech.eu/?s="
        driver = webdriver.Chrome()

        for company in self._companies_list:
            # convert company name so that it could be found using http request
            company_name_for_url = company.replace(" ", "+").replace("&", "%26")
            driver.get(base_url + company_name_for_url)

            # some companies have a lot of news articles, and they are located on several pages. Here we find out,
            # how many pages a company has using navigation panel (with a number of the last page).
            try:
                navigation_buttons = driver.find_element(By.CLASS_NAME, "navigation").find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")
                number_of_last_page = int(navigation_buttons[-2].find_element(By.TAG_NAME, "a").text)
            except:
                number_of_last_page = 1

            # going through each page, we collect information of all articles that are placed on a single page
            for page_number in range(1, number_of_last_page + 1):
                driver.get(f"https://www.labiotech.eu/page/{page_number}/?s={company_name_for_url}")

                try:
                    articles = driver.find_elements(By.TAG_NAME, "article")
                    for article in articles:
                        article_link = article.find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, 'a').get_property('href')
                        article_title = article.find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, 'a').text
                        self._save_row_to_csv(company, article_title, article_link, resource_name)
                except:
                    # if there are no articles of a company, we will save into .csv file only a company and resource
                    # name, leaving article title and article link empty
                    self._save_row_to_csv(company, "", "", resource_name)

    def get_links_venturebeat(self):
        """
        Method scraps the data from this news resource: https://venturebeat.com
        After this method scraps one article, it saves data into the .csv file immediately.
        If there are no articles af some company, method will save only the company name and news resource into a data
        file, leaving some fields (which are related to the existing article) empty.
        """
        self._check_data_storage_exists()

        resource_name = "https://venturebeat.com"
        base_url = "https://venturebeat.com/?s="
        driver = webdriver.Chrome()

        for company in self._companies_list:
            # convert company name so that it could be found using http request
            company_name_for_url = company.replace(" ", "+").replace("&", "%26")
            driver.get(base_url + company_name_for_url)

            # some companies have a lot of news articles, and they are located on several pages. Here we find out,
            # how many pages a company has using navigation panel (with a number of the last page).
            try:
                navigation_buttons = driver.find_elements(By.CLASS_NAME, "page-numbers")
                number_of_last_page = int(navigation_buttons[-2].text)
            except:
                number_of_last_page = 1

            # going through each page, we collect information of all articles that are placed on a single page
            for page in range(1, number_of_last_page + 1):
                driver.get(f"https://venturebeat.com/page/{page}/?s={company_name_for_url}")

                try:
                    articles = driver.find_elements(By.TAG_NAME, "article")
                    for article in articles:
                        article_link = article.find_element(By.TAG_NAME, "a").get_attribute('href')
                        article_title = article.find_element(By.TAG_NAME, "header").find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, "a").text
                        self._save_row_to_csv(company, article_title, article_link, resource_name)
                except:
                    # if there are no articles of a company, we will save into .csv file only a company and resource
                    # name, leaving article title and article link empty
                    self._save_row_to_csv(company, "", "", resource_name)

    def get_links_hitconsultant(self):
        """
        Method scraps the data from this news resource: https://hitconsultant.net
        After this method scraps one article, it saves data into the .csv file immediately.
        If there are no articles af some company, method will save only the company name and news resource into a data
        file, leaving some fields (which are related to the existing article) empty.
        """
        self._check_data_storage_exists()

        resource_name = "https://hitconsultant.net"
        base_url = "https://hitconsultant.net/?s="
        driver = webdriver.Chrome()

        for company in self._companies_list:
            # convert company name so that it could be found using http request
            company_name_for_url = company.replace(" ", "+").replace("&", "%26")
            driver.get(base_url + company_name_for_url)

            # some companies have a lot of news articles, and they are located on several pages. Here we find out,
            # how many pages a company has using navigation panel (with a number of the last page).
            try:
                navigation_buttons = driver.find_element(By.CLASS_NAME, "archive-pagination.pagination").find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")
                number_of_last_page = int(navigation_buttons[-2].find_element(By.TAG_NAME, "a").text)
            except:
                number_of_last_page = 1

            # going through each page, we collect information of all articles that are placed on a single page
            for page in range(1, number_of_last_page + 1):
                driver.get(f"https://hitconsultant.net/page/{page}/?s={company_name_for_url}")

                try:
                    articles = driver.find_element(By.TAG_NAME, "main").find_elements(By.TAG_NAME, "article")
                    for article in articles:
                        article_link = article.find_element(By.CLASS_NAME, "entry-title-link").get_attribute('href')
                        article_title = article.find_element(By.CLASS_NAME, "entry-title-link").text
                        self._save_row_to_csv(company, article_title, article_link, resource_name)
                except:
                    # if there are no articles of a company, we will save into .csv file only a company and resource
                    # name, leaving article title and article link empty
                    self._save_row_to_csv(company, "", "", resource_name)

    def get_links_techcrunch(self):
        """
        Method scraps the data from this news resource: https://techcrunch.com
        After this method scraps one article, it saves data into the .csv file immediately.
        If there are no articles af some company, method will save only the company name and news resource into a data
        file, leaving some fields (which are related to the existing article) empty.
        """
        self._check_data_storage_exists()

        resource_name = "https://techcrunch.com"
        base_url = "https://techcrunch.com/search"
        driver = webdriver.Chrome()

        for company in self._companies_list:
            # the previous method of parsing using http requests will not work here, because of the unique structure
            # of each request. Thus, we will enter the names of companies in the search field of the news resource.
            driver.get(base_url)
            driver.find_element(By.CLASS_NAME, "form-field__input.form-field__input--text.search-box-form__input").send_keys(f"{company}\n")

            try:
                # since we cannot pass the number of pages in the request, we will find the total number of existing
                # pages and will click on "show next page" to collect all the articles about the company
                amount_of_articles = int(driver.find_element(By.CLASS_NAME, "compPagination").find_element(By.TAG_NAME, "span").text.split()[0])
                amount_of_pages = amount_of_articles // 10 + 1

                for page in range(1, amount_of_pages + 1):
                    articles = driver.find_element(By.CLASS_NAME, "compArticleList").find_elements(By.TAG_NAME, "li")
                    for article in articles:
                        article_link = article.find_element(By.CLASS_NAME, "pb-10").find_element(By.TAG_NAME, "a").get_attribute('href')
                        article_title = article.find_element(By.CLASS_NAME, "pb-10").find_element(By.TAG_NAME, "a").text
                        self._save_row_to_csv(company, article_title, article_link, resource_name)
                    try:
                        # click on "Next" button to load a new page with new articles
                        driver.find_element(By.CLASS_NAME, "compPagination").find_element(By.CLASS_NAME, "next").click()
                    except:
                        # if we have gone through all pages, the button "Next" would disappear. To not break all method,
                        # we are using here try/except
                        pass

            except:
                # if there are no articles of a company, we will save into .csv file only a company and resource
                # name, leaving article title and article link empty
                self._save_row_to_csv(company, "", "", resource_name)

    def get_all_links(self):
        """
        Method allows us to scrap all the information from available news resources at once, without calling each method
        individually.
        """
        self.get_links_labiotech()
        self.get_links_pharmatutor()
        self.get_links_venturebeat()
        self.get_links_techcrunch()
        self.get_links_hitconsultant()
