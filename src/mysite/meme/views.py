from mysite.settings import FLICKR_API_KEY, FLICKR_API_SECRET
from django.shortcuts import render, redirect
import flickrapi

# log infomation to see the status
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
	# get the search tag
	strval = request.GET.get("search",None)
	# get the photo's atribute by given tag
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



@require_flickr_auth
def index(request):
	f = flickr(request)
	photos = getPhotoSearch(request,f)
	output = photos
	context = {'output':output}
	return render(request,
			'index.html',
			context,)