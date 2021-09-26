from django.db import models

# Create your models here.
class JakmallScrapper(models.Model):
	pid = models.IntegerField(default=0)
	name = models.CharField(max_length=255)
	sku = models.CharField(max_length=100)
	price = models.IntegerField(default=0, verbose_name='Price (normal)')
	final_price = models.IntegerField(default=0, verbose_name='Price (after discount cut)')
	discount = models.IntegerField(default=0, verbose_name='Discount (in %)')
	stock = models.IntegerField(default=0)
	weight = models.IntegerField(default=0, verbose_name='Price (in Gram)')
	variant = models.CharField(max_length=551, blank=True)
	url = models.URLField(max_length=512)
	seller = models.CharField(max_length=255)
	seller_url = models.URLField(max_length=512)
	seller_location = models.CharField(max_length=512, blank=True)
	rating_count = models.IntegerField(default=0) 
	review_count = models.IntegerField(default=0)
	sold_count = models.IntegerField(default=0)
	views_count = models.IntegerField(default=0)
	created_time = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return f"{self.seller} - {self.name}"

class ImageType(models.IntegerChoices):
	Standard = 1
	Thumbnail = 2
	Square = 3



class JakmallImagesScrapper(models.Model):
	jakmall_scrap = models.ForeignKey(JakmallScrapper, on_delete=models.CASCADE)
	file = models.FileField(upload_to='images/jackmall/temp/', blank=True)
	url = models.URLField(max_length=512)
	image_type = models.IntegerField(choices=ImageType.choices, default=ImageType.Standard)
	created_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.jakmall_scrap.name} - {self.image_type}"