from django.db import models
from django.contrib.auth.models import User


class Label(models.Model):
    LabelID = models.AutoField(primary_key=True)
    LabelName = models.CharField(max_length=500)
    ParentCategory = models.ForeignKey('Label')


class ItemLabel(models.Model):
    LabelID = models.ForeignKey('Label')
    ItemID = models.ForeignKey('InventoryItem')


class LabelNotes(models.Model):
    LabelNoteID = models.AutoField(primary_key=True)
    LabelID = models.ForeignKey('Label')
    LabelNote = models.CharField(max_length=500)


class LabelImage(models.Model):
    LabelID = models.ForeignKey('Label')
    ImageID = models.ForeignKey('Image')


class ItemImage(models.Model):
    ItemID = models.ForeignKey('InventoryItem')
    ImageID = models.ForeignKey('Image')


class Image(models.Model):
    ImageID = models.AutoField(primary_key=True)


class Status(models.Model):
    StatusID = models.AutoField(primary_key=True)
    StatusDescription = models.CharField(max_length=500)


class InventoryItem(models.Model):
    ItemID = models.AutoField(primary_key=True)
    AlternateID = models.ForeignKey('InventoryWidget')
    BrandID = models.ForeignKey('ItemBrand')
    ModelID = models.ForeignKey('ItemModel')
    Description = models.CharField(max_length=500)
    Notes = models.CharField(max_length=500)
    CategoryID = models.ForeignKey('Label')
    ParentItem = models.ForeignKey('InventoryItem')
    StatusID = models.ForeignKey('Status')
    StorageLocation = models.ForeignKey('Location')
    CollectionID = models.ForeignKey('Collection')


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
    BuildingID = models.ForeignKey('Building')
    RoomNumber = models.CharField(max_length=500)
    LocationDescription = models.CharField(max_length=500)


class Building(models.Model):
    BuildingID = models.AutoField(primary_key=True)
    BuildingCode = models.IntegerField()
    # Alternate Key
    BuildingName = models.CharField(max_length=500)


class Restriction(models.Model):
    RestrictionID = models.AutoField(primary_key=True)
    RestrictionDescription = models.CharField(max_length=500)


class ItemRestriction(models.Model):
    ItemRestrictionID = models.ForeignKey('Restriction')
    ItemID = models.ForeignKey('InventoryItem')


class ItemHistory(models.Model):
    OperatorID = models.ForeignKey(User)
    ItemID = models.ForeignKey('InventoryItem')
    ChangeDescription = models.CharField(max_length=500)
    ChangeDateTime = models.CharField(max_length=500)


class ReservationHistory(models.Model):
    OperatorID = models.ForeignKey(User)
    ReservationID = models.ForeignKey('Reservation')
    ChangeDescription = models.CharField(max_length=500)
    ChangeDateTime = models.CharField(max_length=500)


class ActionItem(models.Model):
    InventoryItemID = models.ForeignKey('InventoryItem')
    ActionID = models.ForeignKey('Action')


class ActionType(models.Model):
    ActionTypeID = models.AutoField(primary_key=True)
    ActionTypeName = models.CharField(max_length=500)


class ReservationAction(models.Model):
    ReservationID = models.ForeignKey('Reservation')
    ActionID = models.ForeignKey('Action')


class Action(models.Model):
    ActionID = models.AutoField(primary_key=True)
    # TODO: What should this go to?
    # AssignedOperatorID = models.ForeignKey()
    ActionTypeID = models.ForeignKey('ActionType')
    StartTime = models.CharField(max_length=500)
    EndTime = models.CharField(max_length=500)
    Origin = models.ForeignKey('Location', related_name='action_origin')
    Destination = models.ForeignKey('Location', related_name='action_destination')
    ActionStatus = models.CharField(max_length=500)
    ActionNotes = models.CharField(max_length=500)


class InstitutionalUser(models.Model):
    InstitutionalID = models.AutoField(primary_key=True)
    Username = models.IntegerField()
    UserPhone = models.CharField(max_length=500)
    UserEmail = models.CharField(max_length=500)
    UserDept = models.ForeignKey('InstitutionalDepartment')
    UserFirstName = models.CharField(max_length=500)
    UserLastName = models.CharField(max_length=500)


class InstitutionalDepartment(models.Model):
    DepartmentID = models.AutoField(primary_key=True)
    DepartmentAbbreviation = models.IntegerField()
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
