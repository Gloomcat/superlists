from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.template.context_processors import csrf
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		
		context = csrf(request)

		expected_html = render_to_string('home.html', context)
		self.assertEqual(response.content.decode(), expected_html)


class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		
		self.assertRedirects(response, '/lists/5/')


class ListViewTest(TestCase):
	def test_uses_list_template(self):
		response = self.client.get('/lists/5/')
		self.assertTemplateUsed(response, 'list.html')

	def test_display_all_items(self):
		list_ = List.objects.create()
		first_item = Item.objects.create(text='itemey1', list=list_)
		second_item = Item.objects.create(text='itemey2', list=list_)

		response = self.client.get('/lists/5/')

		self.assertContains(response, 'itemey1')
		self.assertContains(response, 'itemey2')


class ListAndItemModelsTest(TestCase):
	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]

		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.list, list_)
