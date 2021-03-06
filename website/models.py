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
    StatusName = models.CharField(max_length=500)
    StatusDescription = models.CharField(max_length=500)


class ActionState(models.Model):
    ActionStateID = models.AutoField(primary_key=True)
    ActionStateName = models.CharField(max_length=500)
    ActionStateDescription = models.CharField(max_length=500)
    ActionComplete = models.BooleanField(default=False)


class Reservation(models.Model):
    ReservationID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey(User, related_name='owner_set')
    OwnerID = models.ForeignKey(User)
    CustomerPhone = models.CharField(max_length=500)
    CustomerEmail = models.CharField(max_length=500)
    CustomerDept = models.CharField(max_length=500)
    CustomerStatus = models.CharField(max_length=500)
    ReservationNotes = models.CharField(max_length=500, null=True, blank=True)
    EventTitle = models.CharField(max_length=500)
    Finalized = models.BooleanField(default=False)


class Action(models.Model):
    ActionID = models.AutoField(primary_key=True)
    AssignedOperatorID = models.ForeignKey(User, null=True, blank=True)    # User who created the reservation
    ActionTypeID = models.ForeignKey(u'ActionType', null=True, blank=True)
    StartTime = models.DateTimeField()
    EndTime = models.DateTimeField()
    Origin = models.ForeignKey(u'Location', related_name=u'action_origin')
    Destination = models.ForeignKey(u'Location', related_name=u'action_destination')
    ActionState = models.ForeignKey(ActionState)
    ActionNotes = models.CharField(max_length=500, null=True, blank=True)
    Reservation = models.ManyToManyField(Reservation, blank=True)


class InventoryItem(models.Model):
    ItemID = models.AutoField(primary_key=True)
    Description = models.CharField(max_length=500)
    CategoryID = models.ForeignKey(u'Label')
    StorageLocation = models.ForeignKey(u'Location')
    CollectionID = models.ForeignKey(u'Collection')
    Notes = models.CharField(max_length=500, null=True, blank=True)
    Action = models.ManyToManyField(Action, blank=True)
    AlternateID = models.ForeignKey(u'InventoryWidget', blank=True, null=True)
    BrandID = models.ForeignKey(u'ItemBrand')
    ModelID = models.ForeignKey(u'ItemModel')
    ParentItem = models.ForeignKey(u'InventoryItem', null=True, blank=True)
    StatusID = models.ForeignKey(u'Status', null=True)


class InventoryWidget(models.Model):
    InventoryID = models.AutoField(primary_key=True)


class ItemBrand(models.Model):
    BrandID = models.AutoField(primary_key=True)
    BrandName = models.CharField(max_length=500)


class ItemModel(models.Model):
    ModelID = models.AutoField(primary_key=True)
    ModelDesignation = models.CharField(max_length=500)


class Building(models.Model):
    BuildingID = models.AutoField(primary_key=True)
    BuildingCode = models.CharField(max_length=20)
    # Alternate Key
    BuildingName = models.CharField(max_length=500)


class Location(models.Model):
    LocationID = models.AutoField(primary_key=True)
    BuildingID = models.ForeignKey(Building)
    RoomNumber = models.CharField(max_length=500)
    LocationDescription = models.CharField(max_length=500)


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


class ActionType(models.Model):
    ActionTypeID = models.AutoField(primary_key=True)
    ActionTypeName = models.CharField(max_length=500)


class InstitutionalDepartment(models.Model):
    DepartmentID = models.AutoField(primary_key=True)
    DepartmentCode = models.CharField(max_length=50)
    DepartmentName = models.CharField(max_length=500)


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