__author__ = 'fhaynes'

from os.path import abspath, dirname
import sys

project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from website.views import reservationViews
from website.models import *
from datetime import datetime, timedelta
from django.test.client import RequestFactory

class SchedulingTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        generic_user = User.objects.create(pk=1, username='Test User 1')
        delivery_action_type = ActionType.objects.create(pk=1, ActionTypeName="Delivery")
        pickup_action_type = ActionType.objects.create(pk=2, ActionTypeName="Return")
        storage_location = Location.objects.create(pk=1,
                                                   BuildingID=Building.objects.create(pk=1, BuildingCode='SML', BuildingName='Smullin'),
                                                   RoomNumber="122",
                                                   LocationDescription="Smullin 122 Closet")
        delivery_location = Location.objects.create(pk=2,
                                                    BuildingID=Building.objects.create(pk=2, BuildingCode='FORD', BuildingName = 'Ford'),
                                                    RoomNumber="202",
                                                    LocationDescription="Ford Lab")


        first_reservation = Reservation.objects.create(pk=1,
                                                       CustomerID=generic_user,
                                                       OwnerID=generic_user,
                                                       CustomerPhone="",
                                                       CustomerEmail="",
                                                       CustomerDept="",
                                                       CustomerStatus="",
                                                       ReservationNotes="",
                                                       EventTitle="")

        start = datetime.now() + timedelta(days=1)
        end = datetime.now() + timedelta(days=1, hours=1)

        first_action = Action.objects.create(ActionID=1,
                                             AssignedOperatorID=generic_user,
                                             ActionTypeID=delivery_action_type,
                                             StartTime=start,
                                             EndTime=end,
                                             Origin=storage_location,
                                             Destination=delivery_location,
                                             ActionStatus="Incomplete",
                                             ActionNotes="This is action 1")
        first_action.Reservation.add(first_reservation)

        start = datetime.now() + timedelta(days=2)
        end = datetime.now() + timedelta(days=2, hours = 1)
        second_action = Action.objects.create(ActionID=2,
                                              AssignedOperatorID=generic_user,
                                              ActionTypeID=pickup_action_type,
                                              StartTime=start,
                                              EndTime=end,
                                              Origin=delivery_location,
                                              Destination=storage_location,
                                              ActionStatus="Incomplete",
                                              ActionNotes="This is action 2")
        second_action.Reservation.add(first_reservation)

        generic_category = Label.objects.create(LabelID=1,
                                                LabelName="Label",
                                                ParentCategory=None)

        generic_collection = Collection.objects.create(CollectionID=1,
                                                       CollectionName="Collection 1",
                                                       CollectionDescription="")

        generic_item_brand = ItemBrand.objects.create(BrandID=1,
                                                      BrandName="Unit test brand")

        generic_model = ItemModel.objects.create(ModelID=1,
                                                 ModelDesignation="Unit test model")

        generic_status = Status.objects.create(StatusID=1,
                                               StatusDescription="Unit test")

        InventoryItem.objects.create(ItemID=1,
                                     Description="Item 1",
                                     CategoryID=generic_category,
                                     StorageLocation=storage_location,
                                     CollectionID=generic_collection,
                                     Notes="Created by unit test",
                                     AlternateID=None,
                                     BrandID=generic_item_brand,
                                     ModelID=generic_model,
                                     ParentItem=None,
                                     StatusID=generic_status)

        InventoryItem.objects.create(ItemID=2,
                                     Description="Item 2",
                                     CategoryID=generic_category,
                                     StorageLocation=storage_location,
                                     CollectionID=generic_collection,
                                     Notes="Created by unit test",
                                     AlternateID=None,
                                     BrandID=generic_item_brand,
                                     ModelID=generic_model,
                                     ParentItem=None,
                                     StatusID=generic_status)


    def test_simple_scheduling(self):
        start = datetime.now() + timedelta(days=3)
        end = datetime.now() + timedelta(days=3, hours=1)
        res = Reservation.objects.create(pk=2,
                                         CustomerID=User.objects.get(pk=1),
                                         OwnerID=User.objects.get(pk=1),
                                         CustomerPhone="",
                                         CustomerEmail="",
                                         CustomerDept="",
                                         CustomerStatus="",
                                         ReservationNotes="",
                                         EventTitle="Second Test Reservation")

        start = datetime.now() + timedelta(days=3)
        end = datetime.now() + timedelta(days=3, hours=1)
        a1 = Action.objects.create(ActionID=3,
                                   AssignedOperatorID=User.objects.get(pk=1),
                                   ActionTypeID=ActionType.objects.get(pk=1),
                                   StartTime=start,
                                   EndTime=end,
                                   Origin=Location.objects.get(pk=1),
                                   Destination=Location.objects.get(pk=2),
                                   ActionStatus="Incomplete",
                                   ActionNotes="This is action 1")
        a1.Reservation.add(res)

        start = datetime.now() + timedelta(days=4)
        end = datetime.now() + timedelta(days=4, hours=1)
        a2 = Action.objects.create(ActionID=4,
                                   AssignedOperatorID=User.objects.get(pk=1),
                                   ActionTypeID=ActionType.objects.get(pk=2),
                                   StartTime=start,
                                   EndTime=end,
                                   Origin=Location.objects.get(pk=2),
                                   Destination=Location.objects.get(pk=1),
                                   ActionStatus="Incomplete",
                                   ActionNotes="This is action 1")
        a2.Reservation.add(res)

        request = self.factory.get('/findAvailableEquipment/?actions[]=3,4&categoryid=1')
        response = reservationViews.findAvailableEquipment(request)
        self.assertEqual(1, 1)




