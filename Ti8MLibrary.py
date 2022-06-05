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
        self.seniority_array = [["Junior", "Professional", "Senior", "Default"],
                                ["1301737", "1301738", "1301739", ""]]
        self.stichwort = None
        self.standort = None
        self.bereich = None
        self.seniorität = None
        self.bezeichnung = None
        self.email = None
        self.mock_html_path = ''
        self.search_length = 1
        
# Functions regarding connection-----------------------------
    def connect(self, url : str, browser : str) -> None:
        """
        
        Parameters
        ----------
        url : str
            URL of the webpage to be tested.
        browser : str
            The browser to be used for the tests, e.g. "Firefox"

        Returns
        -------
        None.

        """
        if browser.find("Firefox") > -1: b = webdriver.Firefox()
        elif browser.find("Chrome") > -1: b = webdriver.Chrome()
        elif browser.find("Edge") > -1: 
            options = {
            'port': 12345
            }
            b = webdriver.Edge(seleniumwire_options=options)
        self.driver = b
        self.driver.get(url)

    def connect_with_interceptor(self, url : str, test_case_nr : str, browser : str) -> None:
        """
        Connects webdriver to the chosen website in the chosen browser. 
        Sets path of the html used for mocking in the job search, depending on the test case.

        Parameters
        ----------
        url : str
            URL of the webpage to be tested..
        test_case_nr : str
            Number of the test case calling this function.
        browser : str
            The browser to be used for the tests, e.g. "Firefox".

        Returns
        -------
        None.

        """
        
        b = None
        if browser.find("Firefox"): b = webdriver.Firefox()
        elif browser.find("Chrome") : b = webdriver.Chrome()
        elif browser.find("Edge"):
            options = {
            'port': 12345
            }
            b = webdriver.Edge(seleniumwire_options=options)
     
        
        self.set_mock_html_path(test_case_nr)
        self.driver = b
        self.driver.request_interceptor = self.interceptor
        self.driver.get(url)
        
    def disconnect_webdriver(self) -> None:
        """
        Disconnect webdriver.

        Returns
        -------
        None
            DESCRIPTION.

        """
        self.driver.quit()
        
    def allow_cookies(self) -> None:
        """
        Allows all cookies.

        Returns
        -------
        None
            DESCRIPTION.

        """
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "cc-allow"))).click()
        
    
# Functions job search-----------------------------   
    
    def load_and_switch_to_iframe(self) -> None:
        """
        Scrolls to iframe that contains the job list.

        Returns
        -------
        None.

        """
      #Function navigates to search field 
      
        self.search_iframe = self.driver.find_element(By.CLASS_NAME, "ti8m-iframe")
        
        desired_y = (self.search_iframe.size['height'] / 2) + self.search_iframe.location['y'] + 100
        current_y = (self.driver.execute_script('return window.innerHeight') / 2) + self.driver.execute_script('return window.pageYOffset')
        scroll_y_by = desired_y - current_y
        self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        time.sleep(4)
        self.first_tab = self.driver.current_window_handle
        self.driver.switch_to.frame(self.search_iframe)
        # print(self.driver.current_window_handle)

    
    def search_in_field(self, keyword : str) -> None:
        """
        Search for keyword in job list.

        Parameters
        ----------
        keyword : str
            Word to search for.

        Returns
        -------
        None.

        """
        search = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.NAME, "query")))
        #search = self.driver.find_element(By.NAME, "query")
        search.send_keys(keyword)
        self.search_length = len(keyword)
        # self.search_request = self.driver.wait_for_request('/?lang=de')
        # print(self.search_request.url)
        #search.send_keys(Keys.RETURN)
        time.sleep(1)
        
    def search_in_seniority(self, seniority : str) -> None:
        """
        Checks the checkbox chosen by seniority for the joblist search.

        Parameters
        ----------
        seniority : str
            E.g. "Junior", "Professional", "Senior"

        Returns
        -------
        None.

        """
        # script = "return window.getComputedStyle(document.querySelector('div>input.1301739'),':before').getPropertyValue('text')"
        # self.driver.execute_script(script).strip()
        
        index = self.seniority_array[0].index(seniority)
        # print(self.seniority_array[1][index])
        check = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, self.seniority_array[1][index])))
            # EC.presence_of_element_located((By.ID, "1301737")))
        #check = self.driver.find_element(By.ID, self.seniority_array[1][index])
        check.send_keys(Keys.SPACE)
        time.sleep(1)
    
    
    def list_job_results(self) -> None:
        """
        Waits for joblist to be active and saves the webelement.

        Returns
        -------
        None.

        """
        # print(self.driver.current_window_handle)
        try:
            self.job_list = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "jobs"))
                )
          
            self.job_results = self.job_list.find_elements(By.TAG_NAME, "a")
            
            # print(len(self.job_list))

        except:  
            print("Fail")
            self.driver.quit()
    
    def list_job_results_with_timeout(self, timeout : int):
        
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
    
    # def response_active():
        
    #     def _predicate(driver):
    #         response = driver.last_response
    #         if driver.last.response:
    #             return response
    #         else: 
    #             return False
    #     return _predicate
    
    def find_last_search_request_index(self, driver) -> None:
        """
        Searches the last network request responses have status 200 or 204.
        The amount of searched requests is equal to the number of letters in the search
        or 1 if checkbox search has been initiated by the user. 
        The reason for this is that the search is triggered after every letter in the search field.
        
        Parameters
        ----------
        driver : Webdriver
            Webdriver instance to iterate through.

        Returns
        -------
        bool
            True if all searched network responses have either status 200 or 204.

        """
        # last_req = None
        # i=0
        # ind = 0
        # for req in driver.requests[len(driver.requests)-4:]:
        #     i=i+1
        #     print(req.host)
        #     if req.host.find("ti8m"):
        #         last_req = req
        #         ind = i

        # print(ind)
        # # print(last_req.host)
        # return (len(driver.requests)-4+ind)
        all_responses_arrived = True
        # There are at least as many requests as letters in the search field
        for req in driver.requests[len(driver.requests)-self.search_length:]:
            if req.response.status_code != 200 and req.response.status_code != 204:
                all_responses_arrived = False
                print(req.response.status_code)
             
        return all_responses_arrived
        
    
    def wait_for_joblist(self) -> None:
        """
        Waits until last 10 network requests responses have status code 200.
        Only requests on the ti8m domain are checked for status code.
        Returns
        -------
        None
            DESCRIPTION.

        """
      
        # If google analytics is the last response and faster than the search resp., it is not working
        wait = WebDriverWait(self.driver, timeout=40, poll_frequency=2, ignored_exceptions=[AttributeError])
        # done = wait.until(lambda x: x.last_request.response.status_code == 200)
        # done = wait.until(lambda x: self.find_last_search_request_index(x) and
        #                   x.last_request.response.status_code == 200) 
        # done = wait.until(lambda x: x.requests[self.find_last_search_request_index(x)].response.status_code == 200) 
        # done = wait.until(lambda x: self.search_request.response.status_code == 200)
        done = wait.until(lambda x: self.find_last_search_request_index(x)) 
        
        # done = wait.until(lambda x : last_req.response.status_code == 200)
                        
            
        
        print("Status: ")
        print(done)
       
                
    
    def get_list_of_job_results(self) -> list:
        """
        Reads the saved webelement containing the job results and returns their titles in a list.
        Returns
        -------
        list(str)
            List of titles of found job results.

        """

        job_result_texts= []
        for job in self.job_results:
            # print(job.text)
            job_result_texts.append(job.text)
        return job_result_texts
    
    def get_job_result_text(self, ind : int) -> str:
        """
        Get the title of saved job result at index ind.

        Parameters
        ----------
        ind : int
            Index of job result in the list of job results.

        Returns
        -------
        str
            Title of saved job result.

        """
        return self.job_results[int(ind)].text
    
    def get_size_of_job_results(self) -> int:
        """
        Get number of job results.

        Returns
        -------
        int
            Nr. of job results.

        """
        #return sum(1 for _ in self.job_results)
        #return len(list(self.job_results_iter))
        return str(len(self.job_results))
    
    def click_link_of_job_result(self, link : str) -> None:
        """
        Click on the job result with title 'link'.

        Parameters
        ----------
        link : str
            Title of job result to be clicked.

        Returns
        -------
        None
            DESCRIPTION.

        """
        #self.driver.switch_to.window(self.first_tab)
        #time.sleep(5)
        job_link = self.job_list.find_element(By.LINK_TEXT, link)
        job_link.click()
        time.sleep(2)
        self.driver.switch_to.window(self.first_tab)
        self.driver.switch_to.frame(self.search_iframe)
        
        time.sleep(2)
    
    def get_job_result_location(self) -> str:
        """
        Returns the 'location' of the found job result.
        Works only the there is only one found job!!
        TODO: extend functionality for more than one jobs.

        Returns
        -------
        str
            Location of job result.

        """
        found_location = self.job_list.find_element(By.CLASS_NAME, "location")
        return found_location.text
    


