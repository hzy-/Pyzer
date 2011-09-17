#imports
from bottle import route, run, request, response, abort
import urllib
import Image
import cStringIO
import redis
import cPickle as pickle
import daemon

#defining settings
redis_cache = redis.Redis(host='localhost', port=6379, db=711)

#routes and classes
@route('/resize')
def resize():
	if request.headers.get('If-Modified-Since') == 'Wed, 11 Jan 1984 08:00:00 GMT':
		abort(304, "Not Modified")
	if request.GET.get('src'):
		image_url = request.GET.get('src')
	else:
		return 'no image defined'

	#determining size
	if request.GET.get('w'):
		width = int(request.GET.get('w'))
	else:
		width = 2000

	if request.GET.get('h'):
		height = int(request.GET.get('h'))
	else:
		height = 2000

	r_image_id = 'r_'+image_url+'_'+str(width)+'_'+str(height)
	o_image_id = 'o_'+image_url
	if redis_cache.exists(r_image_id):
		image_return = redis_cache.get(r_image_id)
	else:
		#opens image
		if redis_cache.exists(o_image_id):
			file_contents = cStringIO.StringIO(redis_cache.get(o_image_id))
		else:
			file_from_url = urllib.urlopen(image_url)
			file_contents = cStringIO.StringIO(file_from_url.read())
			redis_cache.set(o_image_id, file_contents.getvalue())

		image = Image.open(file_contents)

		#does resizing to said image
		size = [width, height]
		image.thumbnail(size, Image.ANTIALIAS)

		#preps image for response
		image_out = cStringIO.StringIO()
		image.save(image_out, "JPEG", quality=80)
		image_return = image_out.getvalue()
		
		#saves image to cache
		redis_cache.set(r_image_id, image_return)

	print r_image_id
	response.content_type = 'image/jpg'
	response.set_header('Cache-Control', 'max-age=31536000')
	response.set_header('Last-Modified', 'Wed, 11 Jan 1984 08:00:00 GMT')
	return image_return
	

#let's run this
context = daemon.DaemonContext(
    working_directory='.',
    umask=0o002,
    )

with context:
	run(server='tornado', host='127.0.0.1', port=9998)
