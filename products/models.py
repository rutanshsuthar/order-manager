from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        """
        This delete method allows us to implement recursive delete i.e. if a parent category is deleted then all its
        child categories as well as all of its products as well as the products of its child categories are deleted.
        Now considering that this is soft delete, the records are not removed from the database,
        just the is_active flags are set to False.
        """
        self.is_active = False
        self.save()
        self.product_set.filter(is_active=True).update(is_active=False)
        for child_category in self.category_set.filter(is_active=True):
            child_category.delete()


class Product(models.Model):
    name = models.TextField()
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
