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
        2. Check for words like "Book" or "Consultation" in divs
            - Cons: potential false positives
        3. Crawl entire website
            - won't miss out on any booking links
            - Cons: slow

3. Test the pressing
4. Receive failure or confirmation
5. Test the booking
6. Receive failure or confirmation
7. Return Diagnostics
'''

def find_links(driver):
    '''
    For now we will only support calendly links

    TODO: support other booking programs
    '''
    try:
        calendly_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='calendly.com']")
        return calendly_links
    except Exception as e:
        print(f"Error finding Calendly link: {e}")
        return None



def _read_links(links: list):
    '''
    For debugging purposes
    '''
    read_links = []
    for link in links:
        read_links.append(link.get_attribute('href'))
    return read_links



def test_booking_link(booking_link, driver) -> dict:
    results = {
        'demo_button_found': False,
        'demo_link_works': False,
        'booking_completed': False,
        'errors': [],
        'insights': {}
    }

    try:
        booking_link.click()
        results['demo_button_found'] = True
    except Exception as e:
        results['errors'].append(f"'Book a Demo' button not found: {str(e)}")
        return results
    
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
        # Wait for and validate the confirmation message
    except Exception as e:
        results['errors'].append(f"Error booking an appointment: {str(e)}")
        return results
    
    try:
        confirmation_message = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'You are scheduled')]")
            )
        )

        results['booking_completed'] = True
    except Exception as e:
        results['errors'].append(f"Could not confirmation booking: {str(e)}")
        results['confirmation'] = False

    return results

def run_test(url):
    results = []

    driver = webdriver.Chrome()

    driver.get(url)

    elements = find_links(driver=driver)

    for element in elements:
        results.append(test_booking_link(element, driver))

    time.sleep(5)

    driver.close()

    return results

# Example usage
if __name__ == "__main__":
    print(run_test("https://sample-booking-site.vercel.app"))
