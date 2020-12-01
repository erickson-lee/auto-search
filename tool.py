#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

class AutoSearcher:

    def __init__(self):
    
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('./chromedriver', 
		                        chrome_options=chrome_options)
	
    def search_and_collect(self, input_keyword='零食'):
    
        search_url = 'https://google.com.tw/'    
        self.driver.get(search_url)
        input_element = self.driver.find_element_by_name('q')
        input_element.clear()
        input_element.send_keys(input_keyword)
        input_element.submit()
		
        if not self.driver.page_source:
            return None
		
        is_final = False
        result = []
        number = 1
		
        while is_final != True:
            html_page = self.driver.page_source
            soup = BeautifulSoup(html_page, 'html.parser')
            
            for text in soup.find_all('div',{'class':'yuRUbf'}):
                url = text.a['href']
                title = text.span.string
                result.append([number, url, title])
                number = number + 1

            time.sleep(2)

            try:
                self.driver.find_element_by_link_text('下一頁').click()
            except NoSuchElementException:
                is_final = True
            
        self.close_browser()
                
        return result
		
    def change_region(self, target_region='Taiwan'):
            
        setting_url = 'https://www.google.com.tw/preferences?hl=en'
        is_success = False
        self.driver.get(setting_url)

        if not self.driver.page_source:
            return is_success
		
	    # click show more button
        self.driver.find_element_by_id('regionanchormore').click()
    
        # search and click target region button
        for i in self.driver.find_elements_by_xpath("//div[@class='DB6WRb']"):
            if i.text == target_region:
                i.click()
                #save setting
                self.driver.find_element_by_css_selector(
                        '.goog-inline-block.jfk-button.jfk-button-action').click()
                is_success = True
                break

        return is_success

    def close_browser(self):
        self.driver.quit()
