from django.db import models

class Label(models.Model):
	LabelID = models.IntegerField()
	LabelID.primary_key = True
	LabelName = models.CharField(max_length=500)
	ParentCategory = models.ForeignKey('Label')
	
class ItemLabel(models.Model):
	LabelID = models.ForeignKey('Label')
	ItemID = models.ForeignKey('InventoryItem')

class LabelNotes(models.Model):
	LabelNoteID = models.IntegerField()
	LabelNoteID.primary_key = True
	LabelID = models.ForeignKey('LabelID')
	LabelNote = models.CharField(max_length=500)
	
class LabelImage(models.Model):
	LabelID = models.ForeignKey('Label')
	ImageID = models.ForeignKey('Image')
	
class ItemImage(models.Model):
	ItemID = models.ForeignKey('InventoryItem')
	ImageID = models.ForeignKey('Image')

class Image(models.Model):
	ImageID = models.IntegerField()
	ImageID.primary_key = True
	#Image

class Status(models.Model):
	StatusID = models.IntegerField()
	StatusID.primary_key = True
	StatusDescription = models.charField(max_length=500)
	
class InventoryItem(models.Model):
	ItemID = models.IntegerField()
	ItemID.primary_key = True
	AlternateID = models.ForeignKey('InventoryWidget')
	BrandID = models.ForeignKey('BrandID')
	ModelID = models.ForeignKey('ItemModel')
	Description = models.CharField(max_length=500)
	Notes = models.CharField(max_length=500)
	CategoryID = models.ForeignKey('Label')
	ParentItem = models.ForeignKey('InventoryItem')
	StatusID = models.ForeignKey('Status')
	StorageLocation = models.ForeignKey('Location')
	CollectionID = models.ForeignKey('Collection')
	#RECORD
	
class InventoryWidget(models.Model):
	InventoryID = models.IntegerField()
	InventoryID.primary_key = True
	#RECORD
	
class ItemBrand(models.Model):
	BrandID = models.IntegerField()
	BrandID.primary_key = True
	BrandName = models.CharField(max_length=500)
	
class ItemModel(models.Model):
	ModelID = models.IntegerField()
	ModelID.primary_key = True
	ModelDesignation = models.CharField(max_length=500)
	
class Location(models.Model):
	LocationID = models.IntegerField()
	LocationID.primary_key = True
	BuildingID = models.ForeignKey('BuildingID')
	RoomNumber = models.CharField(max_length=500)
	LocationDescription = models.CharField(max_length=500)
	
class Building(models.Model):
	BuildingID = models.IntegerField()
	BuildingID.primary_key = True
	BuildingCode = models.IntegerField() #Alternate Key
	BuildingName = models.charField(max_length=500)
	
class Restriction(models.Model):
	RestrictionID = models.IntegerField()
	RestrictionID.primary_key = True
	RestrictionDescription = models.charField(max_length=500)
	
class ItemRestriction(models.Model):
	ItemRestrictionID = models.ForeignKey('Restriction')
	ItemID = models.ForeignKey('InventoryItem')
	
class User(models.Model):
	UserID = models.IntegerField()
	UserID.primary_key = True
	UserInstitutionalID = models.ForeignKey('InstitutionalUser')
	Username = models.IntegerField() #Alternate Foreign Key
	UserAltPhone = models.charField(max_length=500)
	UserAltEmail = models.charField(max_length=500)
	UserStatus = models.ForeignKey()
	UserNote = models.charField(max_length=500)
	
class ItemHistory(models.Model):
	OperatorID = models.ForeignKey('User')
	ItemID = models.ForeignKey('InventoryItem')
	ChangeDescription = models.charField(max_length=500)
	ChangeDateTime = models.charField(max_length=500)
	
class ReservationHistory(models.Model):
	OperatorID = models.ForeignKey('User')
	ReservationID = OperatorID = models.ForeignKey('User')
	ChangeDescription = models.charField(max_length=500)
	ChangeDateTime = models.charField(max_length=500)
	
class ActionItem(models.Model):
	InventoryItemID = models.ForeignKey('InventoryItem')
	ActionID = models.ForeignKey('Action')
	
class ActionType(models.Model):
	ActionTypeID = models.IntegerField()
	ActionTypeID.primary_key = True
	ActionTypeName = models.charField(max_length=500)
	
class ReservationAction(models.Model):
	ReservationID = models.ForeignKey('Reservation')
	ActionID = models.ForeignKey('Action')
	
class Action(models.Model):
	ActionID = models.IntegerField()
	ActionID.primary_key = True
	AssignedOperatorID = models.ForeignKey()
	ActionTypeID = models.ForeignKey('ActionType')
	StartTime = models.charField(max_length=500)
	EndTime = models.charField(max_length=500)
	OriginID = models.ForeignKey('Location')
	DestinationID = models.ForeignKey('Location')
	ActionStatus = models.charField(max_length=500)
	ActionNotes = models.charField(max_length=500)
	
class InstitutionalUser(models.Model):
	InstitutionalID = models.IntegerField()
	InstitutionalID.primary_key = True
	Username = models.IntegerField() #Alternate Key
	UserPhone = models.charField(max_length=500)
	UserEmail = models.charField(max_length=500)
	UserDept = models.ForeignKey('InstitutionalDepartment')
	UserFirstName = models.charField(max_length=500)
	UserLastName = models.charField(max_length=500)
	
class InstitutionalDepartment(models.Model):
	DepartmentID = models.IntegerField()
	DepartmentID.primary_key = True
	DepartmentAbbreviation = models.IntegerField() #Alternate Key
	DepartmentName = models.charField(max_length=500)
	
class Reservation(models.Model):
	ReservationID = models.IntegerField()
	ReservationID.primary_key = True
	CustomerID = models.ForeignKey('User')
	CustomerPhone = models.charField(max_length=500)
	CustomerEmail = models.charField(max_length=500)
	CustomerDept = models.charField(max_length=500)
	CustomerStatus = models.charField(max_length=500)
	ReservationNotes = models.charField(max_length=500)
	EventTitle = models.charField(max_length=500)
	
class Collection(models.Model):
	CollectionID = models.IntegerField()
	CollectionID.primary_key = True
	CollectionName = models.charField(max_length=500)
	CollectionDescription = models.charField(max_length=500)
