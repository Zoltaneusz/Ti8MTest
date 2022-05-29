*** Settings ***
Documentation     A test suite for valid login.
...
...               Keywords are imported from the resource file
Resource          keywords.resource
Default Tags      positive
Test Teardown     Disconnect Webdriver


*** Variables ***
@{EXPECTED_JOBS}    Software Engineer mit Flair für Machine Learning    Data Architect mit einem Flair für AI    Cloud Data Architect mit Flair für AI

*** Test Cases ***
TC1 Behaviour Driven Scenario
	Given Connected To Website
	When The User Scrolls To Search
	And Inputs The Word(s) Machine
	And Selects Seniority Senior
	Then The Job Result Should Be Cloud Data Architect mit Flair für AI
	

TC2 Behaviour Driven Performance Test
	Given Connected To Website
	When The User Scrolls To Search
	And Inputs The Word(s) Machine Test Engineering Python
	Then The Time Should Take Maximum 20
	
	

TC3 Verify Location Consistency
    Connect to Website
	Search Keyword in Joblist    Düsseldorf
	Verify Result Location    Düsseldorf

	

TC4 Search in Field and Click Link
    Connect to Website
	Search Keyword in Joblist    Machine
	Verify Result    @{EXPECTED_JOBS}
	Click Links
	


	

	
	
