# rom django.db import models

# from lib.FlickrClient import FlickrClient

# class Photo(models.Model):
#         title = models.CharField(blank=True, maxlength=100)
#         flickr_id = models.IntegerField()
#         flickr_owner = models.CharField(maxlength=20)
#         flickr_server = models.IntegerField()
#         flickr_secret = models.CharField(maxlength=50)
        
#         class Admin:
#                 list_display = ('title',)

#         def __str__(self):
#                 return self.title
                
#         def get_absolute_url(self):
#                 return "/photos/%s/" % (self.id)

#         def sync_flickr_photos(*args, **kwargs):
#             API_KEY = '336e6f4d1ff271b7b053517fefb5d746'
#             USER_ID = 'bbc57228c99c80c6D'

#             cur_page = 1            # Start on the first page of the stream
#             paginate_by = 20        # Get 20 photos at a time
#             dupe = False            # Set our dupe flag for the following loop

#             client = FlickrClient(API_KEY)          # Get our flickr client running

#             while (not dupe):
#                     photos = client.flickr_people_getPublicPhotos(user_id=USER_ID, page=cur_page, per_page=paginate_by)

#                     for photo in photos:
#                             try:
#                                     row = Photo.objects.get(flickr_id=photo("id"), flickr_secret=str(photo("secret")))
#                                     # Raise exception if photo doesn't exist in our DB yet

#                                     # If the row exists already, set the dupe flag
#                                     dupe = True
#                             except ObjectDoesNotExist:
#                                     p = Photo(
#                                     title = str(photo("title")),
#                                     flickr_id = int(photo("id")),
#                                     flickr_owner = str(photo("owner")),
#                                     flickr_server = int(photo("server")),
#                                     flickr_secret = str(photo("secret")),
#                                     )
#                                     p.save()

#                                     if (dupe or photos("page") == photos("pages")):   # If we hit a dupe or if we did the last page...
#                                             break
#                             else:
#                                     cur_page += 1

            