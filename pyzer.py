#imports
from bottle import route, run, request, response
import urllib
import Image
import cStringIO
import redis

#defining settings
redis_cache = redis.Redis(host='localhost', port=6379, db=711)

#routes and classes
@route('/hi/:name')
def hi(name):
	return 'Hello %s!' % name

@route('/resize')
def resize():
	if request.GET.get('src'):
		image_url = request.GET.get('src')
	else:
		return 'no image defined'

	#determining size
	if request.GET.get('w'):
		width = int(request.GET.get('w'))
	else:
		width = 2000
		w_default = True

	if request.GET.get('h'):
		height = int(request.GET.get('h'))
	else:
		height = 2000
		if w_default == True:
			return 'include at lest one size parameter'
	image_id = str(image_url)+'_'+str(width)+'_'+str(height)
	print image_id
	if redis_cache.exists(image_id):
		image_return = redis_cache.get(image_id)
	else:
		#opens image
		file_from_url = urllib.urlopen(image_url)
		file_contents = cStringIO.StringIO(file_from_url.read())
		image = Image.open(file_contents)

		#does resizing to said image
		#...

		#preps image for response
		image_out = cStringIO.StringIO()
		image.save(image_out, "JPEG")
		image_return = image_out.getvalue()
		
		#saves image to cache
		redis_cache.set(image_id, image_return)

	response.content_type = 'image/jpg'
	return image_return
	

#let's run this
run(host='localhost', port=9999, reloader=True)