#Functions for Timer Functionality---------------

    def start_timer(self) -> None:
        """
        Saves current time to variable.

        Returns
        -------
        None
            DESCRIPTION.

        """
        self.elapsed_time = time.perf_counter()
        
    def stop_timer(self) -> None:
        """
        Saves time elapsed since calling "start_timer" to variabe.

        Returns
        -------
        None
            DESCRIPTION.

        """
        self.elapsed_time = time.perf_counter()-self.elapsed_time
        
    def get_timer(self) -> int:
        """
        Returns time measured between "start_timer" and "stop_timer"

        Returns
        -------
        int
            Time measured between "start_timer" and "stop_timer"

        """
        return self.elapsed_time
    
    
#Functions for Finding Webelement---------------   
    
    def send_key_to_button(self,btn_name : str, key : str) -> None:
        """
        Find webelement 'btn_name' and click on it. Click is realized either with pressing Return or Space.

        Parameters
        ----------
        search_param : str
            Search mode for webelement. E.g 'ID' or 'Class'.
        btn : str
            E.g "Jobabo", "Terms Checkbox".
        key : str
            Key to press to realize click action. E.g "Return" or "Space".

        Returns
        -------
        None
            DESCRIPTION.

        """
        # if search_param == "ID":
        #     by = By.ID
        # elif search_param == "Class":
        #     by = By.CLASS_NAME
            
        if key == "Return":
            pressed_key = Keys.RETURN
        elif key == "Space":
            pressed_key = Keys.SPACE
         
        button = self.job_list = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((self.web_element_finder(btn_name))
            ))
        button.send_keys(pressed_key)
        time.sleep(3)

    def web_element_finder(self, input_elem : str) -> tuple:
        """
        Return webelement class or ID, depending on 'input_elem'.
        'input_elem' is the webelement to look for. E.g. 'ID' or 'Class'.

        Parameters
        ----------
        input_elem : str
            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        """
        if input_elem == "Jobabo":
            return (By.CLASS_NAME, "jobabo-subscribe-button")
        elif input_elem == "Terms Checkbox":
            return (By.ID, "single-opt-in")
        else: return "NaN"

