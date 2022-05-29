*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Library           Ti8MLibrary.py


*** Variables ***
${multi_use_var}

*** Keywords ***
Connect to Website
    Connect    C:/Program Files (x86)/geckodriver.exe    https://www.ti8m.com/de/career
	Allow Cookies
	
Search Keyword in Joblist
    [Arguments]    ${Keyword}
    Load and switch to iframe
	Search in field    ${Keyword}
	
Verify Result
    [Arguments]    @{EXPECTED_JOBS}
	List Job Results
	FOR   ${index}    ${expected_job}    IN ENUMERATE    @{EXPECTED_JOBS}
	    ${found_job}=   Get Job Result Text    ${index}
		Should Be Equal    ${found_job}    ${expected_job}
    END
	
Verify Result Location
    [Arguments]    ${expected_location}
	List Job Results
	${found_location}    Get Job Result Location
	Should Be Equal    ${found_location}    ${expected_location}

Click Links
	FOR   ${Link}    IN    @{EXPECTED_JOBS}
	    Click Link Of Job Result    ${Link}
    END
	
Disconnect
	Disconnect Webdriver
	
	
Connected to Website
    Connect    C:/Program Files (x86)/geckodriver.exe    https://www.ti8m.com/de/career
	
	

The User Scrolls To Search
    Load and switch to iframe
	
Inputs The Word(s) ${keyword}
    Search in field    ${keyword}	

Selects Seniority ${seniority}
	Search in seniority    ${seniority}
	
The Job Result Should Be ${expected_job}
    List Job Results
    ${found_job}=   Get Job Result Text    0
    Should Be Equal    ${found_job}    ${expected_job}

	
The Expected Job Number Is ${expected_number}
	${multi_use_var}=   ${expected_number}

The Time Should Take Maximum ${maximum_time}
    Start Timer
	List Job Results
    ${found_number}=   Get Size Of Job Results
	Get Timer
    Should Be Equal    ${found_number}    100
	${elapsed_time}=   Stop Timer
	Should Be Equal    ${elapsed_time}    ${maximum_time}
