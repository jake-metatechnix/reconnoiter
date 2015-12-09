#!/usr/bin/env python

__version__ = '0.4.4'
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

		tokens = re.findall(
			# '<a href=".*?\/gwt.*?">(.*?)<\/a>',content)
			'<a href="\/url.*?">(.*?)<\/a>',content)

		results = []

		for token in tokens:
			logging.debug('Search.search - found url ' + url)

			results.append((token))

		return results

class Crawl(Search):

	def crawl(self, q, depth = 0):
		"""
		crawl(q, depth = 0) -> generator

		Do google web crawl.
		"""

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


class MungeUsernames(Crawl):
        """
        Create usernames out of the search results
        """

        def mungeusers(self, searchterms):
                """
                set everything to lower case to start
                """

                names_raw = searchterms.lower()
		
		# print "Raw names"
		# print names_raw

		"""
		remove " | linkedin" from each row that has it
		then remove ": directory" from every row that has it
		then remove "profiles" from every row that has it
		assign the leftover values to the name variable
		"""

		matcher = re.match( r'(.*) [\D|\W] linkedin', names_raw, re.M|re.I)

		name = ""

		if matcher:
			match_directory = re.match( r'(.*): directory', matcher.group(1), re.M|re.I)
			match_profiles = re.match( r'(.*) profiles', matcher.group(1), re.M|re.I)
			if  match_directory:
				name = match_directory.group(1)
				# print name
			elif match_profiles:
				name = match_profiles.group(1)
				# print name
			else:
				name = matcher.group(1)
				# print name

		"""
		Break the name up into first and last names.
		create the username variations with the first initial, last name
		and first name, last initial
		"""

		if name != "":
			if not re.search('<|>|\[|\]|\(|\)|\#', name):
				full_name = name.split(" ")

				if len(full_name) == 2:
					fname = full_name[0]
					lname = full_name[1]
					uname = fname[0] + lname
					print uname
					f = open('flast.' + sys.argv[1], 'a')
	                                f.write(uname)
        	                        f.write('\n')

					uname = fname + lname[0]
					print uname
					f = open('firstl.' + sys.argv[1], 'a')
	                                f.write(uname)
        	                        f.write('\n')

					uname = lname + fname[0]
					print uname
					f = open('lastf.' + sys.argv[1], 'a')
                                	f.write(uname)
                                	f.write('\n')
				elif len(full_name) == 3:
					fname = full_name[0]
					mname = full_name[1]
					lname = full_name[2]
					uname = fname[0] + lname
					print uname
					f = open('flast.' + sys.argv[1], 'a')
                                	f.write(uname)
                                	f.write('\n')

					uname = fname + lname[0]
					print uname
					f = open('firstl.' + sys.argv[1], 'a')
                                	f.write(uname)
                                	f.write('\n')

					uname = lname + fname[0]
					print uname
					f = open('lastf.' + sys.argv[1], 'a')
                                	f.write(uname)
                                	f.write('\n')

					uname = fname[0] + mname[0] + lname
					print uname
					f = open('fmlast.' + sys.argv[1], 'a')
                                	f.write(uname)
                                	f.write('\n')
			

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

	u = MungeUsernames()

	search_term = "site:linkedin.com inurl:pub "

	search_company = sys.argv[1]

	search_term +=  sys.argv[1]

	for result in g.crawl(search_term, int(sys.argv[2])):
		# print result
		for entry in result:
	 		u.mungeusers(entry)

		time.sleep(1)

