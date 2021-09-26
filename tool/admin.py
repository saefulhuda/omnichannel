from django.contrib import admin
from tool.models import JakmallScrapper, JakmallImagesScrapper
from omnichannel import providers as provider
import threading
from django.utils.html import mark_safe

# Register your models here.
admin.autodiscover()
admin.site.enable_nav_sidebar = False
admin.site.site_header = 'Omnichannel Marketplace'


class JakmallScrapperAdmin(admin.ModelAdmin):
	search_fields = ['name', 'sku']
	list_display = ('image', 'name', 'seller', 'price', 'final_price', 'stock', 'sold_count', 'review_count', 'rating_count', 'created_time')
	list_filter = ('seller',)
	list_per_page = 20
	products = []

	def image(self, obj):
		image = JakmallImagesScrapper.objects.filter(jakmall_scrap=obj, image_type=2)
		if image.exists():
			image = image[0]
			return mark_safe('<img width="100" src="{}"></img>'.format(image.url))
		else:
			return 'Image not found'

	def scrap_product_detail(self, endpoint):
		scrap = provider.jakmall_product_detail_scrapper(endpoint)
		if scrap['message'] == 'OK':
			self.products.append(scrap['products'])


	def changelist_view(self, request, extra_context=None):
		extra_context = {'message':''}
		endpoint = request.GET.get('jm_endpoint', '')
		endpoint = endpoint.replace("https://www.jakmall.com/",'')
		endpoint_count = endpoint.split('/')
		role = 'detail' if len(endpoint_count) > 1 else 'list'
		if endpoint != '' and role != '':
			import json
			if role == 'detail':
				self.scrap_product_detail(endpoint)
			elif role == 'list':
				scrap = provider.jakmall_product_list_scrapper(endpoint)
				scrap = scrap['products']
				threads = []
				for product in scrap:
					t = threading.Thread(target=self.scrap_product_detail, args=(product['url'].replace("https://www.jakmall.com/",''),))
					t.start()
					threads.append(t)
				for t in threads:
					t.join()
			for product in self.products:
				sku = product['sku'][list(product['sku'])[0]]
				production_existing = JakmallScrapper.objects.filter(pid=product['id'])
				if production_existing.exists():
					production_existing.delete()
				save_product = JakmallScrapper.objects.create(
					pid=product['id'],
					name=product['name'],
					sku=sku['sku'] if sku['sku'] is not None else '',
					price=sku['price']['list'],
					final_price=sku['price']['final'],
					discount=sku['price']['discount']['percentage'] if sku['price']['discount'] is not None else 0,
					weight=sku['weight'],
					variant=json.dumps(product['variants'][list(product['variants'])[0]]) if len(product['variants']) > 0 else '',
					url=product['url'],
					seller=product['store']['name'],
					seller_url=product['store']['url'],
					rating_count=product['rating']['summary']['average'] if product['rating']['summary']['average'] is not None else 0,
					review_count=product['rating']['summary']['count'],
					sold_count=product['sold'],
					stock=1 if sku['in_stock'] is True else 0
					)

				threads = []
				for image in sku['images']:
					t = threading.Thread(target=JakmallImagesScrapper.objects.create(
						jakmall_scrap=save_product,
						url=image['detail']
						).save())
					t.start()
					threads.append(t)
				for t in threads:
					t.join()

				save_image_thumbnail = JakmallImagesScrapper.objects.create(
					jakmall_scrap=save_product,
					url=sku['images'][0]['thumbnail'],
					image_type=2
					).save()
		return super().changelist_view(request, extra_context=extra_context)


class JakmallImagesScrapperAdmin(JakmallScrapperAdmin):
	search_fields = ['jakmall_scrap__name', 'jakmall_scrap__sku']
	list_display = ('jakmall_scrap', 'image_type')
	list_filter = ('jakmall_scrap__seller', 'image_type')


admin.site.register(JakmallScrapper, JakmallScrapperAdmin)
admin.site.register(JakmallImagesScrapper, JakmallImagesScrapperAdmin)