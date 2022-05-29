#from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver

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
        self.stichwort = None
        self.standort = None
        self.bereich = None
        self.seniorität = None
        self.bezeichnung = None
        self.email = None
        
    
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
        #search.send_keys(Keys.RETURN)
        time.sleep(10)
        
    def search_in_seniority(self, seniority):
        # script = "return window.getComputedStyle(document.querySelector('div>input.1301739'),':before').getPropertyValue('text')"
        # self.driver.execute_script(script).strip()
        
        index = self.seniority_array[0].index(seniority)
        check = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, self.seniority_array[1][index])))
        #check = self.driver.find_element(By.ID, self.seniority_array[1][index])
        check.send_keys(Keys.SPACE)
        time.sleep(10)
    
    
    def list_job_results(self):
        try:
            self.job_list = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "jobs"))
                )
          
            self.job_results = self.job_list.find_elements(By.TAG_NAME, "a")
            # self.job_results = WebDriverWait(self.driver, 15).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, nr_of_jobs))
            #     )
            
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
        return str(len(self.job_results))
    
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
    
    
    def send_key_to_button(self,search_param, btn, key):
        if search_param == "ID":
            by = By.ID
        elif search_param == "Class":
            by = By.CLASS_NAME
            
        if key == "Return":
            pressed_key = Keys.RETURN
        elif key == "Space":
            pressed_key = Keys.SPACE
         
        button = self.job_list = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((by, self.web_element_ID_finder(btn))
            ))
        button.send_keys(pressed_key)
        time.sleep(3)

    def web_element_ID_finder(self, input_elem):
        if input_elem == "Jobabo":
            return "jobabo-subscribe-button"
        elif input_elem == "Terms Checkbox":
            return "single-opt-in"
        else: return "NaN"

    def input_jobabo_form_data(self, stichwort, standort, bereich, seniorität, bezeichnung, email):
        self.stichwort = stichwort
        self.standort = standort
        self.bereich = bereich
        self.seniorität = seniorität
        self.bezeichnung = bezeichnung
        self.email = email.replace("@", "%40")

    
    def fill_jobabo_form_page_1(self):
                
        last_window = self.driver.window_handles[-1]
        self.driver.switch_to.window(last_window)       
        
        #Stichwortsuche
        input_stichwortsuche = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "query"))
            )
        input_stichwortsuche.send_keys(self.stichwort)
        
        #Suche nach Chckboxen
        #TODO...fill other checkboxes
        self.send_key_to_button("ID", "Terms Checkbox", "Space")
        
        #Click button to reach next page
        self.send_key_to_button("Class", "Jobabo", "Return")

    def fill_jobabo_form_page_2(self):
        
        # Fill Bezeichnung
        input_bezeichnung = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "jobabo_bezeichnung"))
            )
        input_bezeichnung.send_keys(self.bezeichnung)
        
        # Fill e-mail
        # TODO: test for e-mail validation function as Unit-Test!
        input_email = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "jobabo_email"))
            )
        input_email.send_keys(self.email)
        
        #Click button to finish Jobabo
        #self.send_key_to_button("Class", "jobabo-subscribe-button", "Return")
        button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobabo-subscribe-button")
            ))
        
        button.submit()
        time.sleep(5)
 
    def intercept_traffic_and_validate_result(self):
    
        # If e-mail contained "%40" itself, the test would cause false negative.
        
        #print(self.email)
        request = self.driver.requests[-1]  
        req_string = None
        req_string = request.body.decode()
        print(req_string)
        if req_string.find("query="+self.stichwort) > -1 and req_string.find("jobabo_bezeichnung="+self.bezeichnung) > -1 and req_string.find("jobabo_email="+self.email) > -1:
            return True
        else: return False
         

    

# Ti8m=Ti8MLibrary()
# Ti8m.connect('C:\Program Files (x86)\geckodriver.exe', 'https://www.ti8m.com/de/career')
# Ti8m.load_and_switch_to_iframe()
# # Ti8m.start_timer()
# # Ti8m.search_in_field('Machine Python Senior')
# # Ti8m.search_in_seniority("Senior")
# #time.sleep(5)
# # Ti8m.list_job_results()
# # Ti8m.list_job_results_with_timeout(0.5)
# # print(Ti8m.get_list_of_job_results())
# # Ti8m.stop_timer()
# # print(Ti8m.get_size_of_job_results() == 1)
# # print(Ti8m.get_timer())
# # Ti8m.click_link_of_job_result("Professional Python Engineer")
# # print(Ti8m.get_job_result_text(0))
# Ti8m.send_key_to_button("ID", "Jobabo", "Return")
# Ti8m.input_jobabo_form_data("Python", "Zürich", "Engineering", "Senior", "Header", "fzoltan88@gmail.com")
# Ti8m.fill_jobabo_form_page_1()
# Ti8m.fill_jobabo_form_page_2()
# print(Ti8m.intercept_traffic_and_validate_result())

# Ti8m.disconnect_webdriver()
