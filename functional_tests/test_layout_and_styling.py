from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
	def test_layout_and_styling(self):
		self.browser.get(self.server_url)
		self.browser.set_window_size(960, 768)

		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			input_box.location['x'] + input_box.size['width'] / 2,
			480,
			delta=5
		)
	
