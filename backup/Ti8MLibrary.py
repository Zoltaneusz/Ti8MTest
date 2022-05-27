from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Ti8MLibrary:

    def __init__(self) -> None:
        self.output = ''
        self.driver = None
        self.job_results= []
        self.job_list = []
        self.first_tab = ''
        self.search_iframe = None
        
    
    def connect(self, web_driver, url):
        self.driver = webdriver.Firefox(executable_path=web_driver)
        self.driver.get(url)
        
    
    
    #Navigate to search field
    def load_and_switch_to_iframe(self):
        
        self.search_iframe = self.driver.find_element(By.CLASS_NAME, "ti8m-iframe")
        
        desired_y = (self.search_iframe.size['height'] / 2) + self.search_iframe.location['y']
        current_y = (self.driver.execute_script('return window.innerHeight') / 2) + self.driver.execute_script('return window.pageYOffset')
        scroll_y_by = desired_y - current_y
        self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        time.sleep(4)
        self.first_tab = self.driver.current_window_handle
        self.driver.switch_to.frame(self.search_iframe)
    
    def search_in_field(self, keyword):
        search = self.driver.find_element(By.NAME, "query")
        search.send_keys(keyword)
        search.send_keys(Keys.RETURN)
        time.sleep(5)
        
    def search_in_seniority(self,"Senior"):
        
    
    
    def list_job_results(self):
        try:
            self.job_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobs"))
                )
          
            self.job_results = self.job_list.find_elements(By.TAG_NAME, "a")
            #print(type(self.job_results))
            #self.job_results_iter = iter(self.job_results)
            #print(type(self.job_results))

        except:  
            print("Fail")
            self.driver.quit()
    
    def get_list_of_job_results(self):
        job_result_texts= []
        for job in self.job_results:
            #print(job.text)
            job_result_texts.append(job.text)
        return job_result_texts
    
    def get_job_result_text(self, ind):
        return self.job_results[int(ind)].text
    
    def get_size_of_job_results(self):
        #return sum(1 for _ in self.job_results)
        #return len(list(self.job_results_iter))
        return len(self.job_results)
    
    def click_link_of_job_result(self, link):
        #self.driver.switch_to.window(self.first_tab)
        #time.sleep(5)
        job_link = self.job_list.find_element(By.LINK_TEXT, link)
        job_link.click()
        time.sleep(2)
        self.driver.switch_to.window(self.first_tab)
        self.driver.switch_to.frame(self.search_iframe)
        
        time.sleep(2)
    
    def get_job_result_location(self):
        found_location = self.job_list.find_element(By.CLASS_NAME, "location")
        return found_location.text
    
    def disconnect_webdriver(self):
        self.driver.quit()

# Ti8m=Ti8MLibrary()
# Ti8m.connect('C:\Program Files (x86)\geckodriver.exe', 'https://www.ti8m.com/de/career')
# Ti8m.load_and_switch_to_iframe()
# Ti8m.search_in_field('Python')
# Ti8m.list_job_results()
# print(Ti8m.get_list_of_job_results())
# print(Ti8m.get_size_of_job_results())
# Ti8m.click_link_of_job_result("Professional Python Engineer")
# print(Ti8m.get_job_result_text(0))
# Ti8m.disconnect_webdriver()
