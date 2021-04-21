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

def getPhotoSearch(request,flickr):
	strval = request.GET.get("search",None)
	# if strval:
	photo_list = flickr.photos.search(tags=[{strval}],per_page='8') \
		.find('photos') \
		.findall('photo')
	photos= []
	for photo in photo_list:
		photo_id=photo.attrib['id']
		owner = photo.attrib['owner']
		secret = photo.attrib['secret']
		server = photo.attrib['server']
		title = photo.attrib['title']
		photo_url = \
			f'https://live.staticflickr.com/{server}/{photo_id}_{secret}.jpg'
		photos.append({'id':photo_id,'url':photo_url})
	return photos



# def getPhotosets(flickr):
	
# 	photoset_list = flickr.photosets.getList(user_id='73509078@N00',per_page='5') \
# 		.find('photosets') \
# 		.findall('photoset')

# 	photo_url_list=[]
# 	for photo in photos:
# 		photo_id=photo.attrib['id']
# 		owner = photo.attrib['owner']
# 		secret = photo.attrib['secret']
# 		server = photo.attrib['server']
# 		title = photo.attrib['title']
# 		photo_url = \
# 			f'https://live.staticflickr.com/{server}/{photo_id}_{secret}.jpg'
# 		photo_url_list.append(photo_url)
# 	return photo_url_list


# def getPhotos(flickr,id):
# 	photoset_photos = flickr.photosets.getPhotos(photoset_id=id,per_page='5') \
# 		.find('photoset').findall('photo')
# 	photoset_photos_list = []
# 	for photo in photoset_photos:
# 		photo_id = photo.attrib['id']
# 		secret = photo.attrib['secret']
# 		farm = photo.attrib['farm']
# 		server = photo.attrib['server']
# 		title = photo.attrib['title']
# 		photo_url = \
# 		'http://farm%s.static.flickr.com/%s/%s_%s.jpg'  \
# 			% (farm,server,photo_id,secret)
# 		photoset_photos_list.append(photo_url)
# 	return photoset_photos_list


# def getPhotoUrls(photos):
# 	photo_url_list=[]
# 	for photo in photos:
# 		photo_id=photo.attrib['id']
# 		owner = photo.attrib['owner']
# 		secret = photo.attrib['secret']
# 		server = photo.attrib['server']
# 		title = photo.attrib['title']
# 		photo_url = \
# 			f'https://live.staticflickr.com/{server}/{photo_id}_{secret}.jpg'
# 		photo_url_list.append(photo_url)
# 	return photo_url_list


@require_flickr_auth
def index(request):
	f = flickr(request)
	# photosets = getPhotosets(f)
	photos = getPhotoSearch(request,f)
	
	output = photos
	# output = [{'photo_url':p} for p in photo_list]

	# for url in photo_url_list:
	# 	output.append({'url':url})


	# for photo in photos:
	# 	photo = getPhotos(f,photo['id'])
	# 	output.append({
	# 		'album_name':photo['name'],
	# 		'photo_list': photo})

	context = {'output':output}
	return render(request,
			'index.html',
			context,)