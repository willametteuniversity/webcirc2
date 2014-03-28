from os.path import abspath, dirname
import sys
project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest

# Import all of our views for testing
from website.views import *

# Same for models
from website.models import *

class InventoryItemFormTests(TestCase):
	def test_add_inventory_item_url_resolves_to_new_inventory_item_view(self):
		found = resolve(u'/addNewInventoryItemForm/')
		self.assertEqual(found.func, addNewInventoryItemForm)

	def test_new_inventory_item_button_returns_correct_form(self):
		request = HttpRequest()
		response = addNewInventoryItemForm(request)
		# Making sure the form title is there, and that it at least has all
		# proper input fields and submit button.
		self.assertIn(u'Add New Inventory Item', response.content)
		self.assertIn(u'brandInput', response.content)
		self.assertIn(u'modelInput', response.content)
		self.assertIn(u'descriptionInput', response.content)
		self.assertIn(u'notesInput', response.content)
		self.assertIn(u'categoryInput', response.content)
		self.assertIn(u'statsSelect', response.content)
		self.assertIn(u'storageLocationSelect', response.content)
		self.assertIn(u'collectionInput', response.content)
		self.assertIn(u'submitInventoryItembtn', response.content)

	def test_add_inventory_item(self):
		'''
		This runs some related tests in sequence because we need the created user from the first
		function to be in the database to test the subsequent functions.
		'''
		self.submit_creates_new_inventory_item()

	def submit_creates_new_inventory_item(self):
		c = Client()

		category = Label.objects.create()
		category.LabelName = "test category"

		brand = ItemBrand.objects.create()
		brand.BrandName = "Test, a family company"

		model = ItemModel.objects.create()
		model.ModelDesignation = "test model"

		status = Status.objects.create()
		status.StatusDescription = "Status1"

		building = Building.objects.create(BuildingCode=1);

		location = Location.objects.create(BuildingID=building);

		response = c.post(u'/addNewInventoryItemForm/', {u'model': model.pk,
												 u'brand': brand.pk,
												 u'description': u'Test1',
												 u'category': category.pk,
												 u'status' : status.pk,
												 u'location' : location.pk})

		testItem = InventoryItem.objects.get(ModelID=model, BrandID=brand, Description=u'Test1', CategoryID=category, StatusID=status, StorageLocation=location)

		self.assertEqual(testItem.ModelID, model.pk)

		self.assertIn(u'succeeded', response.content)