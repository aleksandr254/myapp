import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from django.shortcuts import render
from . import models
from django.utils import timezone

BASE_CRAIGLIST = 'https://sfbay.craigslist.org/search/bbb?query={}'
BASSE_IMG_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')

    if search == None or len(search) == 0:
    	return render(request, 'myapp/new_search.html')

    create_search(search)

    final_url = BASE_CRAIGLIST.format(quote_plus(search))
    responce = requests.get(final_url)

    soup = BeautifulSoup(responce.text, features='html.parser')

    posts_list = soup.find_all('li', {'class' : 'result-row'})
    final_post = []

    for post in posts_list:
    	post_title = post.find(class_='result-title').text
    	post_url = post.find('a').get('href')

    	post_img_id = ''
    	post_img_url = ''

    	if post.find(class_='result-image').get('data-ids'):
    		post_img_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
    		post_img_url = BASSE_IMG_URL.format(post_img_id)
    		print(post_img_url)

    	final_post.append((post_title, post_url, post_img_url))

    stuff_for_frontend = {
    	'search': search,
    	'final_post': final_post,
    	}
    return render(request, 'myapp/new_search.html', stuff_for_frontend)

def create_search(search):
	models.Search.objects.create(search=search, created=timezone.now())