from django.db import models

class Category(models.Model)
	Name = CharField()
	ParentID = ForeignKey(Category)

class ItemLabel(models.Model)
	ItemID = ForeignKey(InventoryItem)
	CategoryID = ForeignKey(Category)

class InventoryItem(models.Model)
	AltID = ForeignKey()
	BrandID = ForeignKey()
	ModelID = ForeignKey()
	StorageLocation_ID = ForeignKey()
	ParentID = ForeignKey(InventoryItem)
	CategoryID = ForeignKey(Category)
	Description = CharField()
	Notes = CharField()

class InventoryWidget(models.Model)
	
class Brand(models.Model)
	Name = CharField()

class ItemModel(models.Model)
	Description = CharField()

class Building(models.Model)
	Name = CharField()

class Location(models.Model()
	BuildingID = ForeignKey(Building)
	RoomNumber = CharField()
	Description = CharField()

class Status(models.Model)
	Description = CharField()

class User(models.Model)
	Username = CharField()

class Restriction(models.Model)
	Description = CharField()

class ItemRestrictions(models.Model)
	ItemID(InventoryItem)

class ItemHistory(models.Model)
	UserID = ForeignKey(User)
	ItemID = ForeignKey(InventoryItem)
	ChangeDesc = CharField()
	ChangeDateTime = CharField()
