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
        self.elapsed_time = 0
        self.seniority_array = [["Junior", "Professional", "Senior"],
                                ["1301737", "1301738", "1301739"]]
        
    
    def connect(self, web_driver, url):
        self.driver = webdriver.Firefox(executable_path=web_driver)
        self.driver.get(url)
        
    def allow_cookies(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "cc-allow"))).click()
        
    
    
    #Navigate to search field
    def load_and_switch_to_iframe(self):
        
        self.search_iframe = self.driver.find_element(By.CLASS_NAME, "ti8m-iframe")
        
        desired_y = (self.search_iframe.size['height'] / 2) + self.search_iframe.location['y'] + 100
        current_y = (self.driver.execute_script('return window.innerHeight') / 2) + self.driver.execute_script('return window.pageYOffset')
        scroll_y_by = desired_y - current_y
        self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        time.sleep(4)
        self.first_tab = self.driver.current_window_handle
        self.driver.switch_to.frame(self.search_iframe)
    
    def search_in_field(self, keyword):
        search = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.NAME, "query")))
        #search = self.driver.find_element(By.NAME, "query")
        search.send_keys(keyword)
        search.send_keys(Keys.RETURN)
        time.sleep(5)
        
    def search_in_seniority(self, seniority):
        # script = "return window.getComputedStyle(document.querySelector('div>input.1301739'),':before').getPropertyValue('text')"
        # self.driver.execute_script(script).strip()
        
        index = self.seniority_array[0].index(seniority)
        check = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, self.seniority_array[1][index])))
        #check = self.driver.find_element(By.ID, self.seniority_array[1][index])
        check.send_keys(Keys.SPACE)
        time.sleep(5)
    
    
    def list_job_results(self):
        try:
            self.job_list = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "jobs"))
                )
          
            self.job_results = self.job_list.find_elements(By.TAG_NAME, "a")
            #print(type(self.job_results))
            #self.job_results_iter = iter(self.job_results)
            #print(type(self.job_results))

        except:  
            print("Fail")
            self.driver.quit()
    
    def list_job_results_with_timeout(self, timeout):
        try:
            self.job_list = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.ID, "jobs"))
                )
          
            self.job_results = self.job_list.find_elements(By.TAG_NAME, "a")
            #print(type(self.job_results))
            #self.job_results_iter = iter(self.job_results)
            #print(type(self.job_results))

        except:  
            print("Search timed out.")
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

    def start_timer(self):
        self.elapsed_time = time.perf_counter()
        
    def stop_timer(self):
        self.elapsed_time = time.perf_counter()-self.elapsed_time
        
    def get_timer(self):
        return self.elapsed_time
    
    
    def click_button(self,search_param, btn):
        if search_param == "ID":
            by = By.ID
        elif search_param == "Class":
            by = By.CLASS_NAME
        button = self.job_list = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((by, btn)
            ))
        button.send_keys(Keys.RETURN)
        time.sleep(3)
    
    def fill_jobabo_form_page_1(self, stichwort, standort, bereich, seniorität):
        input_stichwortsuche = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "query"))
            )
        input_stichwortsuche.send_keys(stichwort)
        
        #TODO...fill other checkboxes
        self.click_button("ID", "single-opt-in")

    def fill_jobabo_form_page_2(self, bezeichnung, email):
        input_bezeichnung = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "jobabo_bezeichnung"))
            )
        input_bezeichnung.send_keys(bezeichnung)
        
        input_email = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "jobabo_email"))
            )
        input_email.send_keys(email)
        self.click_button("Class", "jobabo-subscribe-button")
    
      
    

Ti8m=Ti8MLibrary()
Ti8m.connect('C:\Program Files (x86)\geckodriver.exe', 'https://www.ti8m.com/de/career')
Ti8m.load_and_switch_to_iframe()
# Ti8m.start_timer()
# Ti8m.search_in_field('Machine')
# Ti8m.search_in_seniority("Senior")
#time.sleep(5)
# Ti8m.list_job_results()
# Ti8m.list_job_results_with_timeout(0.5)
# print(Ti8m.get_list_of_job_results())
# Ti8m.stop_timer()
# print(Ti8m.get_size_of_job_results() == 1)
# print(Ti8m.get_timer())
# Ti8m.click_link_of_job_result("Professional Python Engineer")
# print(Ti8m.get_job_result_text(0))
Ti8m.click_button("ID", "jobabo-subscribe-button")
Ti8m.fill_jobabo_form_page_1("Python", "Zürich", "Engineering", "Senior")
Ti8m.fill_jobabo_form_page_2("Header", "fzoltan88@gmail.com")

Ti8m.disconnect_webdriver()
