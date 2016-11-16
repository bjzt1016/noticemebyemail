#coding:utf-8
import requests
from lxml import etree
from ipware.ip import get_ip

from django.shortcuts import render
from django.http import HttpResponse

from .models import JobBoLe

from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def inspect_jobbole(request):
	url = "http://fanyi.jobbole.com/category/ready-to-translate/"
	cookies = {
	    'Cookie': '_ga=GA1.2.307546101.1475052639; wordpress_logged_in_0efdf49af511fd88681529ef8c2e5fbf=q3198108035%7C1480828171%7CUnZ8HWtaD5yF5QtE0HGjKDh49lF4YuWIsyryBTFtvV1%7Cfe906324a4b65cb8bc1dcd5be6848f1300223546eee439bb0a3494d19920462e',
	}
	r = requests.get(url, cookies=cookies)

	page = etree.HTML(r.text)
	all_title_nodes = page.xpath('/html/body/div[1]/div/div/div/div[1]/div[1]/ul[1]/li')
	all_titles = [node.xpath('./div/h3/a/span/text()')[0] for i, node in enumerate(all_title_nodes) if i > 3]###前四项不是


	# all_titles = ['Ff', 'Ef', 'F', 'B', 'C'] ### for test

	if not JobBoLe.objects.all():
		new_title = JobBoLe(latest_news=all_titles[0])
		new_title.save()
		return HttpResponse('First Time To This Site!')

	try:### no new article
		JobBoLe.objects.get(latest_news=all_titles[0])  #X1
		return HttpResponse('no new article!')
	except ObjectDoesNotExist:                          #X1
		last_title = JobBoLe.objects.all()[0]
		JobBoLe.objects.all().delete()
		new_title = JobBoLe(latest_news=all_titles[0])
		new_title.save()

		all_new_titles = ''
		for one_title in all_titles:
			if one_title == last_title.latest_news:
				break
			else:
				all_new_titles += one_title + '##########'

		return HttpResponse('new article:%s!check it!' %all_new_titles)

def test(request):
	return HttpResponse(get_ip(request))

'''ref
X1:https://docs.djangoproject.com/en/1.8/ref/models/querysets/#get
'''