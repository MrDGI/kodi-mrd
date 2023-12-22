import re
import requests
import threading
from requests.auth import AuthBase
from datetime import datetime, timedelta

class Authenticator(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['authorization'] = "Bearer " + self.token
        return r

def dateTime():
	return datetime.now()

def setMinuts(_time, _minuts):
	return _time + timedelta(minutes=_minuts)

def fSeconds(_seconds):
	return int(str( (_seconds / 60) ).split(".")[0])

def fDate(_date):
	return _date.strftime("%m/%d/%Y %H:%M")

def getDate(_hour, _min):
	return dateTime().replace(hour=_hour, minute=_min, second=0, microsecond=0)

def dateDif(_dEnd):
	return _dEnd - dateTime()

def getWeb(_url, _type='JSON'):
	getWeb(_url, '', _type)

def getWeb(_url, _token='', _type='JSON'):
	try:
		if _token == '':
			req = requests.get(_url, verify=True)
		else:
			req = requests.get(_url, verify=True, auth=Authenticator(_token) )

		if _type == 'JSON':
			web_response = req.json()
		else:
			web_response = str(req.text)

		return web_response
	except:
		raise Exception('Unknown error on utils > getWeb')

def findAll(pattern, srchText):
	try:
		content = re.compile(pattern, re.DOTALL).findall(srchText)
		return content[0]
	except:
		raise Exception('Unknown error on utils > findAll')