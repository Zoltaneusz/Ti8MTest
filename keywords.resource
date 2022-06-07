*** Settings ***
Documentation     This is a resource file, that can contain variables and keywords.
...               Keywords defined here can be used where this Keywords.resource in loaded.
Library           Ti8MLibrary.py


*** Variables ***
${multi_use_var}

*** Keywords ***
Connect to Website With Search Mocking For
	[Arguments]    ${Testcasenr}    ${Browser}
    Connect With Interceptor    https://www.ti8m.com/de/career    ${Testcasenr}    ${Browser}

Connect to Website With
	[Arguments]    ${Browser}
    Connect    https://www.ti8m.com/de/career    ${Browser}
	Allow Cookies	
	
Search Keyword in Joblist
    [Arguments]    ${Keyword}
    Load and switch to iframe
	Search in field    ${Keyword}
	
Verify Result
    [Arguments]    @{EXPECTED_JOBS}
	Wait for Joblist
	List Job Results
	FOR   ${index}    ${expected_job}    IN ENUMERATE    @{EXPECTED_JOBS}
	    ${found_job}=   Get Job Result Text    ${index}
		Should Be Equal    ${found_job}    ${expected_job}
    END
	
Verify Result Location
    [Arguments]    ${expected_location}
	Wait For Joblist
	List Job Results
	${found_location}    Get Job Result Location
	Should Be Equal    ${found_location}    ${expected_location}

Click Links
	FOR   ${Link}    IN    @{EXPECTED_JOBS}
	    Click Link Of Job Result    ${Link}
		${Title}    Get Last Tab Title
		Should Be Equal    ${Title}    ${Link}
		Switch Back To Careersite
    END
	
Disconnect
	Disconnect Webdriver
	
	
Connected to Website With
	[Arguments]    ${Browser}
    Connect    https://www.ti8m.com/de/career    ${Browser}

Connected to Website With Search Mocking For
	[Arguments]    ${Testcasenr}   ${Browser}
    Connect With Interceptor    https://www.ti8m.com/de/career    ${Testcasenr}    ${Browser}
	
The User Scrolls To Search
    Load and switch to iframe
	
Inputs The Word(s)
    [Arguments]    @{WORDS}
    Search in field    @{WORDS}	

Selects Seniority
	[Arguments]    ${seniority}
	Search in seniority    ${seniority}
	
The Job Result Should Be
    [Arguments]    ${expected_job}
    List Job Results
    ${found_job}=   Get Job Result Text    0
    Should Be Equal    ${found_job}    ${expected_job}

	
The Expected Job Number Is 
    [Arguments]    ${expected_number}
	${multi_use_var}=   ${expected_number}

The Time Should Take Maximum
    [Arguments]    ${maximum_time}
    Start Timer
	Wait For Joblist
	Stop Timer
	List Job Results
	${elapsed_time}=   Get Timer
	Should Be True    ${elapsed_time}<${maximum_time}

Fill Job Subscription With
    [Arguments]    @{FORM_DATA}
	Load And Switch To Iframe
	Send Key To Button    Jobabo    Return
	Input Jobabo Form Data    @{FORM_DATA}
	Fill Jobabo Form Page 1
	Fill Jobabo Form Page 2
	${True}    Intercept Email And Validate Result
	Should Be Equal    ${True}    True
	