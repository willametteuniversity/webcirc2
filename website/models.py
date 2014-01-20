from django.db import models


class ItemLabel(models.Model):
    ItemID = models.ForeignKey('InventoryItem')
    CategoryID = models.ForeignKey('Category')


class InventoryItem(models.Model):
    AltID = models.ForeignKey('AlternateID')
    BrandID = models.ForeignKey('BrandID')
    ModelID = models.ForeignKey('ModelID')
    StorageLocation_ID = models.ForeignKey('StorageLocation')
    ParentID = models.ForeignKey('InventoryItem')
    CategoryID = models.ForeignKey('Category')
    Description = models.CharField(max_length=500)
    Notes = models.CharField(max_length=500)


class InventoryWidget(models.Model):
    pass


class Brand(models.Model):
    Name = models.CharField(max_length=500)


class ItemModel(models.Model):
    Description = models.CharField(max_length=500)


class Building(models.Model):
    Name = models.CharField(max_length=500)


class Location(models.Model):
    BuildingID = models.ForeignKey('Building')
    RoomNumber = models.CharField(max_length=500)
    Description = models.CharField(max_length=500)


class StorageLocation(models.Model):
    pass


class AlternateID(models.Model):
    pass


class Status(models.Model):
    Description = models.CharField(max_length=500)


class User(models.Model):
    Username = models.CharField(max_length=500)


class Restriction(models.Model):
    Description = models.CharField(max_length=500)


class ItemRestrictions(models.Model):
    ItemID = models.ForeignKey('InventoryItem')


class ItemHistory(models.Model):
    UserID = models.ForeignKey('User')
    ItemID = models.ForeignKey('InventoryItem')
    ChangeDesc = models.CharField(max_length=500)
    ChangeDateTime = models.CharField(max_length=500)


class Category(models.Model):
    Name = models.CharField(max_length=255)
    ParentID = models.ForeignKey('self')


class InventoryItem(models.Model):
    AltID = models.ForeignKey('AltID')
    BrandID = models.ForeignKey('BrandID')
    ModelID = models.ForeignKey('ModelID')
    # TODO: We don't have this defined yet
    StorageLocationID = models.ForeignKey('StorageLocationID')
    ParentID = models.ForeignKey('self')
    CategoryID = models.ForeignKey('Category')
    Description = models.CharField(max_length=500)
    Notes = models.CharField(max_length=1000)


class ItemLabel(models.Model):
    ItemID = models.ForeignKey('InventoryItem')
    CategoryID = models.ForeignKey('Category')


class AltID(models.Model):
    pass


class BrandID(models.Model):
    pass


class ModelID(models.Model):
    pass


class StorageLocationID(models.Model):
    pass
