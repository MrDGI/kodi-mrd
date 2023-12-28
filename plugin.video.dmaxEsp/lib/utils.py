import re
import time
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

def rmSpecialCharts(_text):
	return re.sub(r'\W+', '', _text)

def tFrm(_text):
	_text = _text.encode('utf-8', 'ignore').decode('utf-8').strip()
	_text = str(_text)
	return _text

def dateTime():
	return datetime.now()

def setMinuts(_time, _minuts):
	return _time + timedelta(minutes=_minuts)

def fSeconds(_seconds):
	return int(str( (_seconds / 60) ).split(".")[0])

def fDate(_date):
	return _date.strftime('%d/%m/%Y %H:%M')

def getLastDates(_numDays=2):
	dates = []
	date = dateTime()
	day = date.strftime("%d")
	for i in range(0, (_numDays + 1)):
		nDay = int(day) + i
		nDate = date.replace(day=nDay, hour=0, minute=0, second=0, microsecond=0)
		fDate = nDate.strftime('%Y-%m-%d')
		dates.append(fDate)
	return dates[::-1]

def getOldDates(_numDays=30):
	dates = []
	date = dateTime()
	day = date.strftime("%d")
	for i in range(1, (_numDays + 1)):
		nDay = int(day) + i
		nDate = date - timedelta(days=i)
		fDate = nDate.strftime('%Y-%m-%d')
		dates.append(fDate)
	return dates

def getDate(_hour, _min, _date=''):
	if _date != '':
		curDate = datetime.fromtimestamp(time.mktime(time.strptime(_date, '%Y-%m-%d')))
	else:
		curDate = dateTime()
	return curDate.replace(hour=_hour, minute=_min, second=0, microsecond=0)

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