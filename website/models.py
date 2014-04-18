from django.db import models
from django.contrib.auth.models import User


class Label(models.Model):
    LabelID = models.AutoField(primary_key=True)
    LabelName = models.CharField(max_length=500)
    ParentCategory = models.ForeignKey(u'Label', null=True, blank=True)


class ItemLabel(models.Model):
    LabelID = models.ForeignKey(u'Label')
    ItemID = models.ForeignKey(u'InventoryItem')


class LabelNotes(models.Model):
    LabelNoteID = models.AutoField(primary_key=True)
    LabelID = models.ForeignKey(u'Label')
    LabelNote = models.CharField(max_length=500)


class LabelImage(models.Model):
    LabelID = models.ForeignKey(u'Label')
    ImageID = models.ForeignKey(u'Image')


class ItemImage(models.Model):
    ItemID = models.ForeignKey(u'InventoryItem')
    ImageID = models.ForeignKey(u'Image')


class Image(models.Model):
    ImageID = models.AutoField(primary_key=True)
    ImageName = models.CharField(max_length=500)


class Status(models.Model):
    StatusID = models.AutoField(primary_key=True)
    StatusDescription = models.CharField(max_length=500)


class InventoryItem(models.Model):
    ItemID = models.AutoField(primary_key=True)
    AlternateID = models.ForeignKey(u'InventoryWidget', blank=True, null=True)
    BrandID = models.ForeignKey(u'ItemBrand')
    ModelID = models.ForeignKey(u'ItemModel')
    Description = models.CharField(max_length=500)
    Notes = models.CharField(max_length=500, null=True, blank=True)
    CategoryID = models.ForeignKey(u'Label')
    ParentItem = models.ForeignKey(u'InventoryItem', null=True, blank=True)
    StatusID = models.ForeignKey(u'Status')
    StorageLocation = models.ForeignKey(u'Location')
    CollectionID = models.ForeignKey(u'Collection')


class NonInventoryItem(models.Model):
    ItemID = models.AutoField(primary_key=True)
    Description = models.CharField(max_length=500)
    CategoryID = models.ForeignKey(u'Label')
    StorageLocation = models.ForeignKey(u'Location')
    CollectionID = models.ForeignKey(u'Collection')
    Notes = models.CharField(max_length=500, null=True, blank=True)
    Quantity = models.IntegerField(default=0)

class ConsumableItem(models.Model):
    ItemID = models.AutoField(primary_key=True)
    ItemName = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)
    CategoryID = models.ForeignKey(u'Label')
    StorageLocation = models.ForeignKey(u'Location')
    Notes = models.CharField(max_length=500, null=True, blank=True)
    Quantity = models.IntegerField(default=0)
    # This is the quantity we want to always have on hand
    MinQuantity = models.IntegerField(default=0)
    # Cost per item
    Cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    CollectionID = models.ForeignKey(u'Collection')


class InventoryWidget(models.Model):
    InventoryID = models.AutoField(primary_key=True)


class ItemBrand(models.Model):
    BrandID = models.AutoField(primary_key=True)
    BrandName = models.CharField(max_length=500)


class ItemModel(models.Model):
    ModelID = models.AutoField(primary_key=True)
    ModelDesignation = models.CharField(max_length=500)


class Location(models.Model):
    LocationID = models.AutoField(primary_key=True)
    BuildingID = models.ForeignKey(u'Building')
    RoomNumber = models.CharField(max_length=500)
    LocationDescription = models.CharField(max_length=500)


class Building(models.Model):
    BuildingID = models.AutoField(primary_key=True)
    BuildingCode = models.CharField(max_length=20)
    # Alternate Key
    BuildingName = models.CharField(max_length=500)


class Restriction(models.Model):
    RestrictionID = models.AutoField(primary_key=True)
    RestrictionDescription = models.CharField(max_length=500)


class ItemRestriction(models.Model):
    ItemRestrictionID = models.ForeignKey(u'Restriction')
    ItemID = models.ForeignKey(u'InventoryItem')


class ItemHistory(models.Model):
    OperatorID = models.ForeignKey(User)
    ItemID = models.ForeignKey(u'InventoryItem')
    ChangeDescription = models.CharField(max_length=500)
    ChangeDateTime = models.DateTimeField()


class ReservationHistory(models.Model):
    OperatorID = models.ForeignKey(User)
    ReservationID = models.ForeignKey(u'Reservation')
    ChangeDescription = models.CharField(max_length=500)
    ChangeDateTime = models.DateTimeField()


class ActionItem(models.Model):
    InventoryItemID = models.ForeignKey(u'InventoryItem')
    ActionID = models.ForeignKey(u'Action')


class ActionType(models.Model):
    ActionTypeID = models.AutoField(primary_key=True)
    ActionTypeName = models.CharField(max_length=500)


class ReservationAction(models.Model):
    ReservationID = models.ForeignKey(u'Reservation')
    ActionID = models.ForeignKey(u'Action')


class Action(models.Model):
    ActionID = models.AutoField(primary_key=True)
    # TODO: What should this go to?
    AssignedOperatorID = models.ForeignKey(User)
    ActionTypeID = models.ForeignKey(u'ActionType')
    StartTime = models.CharField(max_length=500)
    EndTime = models.CharField(max_length=500)
    Origin = models.ForeignKey(u'Location', related_name=u'action_origin')
    Destination = models.ForeignKey(u'Location', related_name=u'action_destination')
    ActionStatus = models.CharField(max_length=500)
    ActionNotes = models.CharField(max_length=500)


class InstitutionalDepartment(models.Model):
    DepartmentID = models.AutoField(primary_key=True)
    DepartmentCode = models.CharField(max_length=50)
    DepartmentName = models.CharField(max_length=500)


class Reservation(models.Model):
    ReservationID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey(User)
    CustomerPhone = models.CharField(max_length=500)
    CustomerEmail = models.CharField(max_length=500)
    CustomerDept = models.CharField(max_length=500)
    CustomerStatus = models.CharField(max_length=500)
    ReservationNotes = models.CharField(max_length=500)
    EventTitle = models.CharField(max_length=500)


class Collection(models.Model):
    CollectionID = models.AutoField(primary_key=True)
    CollectionName = models.CharField(max_length=500)
    CollectionDescription = models.CharField(max_length=500)


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    phoneNumber = models.IntegerField(max_length=15, blank=True, null=True)
    altPhoneNumber = models.IntegerField(max_length=15, blank=True, null=True)
    altEmail = models.EmailField(blank=True, null=True)
    userDept = models.ForeignKey(u'InstitutionalDepartment')
    userNote = models.TextField(blank=True, null=True)