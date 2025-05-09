from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

'''
The idea is:

1. Open Link: Success
2. Find booking buttons
    - Options:
        1. We can find the buttons via calendly / cal / etc in href
            - Pros: We can gaurantee that the links will be links to booking sites
            - Cons: The tests only work for booking services that we support  
                    i.e. if some used other-booking-site.com, that we dont support
        2. Check for words like "Book" or "Consultation" in divs
            - Cons: potential false positives
        3. Crawl entire website
            - won't miss out on any booking links
            - Cons: slow, complex

3. Test the pressing
4. Receive failure or confirmation
5. Test the booking
6. Receive failure or confirmation
7. Return Diagnostics
'''

def find_links(driver):
    '''
    For now we will only support calendly and cal links

    TODO: support other booking programs
    '''

    try:
        return driver.find_elements(By.CSS_SELECTOR, "a[href*='calendly.com'], a[href*='cal.com']")
    except Exception as e:
        print(f"Error finding Calendly link: {e}")
        return None
    

def read_links(links: list) -> list[str]:
    '''
    For debugging purposes
    '''
    read_links = []
    for link in links:
        read_links.append(link.get_attribute('href'))
    return read_links


def test_calendly_booking_link(driver) -> dict:
    '''
    Check if the booking link works, currently only works for calendly
    '''
    results = {
        'demo_link_works': False,
        'booking_flow': False,
        'booking_completed': False,
        'errors': [],
        'insights': {}
    }
    
    # Validate that the booking page loaded successfully
    try:
        current_url = driver.current_url
        if 'calendly.com' in current_url:
            results['demo_link_works'] = True
            results['insights']['booking_url'] = current_url
        else:
            raise Exception("Booking link is invalid")
    except Exception as e:
        results['errors'].append(f"Error validating booking page: {str(e)}")
        return results

    sample_user = {
            'name': 'Test User',
            'email': 'testuser@example.com',
        }
    
    try:
        day_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(@aria-label, 'Times available')]")
            )
        )
        day_button.click()

        time_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@data-container='time-button']")
                )
            )
        time_button.click()

        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(@aria-label, 'Next')]")
            )
        )
        next_button.click()

        name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@autocomplete='name']")
            )
        )
        name_input.send_keys(sample_user['name'])


        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@autocomplete='email']")
            )
        )
        email_input.send_keys(sample_user['email'])
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit' and .//span[contains(text(),'Schedule Event')]]")
            )
        ).click()
        results['booking_flow'] = True
    except Exception as e:
        results['errors'].append(f"Error booking an appointment: {str(e)}")
        return results
    
    try:
        confirmation_message = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'You are scheduled')]")
            )
        )

        details_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@data-container='details']")
            )
        )
        
        # Capture all the visible text within the details div
        all_text = details_div.text
        results["insights"]['Booking Details'] = all_text

        results['booking_completed'] = True
    except Exception as e:
        results['errors'].append(f"Could not confirmation booking: {str(e)}")
        results['confirmation'] = False

    return results


def test_cal_booking_link(driver):
    results = {
            'demo_link_works': False,
            'booking_flow': False,
            'booking_completed': False,
            'errors': [],
            'insights': {}
        }
    try:
        current_url = driver.current_url
        if 'cal.com' in current_url:
            results['demo_link_works'] = True
            results['insights']['booking_url'] = current_url
        else:
            raise Exception("Booking link is invalid")
    except Exception as e:
        results['errors'].append(f"Error validating booking page: {str(e)}")
        return results

    sample_user = {
            'name': 'Test User',
            'email': 'testuser@example.com',
        }
    
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@data-testid='time']")
                )
        ).click()
        
        name_input= WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        )
        name_input.send_keys(sample_user['name'])
        email_input= WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys(sample_user['email'])

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit']")
            )
        ).click()

    except Exception as e:
        results['errors'].append(f"Error booking an appointment: {str(e)}")
        return results
    
    try:
        confirmation_message = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'scheduled')]")
            )
        )

        details_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'grid') and contains(@class, 'border-t')]"))
        )
    
        what = details_container.find_element(By.XPATH, ".//div[@data-testid='booking-title']").text
        
        when = details_container.find_element(By.XPATH, ".//div[text()='When']/following-sibling::div[1]").text
        
        who = details_container.find_element(By.XPATH, ".//div[text()='Who']/following-sibling::div[1]").text
            
        all_text = what + "\n" + when + "\n" + who
        results["insights"]['Booking Details'] = all_text

        results['booking_completed'] = True
    except Exception as e:
        results['errors'].append(f"Could not confirmation booking: {str(e)}")
        results['confirmation'] = False

    return results


def transform_results(results: dict) -> dict:
    '''
    transforms the result of each test into a more pretty and user friendly format.
    '''
    transformed_results = {
        "Testing Booking Link Works": "Success ✅" if results.get('demo_link_works', False) else "Failed",
        "Testing Booking Flow Works": "Success ✅" if results.get('booking_flow', False) else "Failed",
        "Testing Booking Confirmaton": "Success ✅" if results.get('booking_completed', False) else "Failed",
        "Errors": "None" if not results.get('errors', False) else[],
        "Insights": results.get('insights', [])
    }
    return transformed_results

def run_test(url: str) -> dict:
    results = {
        'demo_button_found': False,
        'test_results': {},
        'errors': []
    }

    driver = webdriver.Chrome()

    driver.get(url)

    # elements = find_links(driver=driver)

    links = read_links(find_links(driver=driver))
    if len(links): 
        results['Demo Button Found'] = True
    

    for link in links:
        try:
            driver.get(link)
            if 'calendly.com' in link:
                link_result = test_calendly_booking_link(driver)
            elif 'cal.com' in link:
                link_result = test_cal_booking_link(driver)
            else:
                link_result = {"errors": [f"Unsupported booking platform in link: {link}"]}

            # link_result = transform_results(test_booking_link(driver))
            results['test_results'][link] =  transform_results(link_result)
        except Exception as e:
            results['errors'].append(f"'Book a Demo' button not found: {str(e)}")
            return results

    time.sleep(2)

    driver.close()

    return results

# Example usage
if __name__ == "__main__":
    print(run_test("https://sample-booking-site.vercel.app"))
