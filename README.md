# Ti8MTest

## Tool Installation
The testing library is written in Python using Selenium and Selenium-wire packages. High-level test cases are written with RobotFramework. Following Sub-Chapters describe how to install the tools.
Python: 3.10
Selenium: 4.1.5
Selenium-wire: 4.6.4
RobotFramework: 5.0.1

### Installing Python
As written [here](https://www.python.org/downloads/)

### Installing Selenium
Installing Selenium has 2 parts:

__Package Install__
* [Selenium Install](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/)
* TLDR: `pip install selenium`

__Webdriver Install__
* [Webdriver Install](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)


### Installing Selenium-wire
As written here: [Selenium-wire Install](https://pypi.org/project/selenium-wire/#installation)  
Install using pip: `pip install selenium-wire`

For Edge browser following configuration is also needed: [Edge Config](https://pypi.org/project/selenium-wire/0.8.0/)

### Installing RobotFramework
As written [here](https://robotframework.org/?tab=1#getting-started)

Or simply: `pip install robotframework`

## Test Usage
### File Structure
The test cases consist of three levels:
1. High level behaviour-driven or data-driven test cases are saved in ***TestSuite.robot***  
2. Middle level is defined in ***keywords.resource***
3. Lowest level is the file ***Ti8MTest.py***

Following html files may be used in the test cases to circumvent server waiting times. Test cases 1 and 5 may use these files to intercept network responses and bypassing real server data.
1. TC1 Network Request Mock.txt 
2. TC5 Network Request Mock.txt

### Running tests
Using the command line navigate to the directory containing the three main files, defined in the last chapter.
To simply run all the test cases (TC1..TC5) from ***TestSuite.robot*** use following command:  

`robot TestSuite.robot`  

To skip a test case '[Tags]    Skip' may be used as shown for test case 1.

    TC1 Behaviour Driven Scenario With Two Filters
	    [Tags]    skip
        Given Connected To Website With Search Mocking For    TC1    Firefox
	    When The User Scrolls To Search
	    And Inputs The Word(s)    Machine
	    And Selects Seniority    Senior
	    Then The Job Result Should Be    Cloud Data Architect mit Flair für AI
      
Running all test cases except TC1:

`robot --exclude skip TestSuite.robot`  

### Test Report
Following  files store the report and log. More detailed information may be found on Robot Frameworks website.
1. report.html
2. log.html
