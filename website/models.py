from django.db import models

class ItemLabel(models.Model):
	ItemID = ForeignKey('InventoryItem')
	CategoryID = ForeignKey('Category')

class InventoryItem(models.Model):
	AltID = models.ForeignKey()
	BrandID = models.ForeignKey()
	ModelID = models.ForeignKey()
	StorageLocation_ID = models.ForeignKey()
	ParentID = ForeignKey('InventoryItem')
	CategoryID = ForeignKey('Category')
	Description = models.CharField()
	Notes = models.CharField()

class InventoryWidget(models.Model):
	pass
	
class Brand(models.Model):
	Name = models.CharField()

class ItemModel(models.Model):
	Description = models.CharField()

class Building(models.Model):
	Name = models.CharField()

class Location(models.Model):
	BuildingID = ForeignKey(Building)
	RoomNumber = models.CharField()
	Description = models.CharField()

class Status(models.Model):
	Description = models.CharField()

class User(models.Model):
	Username = models.CharField()

class Restriction(models.Model):
	Description = models.CharField()

class ItemRestrictions(models.Model):
	ItemID(InventoryItem)

class ItemHistory(models.Model):
	UserID = ForeignKey(User)
	ItemID = ForeignKey('InventoryItem')
	ChangeDesc = models.CharField()
	ChangeDateTime = models.CharField()

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