#Functions for Jobabo Test---------------

    def input_jobabo_form_data(self, args) -> None:
        """
        

        Parameters
        ----------
        args : list <str>
            args[0] : word to look for.
            args[1] : location to look for.
            args[2] : area to look for.
            args[3] : seniority level to look for.
            args[4] : title of e-mail.
            args[5] : e-mail address of recipient.

        Returns
        -------
        None
            DESCRIPTION.

        """
        
        self.stichwort = args[0]
        self.standort = args[1]
        self.bereich = args[2]
        self.seniorität = args[3]
        self.bezeichnung = args[4]
        self.email = args[5]

    
    def fill_jobabo_form_page_1(self) -> None:
        """
        Fills the first page of the jobabo form with the values defined
        in function 'input_jobabo_form_data'

        Returns
        -------
        None
            DESCRIPTION.

        """
                
        last_window = self.driver.window_handles[-1]
        self.driver.switch_to.window(last_window)       
        
        #Stichwortsuche
        input_stichwortsuche = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "query"))
            )
        input_stichwortsuche.send_keys(self.stichwort)
        
        #Suche nach Chckboxen
        #TODO...fill other checkboxes
        self.send_key_to_button("Terms Checkbox", "Space")
        
        #Click button to reach next page
        self.send_key_to_button("Jobabo", "Return")

    def fill_jobabo_form_page_2(self) -> None:
        """
        Fills the second page of the jobabo form with the values defined
        in function 'input_jobabo_form_data'

        Returns
        -------
        None
            DESCRIPTION.

        """
        
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
 
    def intercept_email_and_validate_result(self) -> None:
        """
        Intercepts network request sent out after calling function
        'fill_jobabo_form_page_2' and validates it's contents with the data filled
        in function 'input_jobabo_form_data'.

        Returns
        -------
        None
            DESCRIPTION.

        """
    # Chrome network response is not the last element in the "requests" list
    # Chrome response is also not always at the same index. It varies in the last 4 indexes
    # Therefore iteration is used. Solution also works for Firefox, where the respons is always at the last index.
        
        # If e-mail contained "%40" itself, the test would cause false negative.
        self.email = self.email.replace("@", "%40")
        #print(self.email)
        req_string = None
        # request = self.driver.requests[-1]  

        
        # for req in self.driver.requests[len(self.driver.requests)-50:]:
        for req in self.driver.requests:
            # print(req)
            req_string = req.body.decode()
            if req_string.find("query="+self.stichwort) > -1:
                print(req_string)
                if req_string.find("query="+self.stichwort) > -1 and req_string.find("jobabo_bezeichnung="+self.bezeichnung) > -1 and req_string.find("jobabo_email="+self.email) > -1:
                    return "True"
                else: return "False"
         
