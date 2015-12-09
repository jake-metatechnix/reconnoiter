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

		self.user_agent = 'User-Agent: Mozilla/5.0 ' \
			+ '(Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.11) ' \
			+ 'Gecko/2009060214 Firefox/3.0.11'

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

		except urllib2.URLError, e:
			print e.code
			print "error"

		return result


class Search(Get):
	"""
	Search

	"""

	def search(self, q, id, num ):

		url = 'http://boss.yahooapis.com/ysearch/web/v1/' + q + '?'

		query = urllib.urlencode({'appid':id, 'format':'xml', 'count':num})

		starturl = url + query

		result = self.get(starturl)
		content = result.read()

		# print content

		"""
		Yahoo only returns a max of 50 results at a time.  So the script has to check to see how many
		results we want, then handle the request on whether or not that's more than 50
		"""
		if num > 50:
			totalhits = re.findall('<resultset_web count="\d*" start="\d*" totalhits="(.*?)" deephits="\d*">', content)
			totalresults = int(totalhits[0])

			tokens = []

			if totalresults < 50:
				tokens = re.findall('<title>(.*?)</title>', content)
				return tokens

			startnum = 0
			while startnum < num:
				"""
				Extract the URL to get to the next page of results
				"""
				uri = re.findall('<nextpage><!\[CDATA\[(.*?)\]\]></nextpage>',content)
				for ur in uri:
					pain = ur[0:]

				baseurl = "http://boss.yahooapis.com"
				fullurl = baseurl + pain

				result = self.get(fullurl)
				content = result.read()

				"""
				Grab the title value from the results
				"""
				itertokens = re.findall('<title>(.*?)</title>', content)
				
				"""
				Add the title values to the tokens array
				"""
				for it in itertokens:
					tokens.append(it)
				startnum = startnum + 50
		else:
			"""
			Less than 50 results desired, so just grab what's on the page
			"""
			tokens = re.findall('<title>(.*?)</title>', content)

		return tokens

class MungeUsernames(Search):
        """
        Create usernames out of the search results
        """

        def mungeusers(self, searchterms):
                """
                set everything to lower case to start
                """

                names_raw = searchterms.lower()
		
		# print names_raw

		"""
		remove " - linkedin" from each row that has it
		then remove ": directory" from every row that has it
		assign the leftover values to the name variable
		"""

		matcher = re.match( r'(.*) [\W|\D] linkedin', names_raw, re.M|re.I)

		name = ""

		if matcher:
			match_directory = re.match( r'(.*): directory', matcher.group(1), re.M|re.I)
			match_profiles = re.match( r'(.*) profiles', matcher.group(1), re.M|re.I)
			if  match_directory:
				name = match_directory.group(1)
			elif match_profiles:
				name = match_profiles.group(1)
			else:
				name = matcher.group(1)

		"""
		Break the name up into first and last names.
		create the username variations with the first initial, last name
		and first name, last initial
		"""

		if name != "":
			# Filter out any results that have HTML in it.  Not likely
			# too be valid and too much of a pain to try to clean up.
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

	if len(sys.argv) < 4:
		print 'usage:', os.path.basename(sys.argv[0]), 'company-name yahoo-api-id #-of-results'

		sys.exit()

	logging.basicConfig()

	companyname = sys.argv[1]
	apiid = sys.argv[2]
	num2get = int(sys.argv[3])

	y = Search()

	u = MungeUsernames()

	search_term = "site:linkedin.com%20inurl:pub%20"

	search_term += companyname

	for result in u.search(search_term, apiid, num2get):
		u.mungeusers(result)


