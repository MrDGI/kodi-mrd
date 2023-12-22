from lib import utils

class Dmax:
	def __init__(self):
		self._token = self.__getToken()
		self._programList = self.__getLastPrograms()
		self._landscape = self.__getLandscape(0)

	def __getToken(self):
		try:
			oToken = utils.getWeb('https://public.aurora.enhanced.live/token?realm=es')
			token = oToken['data']['attributes']['token']
			return token
		except:
			raise Exception('dmax -> getToken --- Error')

	def __getLastPrograms(self):
		try:
			sChannel = utils.getWeb('https://d3ikde5w5w939x.cloudfront.net/programacion/diaria', 'HTML' )
			programList = utils.findAll('<ul class="programas">(.*?)</ul>', sChannel)
			return programList
		except:
			raise Exception('dmax -> getLastPrograms --- Error')

	#def __getProgramItems(self, reload=0):
		#if reload:
			#self.__getLastPrograms()
		#self.programItems = utils.findAll('<li class="programa">(.*?)</li>', self._programList)

	def __getLandscape(self, reload=1):
		try:
			if reload:
				self._programList = self.__getLastPrograms()

			programNow = utils.findAll('<li class="programa now">(.*?)</li>', self._programList)

			incTimeRate = 120 # Represents the time rate to increase (on seconds) before consulting the guide again

			hour = utils.findAll('<span class="tiempo">(.*?)</span>', programNow)
			time = utils.findAll('<span class="duracion">(.*?)</span>', programNow)
			title = utils.findAll('<h3>(.*?)</h3>', programNow)
			episode = utils.findAll('<p class="episode">(.*?)</p>', programNow)
			hTitle  = title + " - " + episode
			sinopsis = utils.findAll('<div class="sinopsis">(.*?)</div>', programNow)
			pegi = utils.findAll('<div class="ico_edad calif_(.*?)" ', programNow)

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
			descTime = "\n[COLOR grey]" + str(fInitProgram) + " · " + str(fEndProgram) + " \t(" + time + ")"
			descSinopsis = "[/COLOR]\n[B][COLOR white]" + sinopsis + "[/COLOR][/B]"
			description =  descTitle + descTime + descSinopsis

			landscape = {'icon': image, 'title': hTitle, 'desc': description, 'timeout': resto}
			return landscape
		except:
			raise Exception('dmax -> Landscape --- Error')

	def getStreaming(self):
		try:
			oMedia = utils.getWeb('https://public.aurora.enhanced.live/playback/channelPlaybackInfo/1?usePreAuth=true', self._token)
			oStream = oMedia['data']['attributes']['streaming'][0]
			return oStream
		except:
			raise Exception('dmax -> getStreaming --- Error')

	def refreshLandscape(self):
		self._landscape = self.__getLandscape(1)
		return self._landscape

	def getLandscape(self):
		return self._landscape