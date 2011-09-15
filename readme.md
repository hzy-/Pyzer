#Introduction
Pyzer is a simple little script meant to enable the quick and easy resizing of iamges on the web.
It's creation has come out of my need for a simple way to resize images on the fly with a cached output.

#Technologies
* Bottle web framework for the HTTP request handling
* Python Image Library (PIL) for the resizing of images
* Some sort of caching (Memcache or Redis)

#Implementation
I plan to be using this for my [Weldr](http://weldr.me) social network, as a way of sane-ly displaying images from a foreign source.
