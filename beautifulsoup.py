
########################################################################################
#############   KINDLY CHECK THE README BELOW BEFORE RUNNING THIS FILE/CODE   ##########
#############           especially, the users' infomrmations                  ##########
########################################################################################




################################    Import Statements    ######################################

#Importing necessary libraries

import requests                 # to get access
from bs4 import BeautifulSoup   # for crawling page and extract data





###############################     Constants Definition    ##################################

# Define URLs, login credentials, and creating a session for persistent cookies.

# urls
LOGIN_URL = 'https://jobs.de/en'
PAGE_URL = 'https://jobs.de/en/jobs?page=0&title=data&limit=20'

# Define login credentials
LOGIN_PAYLOAD = {
                 'username': '*******', # supply valid e-mail address
                 'password': '*******'  # supply valid password
                 }

# Create a session to persist cookies
SESSION = requests.Session()





################################    login_and_crawl Function    ##############################

def login_and_crawl(login_url, login_payload, page_url):
    """
    Log in to the website using the provided credentials and crawl the target page.

    Args:
        login_url (str): The URL of the login page.
        login_payload (dict): The login credentials.
        page_url (str): The URL of the page to crawl.

    Returns:
        soup: Parsed HTML content of the page after successful login.
        None: Returns None if login is unsuccessful.
    """

    # log in to the website with the payload_credentials (login data)

    response = SESSION.post(login_url, params=login_payload)

    # created nested arguments that requires the page to be scrapped if and only if login is successful

    if response.ok:
        print('\n                                    Login Successful:', response.status_code, response.ok) # long space for center alignment

        # If login is successful, proceed to crawl the target page
        data = SESSION.get(page_url)

        if data.ok:
            print('                            Page Crawled Succesfully and Below are the ') # long space for center alignment 

            # here, i use lxml as my data parsing, 'html.parser' is an alternative which doesnt require installation.
            soup = BeautifulSoup(data.text, 'lxml')
            return soup
        
        else:
            print('Page Not Crawled:', data.status_code, data.reason)
            return None
    else:
        print('Login Failed:', response.status_code, response.reason)
        
        return None





##################################  extract_job_details Function    ########################################
    
def extract_job_details(soup):
    """
    Extract job information from the parsed HTML.

    Args:
        soup: Parsed HTML content.

    Returns:
        tuple: Lists of job titles, companies, locations, dates, and modes.
    """
    job_title = soup.find_all('a', class_='h4') #find all job titles
    job_company = soup.find_all('a', class_='h6')   #find all company names
    job_location = soup.find_all('span', {'data-testid': 'job-location-tag'})    #find all job locations
    job_date = soup.find_all('span', {'data-testid': 'job-date-tag'})   #find all posted dates
    job_mode = soup.find_all('span', {'data-testid': 'job-occupation-type-tag'})    #find all modes of work

    return job_title, job_company, job_location, job_date, job_mode





#################################   print_job_details Function  ############################################

def print_job_details(job_title, job_company, job_location, job_date, job_mode):
    """
    Print job details.

    Args:
        job_title (list): List of job titles.
        job_company (list): List of job companies.
        job_location (list): List of job locations.
        job_date (list): List of job posted dates.
        job_mode (list): List of job modes.
    """
    print('                                     Available Jobs on JOBS.DE   ')
    

    #zip all titles, comapny, location and mode then
    #loop through to print all details from each job subsequently using for loop

    for title, company, location, date, mode in zip(job_title, job_company, job_location, job_date, job_mode):
        
        #use .text to extract only the texts from the html tags
        print(f'''
            Job Title: {title.text}
            Company: {company.text}
            Location: {location.text}
            Date Posted: {date.text}
            Job Mode: {mode.text}

            ''')





#########################################   main Function   ##################################################
        
def main():
    """
    Orchestrates the main flow of the script, including login, page crawling, and data extraction.

    Returns:
        None
    """

    # Log in and crawl the target page
    parsed_page = login_and_crawl(LOGIN_URL, LOGIN_PAYLOAD, PAGE_URL)

    # Extract and print job details
    if parsed_page:
        job_title, job_company, job_location, job_date, job_mode = extract_job_details(parsed_page)
        print_job_details(job_title, job_company, job_location, job_date, job_mode)


    #close session
    SESSION.close()





#########################################   Script Execution    #############################################
        
if __name__ == '__main__':
    main()