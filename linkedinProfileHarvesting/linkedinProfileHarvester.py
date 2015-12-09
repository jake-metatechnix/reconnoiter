#!/usr/bin/env python

__author__ = 'Jason Wood - aka Tadaka'

__doc__ = """
http://www.jwnetworkconsulting.com

"""

import re
import urllib
import urllib2
import logging

class Get(object):

	def __init__(self):

		self.user_agent = 'Lynx/2.8.6rel.5 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.8l'

	def get(self, url):
		"""
		get(url) -> Response

		Open given url and return response.
		"""

		try:
			request = urllib2.Request(url)
			request.add_header('User-Agent', self.user_agent)

			logging.debug('Get.get - getting url ' + url)

			result = urllib2.urlopen(request)

		except: raise RuntimeError('unable to open url')

		return result


class Search(Get):

	def search(self, q, start = 0, num = 10):
		"""
		search(q, start = 0, num = 10) -> generator

		Do google web search.
		"""

		url = 'http://www.google.com/m/search?'
		query = urllib.urlencode({'q':q, 'start':start, 'num':num})

	 	# print url + query

		result = self.get(url + query)
		content = result.read()

            	# print content

		# regex for the profile url
		prof_urls = re.findall(
			'q=(http:\/\/\w{1,4}.linkedin.com\/.+?)&.+?>',content)

		# regex for peoples names
	        prof_names = re.findall('<a href="\/url\?q=http:\/\/w{1,4}\.linkedin\.com.*?">(.+? .+?) .+?<\/a>',content)

        	for n, u in zip(prof_names, prof_urls):
            	 	print '{0}\n{1}\n'.format(n, u)
			f = open('linkedin-profiles.' + sys.argv[1], 'a')
			f.write('{0}\n{1}\n\n'.format(n, u))

		return content

class Crawl(Search):

	def crawl(self, q, depth = 0):

		index = 1
		last_results = None

		while True:
			if index == 1:
				start = 0

			else:
				start = (index - 1) * 10

			try:
				# print "try statement"
				results = self.search(q, start, 10)

			except: continue

			if not results:
				break

			if last_results == results:
				break

			last_results = results

			yield results

			if index == depth:
				break

			index = index + 1



if __name__ == '__main__':
	import os
	import sys
	import time

	import signal
	signal.signal(signal.SIGINT, lambda signum, frame: sys.exit())

	if len(sys.argv) < 3:
		print 'usage:', os.path.basename(sys.argv[0]), 'query #-of-results-pages'

		sys.exit()

	logging.basicConfig()

	g = Crawl()

	search_term = "site:linkedin.com inurl:pub "

	search_term +=  sys.argv[1]

	for result in g.crawl(search_term, int(sys.argv[2])):
		# Weak attempt at avoiding a ban by Google
		time.sleep(1)
