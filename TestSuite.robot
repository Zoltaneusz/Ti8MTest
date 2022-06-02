*** Settings ***
Documentation     A test suite for valid login.
...
...               Keywords are imported from the resource file
Resource          keywords.resource
Default Tags      positive
Test Teardown     Disconnect Webdriver


*** Variables ***
@{EXPECTED_JOBS}    Software Engineer mit Flair für Machine Learning    Data Architect mit einem Flair für AI    Cloud Data Architect mit Flair für AI
@{FORM_DATA}    Python Zürich Engineering Senior Header fzoltan88@gmail.com
@{WORDS}    Machine Test Engineering Python

*** Test Cases ***
TC1 Behaviour Driven Scenario With Two Filters
	[Tags]    skip
	Given Connected To Website With Search Mocking For    TC1    Firefox
	When The User Scrolls To Search
	And Inputs The Word(s)    Machine
	And Selects Seniority Senior
	Then The Job Result Should Be Cloud Data Architect mit Flair für AI
	

TC2 Behaviour Driven Performance Test
	[Tags]    skip
	Given Connected To Website With    Firefox
	When The User Scrolls To Search
	And Inputs The Word(s)    @{WORDS}
	Then The Time Should Take Maximum 5
	
TC3 Verify Location Consistency
	[Tags]    skip
    Connect to Website With    Firefox
	Search Keyword in Joblist    Düsseldorf
	Verify Result Location    Düsseldorf

TC4 Scenario Job Subscription
	[Tags]    skip
	Connect to Website With    Firefox
	Fill Job Subscription With    @{FORM_DATA}

TC5 Scenario Search in Field and Click Links
    [Tags]    run
	Connect to Website With Search Mocking For    TC5    Firefox
	Search Keyword in Joblist    Machine
	Verify Result    @{EXPECTED_JOBS}
	Click Links
	Disconnect
	Connect to Website With Search Mocking For    TC5    Chrome
	Search Keyword in Joblist    Machine
	Verify Result    @{EXPECTED_JOBS}
	Click Links
	Disconnect
	Connect to Website With Search Mocking For    TC5    Edge
	Search Keyword in Joblist    Machine
	Verify Result    @{EXPECTED_JOBS}
	Click Links
