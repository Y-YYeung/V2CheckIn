#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re

print("Checking in...")

session = requests.session()

# Request header
headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
	'Origin': 'https://www.v2ex.com',
	'Referer': 'https://www.v2ex.com/signin',
	'Host': 'www.v2ex.com',
}

# Get onceToken, which is hidden when presents
response = session.get("https://www.v2ex.com/signin", headers=headers)
soup = BeautifulSoup(response.content, "lxml")
onceToken = soup.find('input',{'name':'once'})['value']
#print('Once Token is: ' + onceToken)

# User data used to sign in
userData = {
	'u': 'Your account',
	'p': 'Your password',
	'once': onceToken,
	'next': '/',
}

# Sign in and get the check in link
session.post('https://www.v2ex.com/signin', data=userData, headers=headers)
response2 = session.get('https://www.v2ex.com/mission/daily', headers=headers)
soup2 = BeautifulSoup(response2.content, "lxml")
#print(soup2)

# Use regular expression to extract the once token used to check in

# 'r' in front of the string: tell compiler that this is a raw string, do not escape it.
# For example, in raw string, "\n" has two charaters: '\' and 'n'
# Here is an attention, the question mark(?) between the string "redeem" and "once", we need to add a '\' in front of it, cause we're using regular expression, otherwise, the result checkinHref is not subscriptable
checkinHref = soup2.find('input',{'onclick':re.compile(r'location.href = \'/mission/daily/redeem\?once=\d{5}\'')})

try:
	redeem = checkinHref['onclick']
	
	missionURL = 'https://www.v2ex.com' + redeem.split("'")[1] # extract the relative url and compose to a absolute url

	# Get check in result
	checkinResultResponse = session.get(missionURL, headers=headers)
	#print(BeautifulSoup(checkinResultResponse.content, "lxml").prettify())
except Exception as ex:
	# We have already checked in
	print("Can not get your redeem, which means you have already checked in ealier today ^_^")
	exit()


# If we did not check in yet before=, print out the result
soup = BeautifulSoup(checkinResultResponse.content, "lxml")
prompt1 = soup.find('div', {'class':'message'})

# If tag only has one navigableString, then use this property to get it, along with blank character
# But with the function `strip()`, we can clear the blank charater on both side
print(prompt1.string.strip()) # 已成功领取

prompt2 = prompt1.find_next_sibling('div').find_next_sibling('div')
print(prompt2.string.strip()) # 已连续登陆


