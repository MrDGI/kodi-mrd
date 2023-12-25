import re
import json
import requests
from requests.auth import AuthBase
from datetime import datetime, timedelta

class __Authenticator(AuthBase):
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

def getHTML(_url, _token=''):
	return __getWeb(_url, 'HTML')

def getJSON(_url, _token=''):
	return __getWeb(_url, 'JSON', _token)

def __getWeb(_url, _type='JSON', _token=''):
	try:
		if _token == '':
			req = requests.get(_url, verify=True)
		else:
			req = requests.get(_url, verify=True, auth=__Authenticator(_token) )

		if _type == 'JSON':
			web_response = req.json()
		else:
			web_response = str(req.text)

		return web_response
	except:
		raise Exception('Unknown error on utils > getWeb')
	
def postWeb(_url, _data='', _token=''):
	try:
		headers = {'Content-type': 'application/json'}
		req = requests.post(_url, data=json.dumps(_data), verify=True, headers=headers, auth=__Authenticator(_token) )
		return req.json()
	except:
		raise Exception('Unknown error on utils > postWeb')

def findAll(pattern, srchText, getList=False):
	try:
		content = re.findall(pattern, srchText, re.DOTALL)
		resp=[]
		if (len(content) > 0):
			if getList:
				resp = content
			else:
				resp = content[0]
		return resp
	except:
		raise Exception('Unknown error on utils > findAll')