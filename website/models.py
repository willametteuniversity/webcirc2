from django.db import models

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
        CategoryID = models.ForeignKey(Category)
        Description = models.CharField(max_length=500)
        Notes = models.CharField(max_length=1000)

class ItemLabel(models.Model):
        ItemID = models.ForeignKey(InventoryItem)
        CategoryID = models.ForeignKey(Category)

