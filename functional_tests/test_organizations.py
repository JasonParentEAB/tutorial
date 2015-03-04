__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Third-party imports...
from selenium.webdriver.firefox.webdriver import WebDriver

# Django imports...
from django.test import LiveServerTestCase


class OrganizationsTest(LiveServerTestCase):
    def setUp(self):
        self.browser = WebDriver()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def test_new_organizations_are_shown_in_list(self):
        # John goes to the home page.
        self.browser.get(self.live_server_url)

        # He sees an empty table with a single cell that says 'No organizations'.
        # He also sees a button labelled 'Create organization'. He clicks the create button.
        cell = self.browser.find_element_by_xpath('//table/tbody/tr/td')
        self.assertEqual(cell.text, 'No organizations')
        create_button = self.browser.find_element_by_id('create-button')
        self.assertEqual(create_button.text, 'Create organization')
        create_button.click()

        # The page refreshes and John sees a form with a single input: name.
        name_input = self.browser.find_element_by_name('name')
        self.assertEqual(name_input.get_attribute('placeholder'), 'Organization name')

        # John enters an organization name and clicks the submit button.
        name_input.send_keys('TDD Organization')
        submit_button = self.browser.find_element_by_id('submit')
        self.assertEqual(submit_button.text, 'Submit')
        submit_button.click()

        # The page refreshes and John notices that the table now has a single row with
        # the details of the organization that he added.
        row = self.browser.find_element_by_xpath('//table/tbody/tr')
        self.assertIn('TDD Organization', row.text)