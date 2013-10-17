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

