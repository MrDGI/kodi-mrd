import xbmcaddon
from lib import utils

class Dmax:
	def __init__(self):
		self._token = self.__getToken()
		self._programList = self.__getLastPrograms()
		self._landscape = self.__getLandscape(0)
		self._addon = xbmcaddon.Addon()

	def __getSettingString(self, _name):
		return self._addon.getSettings(_name)

	def __getSettingInt(self, _name):
		return self._addon.getSettingInt(_name)

	def __getSettingBool(self, _name):
		return self._addon.getSettingBool(_name)

	def __getToken(self):
		try:
			oToken = utils.getJSON('https://public.aurora.enhanced.live/token?realm=es')
			token = oToken['data']['attributes']['token']
			return token
		except:
			raise Exception('dmax -> getToken --- Error')

	def __getLastPrograms(self, _date=''):
		try:
			if _date != '':
				_date = '?date=' + _date
			sChannel = utils.getHTML('https://d3ikde5w5w939x.cloudfront.net/programacion/diaria' + _date)
			programList = utils.findAll('<ul class="programas">(.*?)</ul>', sChannel)
			return programList
		except:
			raise Exception('dmax -> getLastPrograms --- Error')
		
	def __getItemObject(self, _item, _date=''):

			incTimeRate = 120 # Represents the time rate to increase (on seconds) before consulting the guide again			

			hour = utils.findAll('<span class="tiempo">(.*?)</span>', _item)
			time = utils.findAll('<span class="duracion">(.*?)</span>', _item)
			title = utils.tFrm( utils.findAll('<h3>(.*?)</h3>', _item) )
			episode = utils.tFrm( utils.findAll('<p class="episode">(.*?)</p>', _item) )
			hTitle  = title + " - " + episode
			sinopsis = utils.findAll('<div class="sinopsis">(.*?)</div>', _item)
			pegi = utils.findAll('<div class="ico_edad calif_(.*?)" ', _item)

			image = "https://d3ikde5w5w939x.cloudfront.net/images/ico_calf_" + str(pegi).lower() + ".gif"

			addMins = int(time.split()[0])
			initHour = int(hour.split(':')[0])
			initMin = int(hour.split(':')[1])
			initProgram = utils.getDate(initHour, initMin, _date)

			endProgram = utils.setMinuts(initProgram, addMins)

			# Start and end dates of the program
			fInitProgram = utils.fDate(initProgram)
			fEndProgram = utils.fDate(endProgram)

			resto = (utils.dateDif(endProgram)).seconds + incTimeRate

			descTitle = "[B][COLOR yellow]" + title + "[/COLOR] - [COLOR blue]" + episode + "[/COLOR][/B]" #+ str(resto)
			descTime = "\n[COLOR grey]" + str(fInitProgram) + " · " + str(fEndProgram) + " \t(" + time + ")[/COLOR]"
			descSinopsis = "\n[B][COLOR white]" + sinopsis + "[/COLOR][/B]"
			description =  descTitle + descTime + descSinopsis

			return {'icon': image, 'title': hTitle, 'desc': description, 'time': descTime, 'timeout': resto, 'oTitle': title, 'oDesc': episode}

	def __getProgramItems(self, _date=''):
		dateProgramList = self._programList
		if _date != '':
			dateProgramList = self.__getLastPrograms(_date)
		programItems = utils.findAll('<li class="programa">(.*?)</li>', dateProgramList, True)

		programList = []
		for program in programItems:
			landscape = self.__getItemObject(program, _date)
			programList.append(landscape)
		return programList

	def __getLandscape(self, reload=1):
		try:
			if reload:
				self._programList = self.__getLastPrograms()

			programNow = utils.findAll('<li class="programa now">(.*?)</li>', self._programList)
			landscape = self.__getItemObject(programNow)

			return landscape
		except:
			raise Exception('dmax -> Landscape --- Error')
		
	def getSeries(self):
		try:
			oSeriesContent = utils.getJSON('https://it-api.loma-cms.com/feloma/page/series/?environment=dmaxspain&v=2')
			oSeriesCollection = oSeriesContent['blocks'][0]['items']
			return oSeriesCollection
		except:
			raise Exception('dmax -> getSeries --- Error')
		
	def getEpisodes(self, _slug):
		try:
			oEpisodesContent = utils.getJSON('https://it-api.loma-cms.com/feloma/page/' + _slug + '/?environment=dmaxspain&parent_slug=series&v=2')
			oEpisodesCollection = oEpisodesContent['blocks'][1]['items']
			return oEpisodesCollection
		except:
			raise Exception('dmax -> getEpisodes --- Error')
		
	def getEpisode(self, _episode):
		try:
			data = {"videoId":str(_episode)}
			oMedia = utils.postWeb('https://public.aurora.enhanced.live/playback/v3/videoPlaybackInfo', data, self._token)
			oStream = oMedia['data']['attributes']['streaming'][0]
			return oStream
		except:
			raise Exception('dmax -> getEpisode --- Error')

	def getStreaming(self):
		try:
			oMedia = utils.getJSON('https://public.aurora.enhanced.live/playback/channelPlaybackInfo/1?usePreAuth=true', self._token)
			oStream = oMedia['data']['attributes']['streaming'][0]
			return oStream
		except:
			raise Exception('dmax -> getStreaming --- Error')

	def refreshLandscape(self):
		self._landscape = self.__getLandscape(1)
		return self._landscape

	def getLandscape(self):
		return self._landscape

	def getOldPrograms(self):
		numDays = self.__getSettingInt('guideOldDates')
		return utils.getOldDates(numDays)

	def getNewPrograms(self):
		return utils.getLastDates()

	def getProgramList(self, _date=''):
		return self.__getProgramItems(_date)

	def getAutoSearchValue(self):
		return self.__getSettingBool('searchGuidePrograms')
		