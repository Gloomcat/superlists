from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):
	def test_can_start_a_list_and_retrieve_it_later(self):
		# Edith has heard about a cool new online to-do app. She goes
		# to check out its homepage
		self.browser.get(self.server_url)

		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# She is invited to enter a to-do item straight away
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			input_box.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		self.assertAlmostEqual(
			input_box.location['x'] + input_box.size['width'] / 2,
			480,
			delta=5
		)

		# She types "Buy peacock feathers" into a text box (Edith's hobby
		# is tying fly-fishing lures)
		input_box.send_keys('Buy peacock feathers')
		input_box.send_keys(Keys.ENTER)

		# When she hits enter, she is taken to a new URL,
		# and now the page lists "1: Buy peacock feathers" as an item in a
		# to-do list table
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/\d+')

		# There is still a text box inviting her to add another item. She
		# enters "Use peacock feathers to make a fly" (Edith is very methodical)
		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Use peacock feathers to make a fly')
		input_box.send_keys(Keys.ENTER)

		# The page updates again, and now shows both items on her list
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

		# Now a new user, Francis, comes along to the site.
		## We use a new browser session to make sure that no information
		## of Edith's is coming through from cookies etc
		self.browser.quit()
		self.browser = webdriver.Chrome()

		# Francis visits the home page. There is no sign of Edith's
		# list
		self.browser.get(self.server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		# Francis starts a new list by entering a new item. He
		# is less interesting than Edith...
		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Buy milk')
		input_box.send_keys(Keys.ENTER)
		
		# Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/\d+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		# Again, there is no trace of Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		# Satisfied, they both go back to sleep