# Mock Network Response With Predefined HTML-----------
    def interceptor(self, request) -> None:
        """
        Intercepts outgoing search request and mocks the answer with
        defined html. The html is defined with function 'set_mock_html_path'.

        Parameters
        ----------
        request : TYPE
            DESCRIPTION.

        Returns
        -------
        None
            DESCRIPTION.

        """
        
        f = open(self.mock_html_path, "r", encoding='utf-8')
        interceptor_html_response = f.read()      
        f.close()
        
        if request.url == "https://career.ti8m.com/?lang=de":
            request.create_response(
                status_code = 200,
                headers={'Content-Type': 'text/html'},
                body=interceptor_html_response)
    
    def set_mock_html_path(self, test_case_nr : str) -> None:
        """
        Sets the path for the html which is used for mocking network request
        depending on 'test_case_nr'

        Parameters
        ----------
        test_case_nr : str
        Test_case_nr must be in format "TCX", where X:1,2,...,n
            E.g. "TC1", "TC5"

        Returns
        -------
        None
            DESCRIPTION.

        """
        self.mock_html_path = test_case_nr + " Network Request Mock.txt"

Ti8m=Ti8MLibrary()
# Ti8m.connect_with_interceptor('https://www.ti8m.com/de/career', 'TC5')
Ti8m.connect('https://www.ti8m.com/de/career', 'Edge')
Ti8m.load_and_switch_to_iframe()
Ti8m.start_timer()
Ti8m.search_in_field("Machine Cloud")
# Ti8m.search_in_seniority("Junior")
# time.sleep(10)
Ti8m.wait_for_joblist()
Ti8m.stop_timer()
print(Ti8m.get_timer())
# time.sleep(5)
Ti8m.list_job_results()
# Ti8m.list_job_results_with_timeout(0.5)
print(Ti8m.get_list_of_job_results())

print(Ti8m.get_size_of_job_results())
# print(Ti8m.get_timer())
# Ti8m.click_link_of_job_result("Professional Python Engineer")
# print(Ti8m.get_job_result_text(0))
# Ti8m.send_key_to_button("Jobabo", "Return")
# Ti8m.input_jobabo_form_data(["Python", "Zürich", "Engineering", "Senior", "Header", "fzoltan88@gmail.com"])
# Ti8m.fill_jobabo_form_page_1()
# Ti8m.fill_jobabo_form_page_2()
# print(Ti8m.intercept_email_and_validate_result())
Ti8m.disconnect_webdriver()
