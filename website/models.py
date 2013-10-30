from django.db import models

class Category(models.Model):
        Name = models.CharField()
        ParentID = models.ForeignKey('self')

class ItemLabel(models.Model):
        ItemID = models.ForeignKey(InventoryItem)
        CategoryID = models.ForeignKey(Category)

class InventoryItem(models.Model):
        AltID = models.ForeignKey()
        BrandID = models.ForeignKey()
        ModelID = models.ForeignKey()
        StorageLocation_ID = models.ForeignKey()
        ParentID = models.ForeignKey('self')
        CategoryID = models.ForeignKey(Category)
        Description = models.CharField()
        Notes = models.CharField()

