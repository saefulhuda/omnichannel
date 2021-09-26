from django.db import models

# Create your models here.

class ProductSuperCategory(models.Model):
	name = models.CharField(max_length=40)
	title = models.CharField(max_length=40)
	breadcrumb_URL = models.URLField(max_length=512)
	created_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class ProductCategory(models.Model):
	super_category = models.ForeignKey(ProductSuperCategory, on_delete=models.CASCADE)
	name = models.CharField(max_length=40)
	title = models.CharField(max_length=40)
	breadcrumb_URL = models.URLField(max_length=512)
	created_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.super_category.name} {self.name}"


class ProductChildCategory(models.Model):
	category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
	name = models.CharField(max_length=40)
	title = models.CharField(max_length=40)
	breadcrumb_URL = models.URLField(max_length=512)
	created_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class ProductCondition(models.IntegerChoices):
	New = 1
	Second = 2
	Broken = 3


class ProductPriceCurrency(models.IntegerChoices):
	Rupiah = 1
	DolarAS = 2


class Product(models.Model):
	child_category = models.ForeignKey(ProductChildCategory, on_delete=models.PROTECT)
	name = models.CharField(max_length=255)
	condition = models.IntegerField(choices=ProductCondition.choices, default=ProductCondition.New)
	short_desc = models.CharField(max_length=512, blank=True)
	

class ProductPrice(models.Model):
	price = models.IntegerField(default=0)
	currency = models.IntegerField(choices=ProductPriceCurrency.choices, default=ProductPriceCurrency.Rupiah)
