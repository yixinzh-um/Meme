from mysite.settings import FLICKR_API_KEY, FLICKR_API_SECRET
from django.shortcuts import render, redirect
import flickrapi

import logging
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def require_flickr_auth(view):
#View decorator, redirects users to Flickr when no valid
#authentication token is available.

	def protected_view(request, *args, **kwargs):

		f=flickr(request)

		try:
			token = request.session['token']	
		except:
			token = None	

		if token:
			#check validity of the token
			try:
				f.auth_checkToken()
			except flickrapi.FlickrError:
				#set invalid token to None
				token = None
				del request.session['token']

		if not token:
			# Redirect to Flickr for authentication 
			# if no valid token
			pass
			# url = f.auth_url(perms=u'write')
			# return redirect(url)

		return view(request, *args, **kwargs)

	return protected_view

def flickr_callback(request):
	if not 'flickr_token' in request.session:
		f = flickrapi.FlickrAPI(FLICKR_API_KEY,
			FLICKR_API_SECRET, store_token=False)
		frob=None
		token=None
		try:
			frob = request.GET['frob']
			token = f.get_token(frob)
			request.session['token'] = token
		except Exception:
			pass
	return redirect('index')

def flickr(request):
	try:
		token = request.session['token']
		log.info('Getting token from session: %s' % token)	
	except:
		token = None		
		log.info('No token in session')

	f = flickrapi.FlickrAPI(FLICKR_API_KEY,
		FLICKR_API_SECRET, token=token,
		store_token=False)

	return f

def getPhotosets(flickr):
	
	photoset_list = flickr.photosets.getList(user_id='73509078@N00',per_page='5') \
		.find('photosets') \
		.findall('photoset')
	photoset_list_array = []
	for photoset in photoset_list:
		photoset_id = photoset.attrib['id']
		photoset_title = photoset.find('title').text
		photoset_list_array.append({
			'id':photoset_id,
			'name':photoset_title})
	return photoset_list_array

def getPhotos(flickr,id):
	photoset_photos = flickr.photosets.getPhotos(photoset_id=id,per_page='5') \
		.find('photoset').findall('photo')
	photoset_photos_list = []
	for photo in photoset_photos:
		photo_id = photo.attrib['id']
		secret = photo.attrib['secret']
		farm = photo.attrib['farm']
		server = photo.attrib['server']
		title = photo.attrib['title']
		photo_url = \
		'http://farm%s.static.flickr.com/%s/%s_%s.jpg'  \
			% (farm,server,photo_id,secret)
		photoset_photos_list.append(photo_url)
	return photoset_photos_list


@require_flickr_auth
def index(request):
	f = flickr(request)
	photosets = getPhotosets(f)
	output = []
	for photoset in photosets:
		photos = getPhotos(f,photoset['id'])
		output.append({
			'album_name':photoset['name'],
			'photo_list': photos})

	context = {'output':output}
	return render(request,
			'index.html',
			context,)