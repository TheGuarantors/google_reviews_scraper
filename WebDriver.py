from time import sleep
from random import choice
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from settings import maps_url
from parsel import Selector

class WebDriver:
    
    data = dict()

    def __init__(self, list_of_addresses):
        self.list_of_addresses = list_of_addresses
        self.address = None
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--lang=en")
        self.options.add_experimental_option('prefs', {'intl.accept_languages': 'en_GB'})
        self.s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.s, chrome_options=self.options)
        self.driver.maximize_window()
    
    def sleeping(self, duration=''):
        if duration == "High":
            sleep(choice(range(8,12)))
        elif duration == "Medium":
            sleep(choice(range(5,9)))
        elif duration == "Low":
            sleep(choice(range(1, 4)))
        else:
            sleep(choice(range(3,6)))
    
    def go_to_main_page(self):
        self.driver.get(maps_url)
        self.sleeping('Medium')
        
    def find_search_tab(self):
        search_tab = self.driver.find_element_by_xpath('//*[@id="searchboxinput"]')
        search_tab.send_keys(self.address)
        self.sleeping('Medium')
    
    def find_search_button(self):
        search_button = self.driver.find_element_by_xpath('//*[@id="searchbox-searchbutton"]')
        search_button.click()
        self.sleeping('High')
    
    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True
    
    def reviews_existence(self):
        return self.check_exists_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button')
        
    def apartment_existence(self):
        return self.check_exists_by_xpath("//*[contains(text(), 'Apartment building')]") or self.check_exists_by_xpath("//*[contains(text(), 'Apartment complex')]")
    
    def click_on_building_option(self):
        buildings = self.driver.find_elements_by_xpath("//div[contains(@jsaction, 'auxclick:pane.')]")
        building_el = ''
        for building in buildings:
            if 'building' in building.text or 'complex' in building.text or 'appartment' in building.text.lower():
                building.click()
                break
        self.sleeping('Medium')
                
    def expand_all_reviews(self):
        try:
            element = self.driver.find_elements_by_xpath('//button[text()="More"]')
            for i in element:
                i.click()
        except:
            pass
    
    def check_options(self):
        appartment = self.driver.find_elements_by_xpath("//div[@class='MVVflb-haAclf V0h1Ob-haAclf-d6wfac MVVflb-haAclf-uxVfW-hSRGPd']")
        return True if appartment else False
        
    def click_apartment_button(self):       
        appartment = self.driver.find_elements_by_xpath("//div[@class='MVVflb-haAclf V0h1Ob-haAclf-d6wfac MVVflb-haAclf-uxVfW-hSRGPd']")       
        appartment_name = ''
        for ap in appartment:
            if 'apartment building' in ap.text.lower() or 'apartment complex' in ap.text.lower():
                appartment_name = ap.text.split('\n')[0]
                break
        if appartment_name:
            self.driver.find_element_by_xpath(f"//a[@aria-label='{appartment_name}']").click()
        self.sleeping('Medium')
        
    def click_reviews_button(self):
        reviews_button = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button')
        reviews_button.click()
        self.sleeping('High')
        
    def get_scores(self):
        average_score = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[1]')
        WebDriver.data[self.address]['average_score'] = average_score.text

        five_stars_amount = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/table/tbody/tr[1]')
        WebDriver.data[self.address]['five_stars_amount'] = five_stars_amount.get_attribute("aria-label")

        four_stars_amount = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/table/tbody/tr[2]')
        WebDriver.data[self.address]['four_stars_amount'] = four_stars_amount.get_attribute("aria-label")

        three_stars_amount = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/table/tbody/tr[3]')
        WebDriver.data[self.address]['three_stars_amount'] = three_stars_amount.get_attribute("aria-label")

        two_stars_amount = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/table/tbody/tr[4]')
        WebDriver.data[self.address]['two_stars_amount'] = two_stars_amount.get_attribute("aria-label")
        
        one_stars_amount = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/table/tbody/tr[5]')
        WebDriver.data[self.address]['one_stars_amount'] = one_stars_amount.get_attribute("aria-label")
        self.sleeping()
    
    def scroll_page(self):
        total_number_of_reviews = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]').text.split(" ")[0]
        total_number_of_reviews = int(total_number_of_reviews.replace(',','')) if ',' in total_number_of_reviews else int(total_number_of_reviews)
        WebDriver.data[self.address]['total_number_of_reviews'] = total_number_of_reviews
        #Find scroll layout
        scrollable_div = self.driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]')
        #Scroll as many times as necessary to load all reviews
        for i in range(0,(round(total_number_of_reviews/10))):
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', 
                        scrollable_div)
                self.sleeping('Low')
    
    def dict_to_list(self, data):
        data_dict = dict()
        for i in list(enumerate(data)):
            data_dict[i[0]] = i[1]
        return data_dict
    
    def get_reviews(self):
        page_content = self.driver.page_source
        response = Selector(page_content)

        #parse the content
        reviews = []

        for el in response.xpath('//div/div[@data-review-id]/div[contains(@class, "content")]'):
            reviews.append({
                'Name':el.xpath('.//div[contains(@class, "title")]/span/text()').extract_first(''),
                'Rating':el.xpath('.//span[contains(@aria-label, "star")]/@aria-label').extract_first('').replace('stars', '').replace('star', '').strip(),
                'Text':el.xpath('.//span[contains(@class, "text")]/text()').extract_first(''),
                'Date':el.xpath('.//span[contains(@class, "date")]/text()').extract_first(''),
            })  
    
        return self.dict_to_list(reviews)
    
    def scraping(self):
        WebDriver.data[self.address] = {'average_score': '', 
                                        'five_stars_amount': '', 
                                        'four_stars_amount': '', 
                                        'three_stars_amount': '', 
                                        'two_stars_amount': '', 
                                        'one_stars_amount': '',
                                       'total_number_of_reviews': '',
                                       'reviews': ''}
        self.go_to_main_page()
        self.sleeping('Low')
        self.find_search_tab()
        self.find_search_button()
        reviews_existence_flag = self.reviews_existence()
        apartment_existence_flag = self.apartment_existence()
        reviews_flag = False
        if reviews_existence_flag:
            print('First part')
            self.click_reviews_button()
            self.get_scores()
            self.scroll_page()
            self.expand_all_reviews()
            WebDriver.data[self.address]['reviews'] = self.get_reviews()
            reviews_flag = True
        if (apartment_existence_flag or self.check_options()) and not reviews_flag:
            print('Second part')
            self.click_apartment_button()
            if self.reviews_existence():
                self.click_reviews_button()
                self.get_scores()
                self.scroll_page()
                self.expand_all_reviews()
                WebDriver.data[self.address]['reviews'] = self.get_reviews()
                reviews_flag = True
        if not reviews_flag:
            print('Third part')
            self.click_on_building_option()
            if self.reviews_existence():
                self.click_reviews_button()
                self.get_scores()
                self.scroll_page()
                self.expand_all_reviews()
                WebDriver.data[self.address]['reviews'] = self.get_reviews()
                reviews_flag = True
   
    def run_scraping(self):
        counter = 0
        for ad in self.list_of_addresses:
            self.address = ad
            counter += 1
            print(f'Parsing {counter} address: {self.address}')
            try:
                self.scraping()
            except Exception as e:
                print(f'Failed to scrape {self.address} : {str(e)}')
            
        return WebDriver.data
