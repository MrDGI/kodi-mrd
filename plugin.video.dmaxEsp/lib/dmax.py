from lib import utils
import xbmc


class Dmax:
	def __init__(self):
		self._token = self.__getToken()
		self._programList = self.__getLastPrograms()
		self._landscape = self.__getLandscape(0)

	def __getToken(self):
		try:
			oToken = utils.getJSON('https://public.aurora.enhanced.live/token?realm=es')
			token = oToken['data']['attributes']['token']
			return token
		except:
			raise Exception('dmax -> getToken --- Error')

	def __getLastPrograms(self):
		try:
			sChannel = utils.getHTML('https://d3ikde5w5w939x.cloudfront.net/programacion/diaria')
			programList = utils.findAll('<ul class="programas">(.*?)</ul>', sChannel)
			return programList
		except:
			raise Exception('dmax -> getLastPrograms --- Error')
		
	def __getItemObject(self, _item):

			incTimeRate = 120 # Represents the time rate to increase (on seconds) before consulting the guide again			

			hour = utils.findAll('<span class="tiempo">(.*?)</span>', _item)
			time = utils.findAll('<span class="duracion">(.*?)</span>', _item)
			title = utils.findAll('<h3>(.*?)</h3>', _item)
			episode = utils.findAll('<p class="episode">(.*?)</p>', _item)
			hTitle  = title + " - " + episode
			sinopsis = utils.findAll('<div class="sinopsis">(.*?)</div>', _item)
			pegi = utils.findAll('<div class="ico_edad calif_(.*?)" ', _item)

			image = "https://d3ikde5w5w939x.cloudfront.net/images/ico_calf_" + str(pegi).lower() + ".gif"

			addMins = int(time.split()[0])
			initHour = int(hour.split(':')[0])
			initMin = int(hour.split(':')[1])
			initProgram = utils.getDate(initHour, initMin)

			endProgram = utils.setMinuts(initProgram, addMins)

			# Start and end dates of the program
			fInitProgram = utils.fDate(initProgram)
			fEndProgram = utils.fDate(endProgram)

			resto = (utils.dateDif(endProgram)).seconds + incTimeRate

			descTitle = "[B][COLOR yellow]" + title + "[/COLOR] - [COLOR blue]" + episode + "[/COLOR][/B]" #+ str(resto)
			descTime = "\n[COLOR grey]" + str(fInitProgram) + " · " + str(fEndProgram) + " \t(" + time + ")[/COLOR]"
			descSinopsis = "\n[B][COLOR white]" + sinopsis + "[/COLOR][/B]"
			description =  descTitle + descTime + descSinopsis

			return {'icon': image, 'title': hTitle, 'desc': description, 'timeout': resto}

	def __getProgramItems(self, reload=0):
		if reload:
			self._programList = self.__getLastPrograms()
		self.programItems = utils.findAll('<li class="programa">(.*?)</li>', self._programList)
  
		programList = []
		xbmc.log("EEEE "+ str(self.programItems))
		for program in self.programItems:
			if (len(program[0]) > 1):
				landscape = self.__getItemObject(program)
				xbmc.log("EEEE "+ landscape)
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

	def getProgramList(self):
		return self.__getProgramItems(0)
		