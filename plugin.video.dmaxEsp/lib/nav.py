import xbmc
import xbmcgui
import xbmcplugin
import sys
import urllib.parse as urllib

class nav:
	def __init__(self, oOptions, oMedia):
		self._oOptions = oOptions
		self._oMedia = oMedia
		self._urlBase = sys.argv[0]
		self._handle = int(sys.argv[1])
         
	def __addItemMenu(self, _label, _thumbnail, _url, _isPlayable='false', _isFolder=False):
		newItem = xbmcgui.ListItem(_label)
		newItem.setArt({ 'thumb': _thumbnail})
		newItem.setProperty('IsPlayable', _isPlayable)
		newItem.setIsFolder(_isFolder)
		xbmcplugin.addDirectoryItem(self._handle, listitem=newItem, url=_url, isFolder=_isFolder)

	def __getTitle(self, _item):
		return str(_item['title'])

	def __getTempEpi(self, _item):
		temp = _item['seasonNumber']
		epi = _item['episodeNumber']
		return (int(temp), int(epi))
	
	def __buildUrl(self, _query):
		return self._urlBase + '?' + urllib.urlencode(_query)
	
	def __loadGuide(self):
		programList = self._oOptions.getProgramList()
		for program in programList:
			title = program['title']
			icon = program['icon']
			desc = program['desc']	
			self.__addItemMenu(title, icon, '', 'false', True)

	def __loadOptGuide(self):
		internalUrl = self.__buildUrl( {'action': 'guide', 'slug': '' } )
		title = "[Gia] (Guide)"
		self.__addItemMenu(title, '', internalUrl, 'false', False)

	def __loadOptLive(self):
		landscape = self._oOptions.getLandscape()
		title = '[Directo] (Live)' + landscape['title']
		icon = landscape['icon']
		internalUrl = self.__buildUrl( {'action': 'live', 'slug': '' } )
		self.__addItemMenu(title, icon, internalUrl, 'false', False)

	def __loadSeries(self):
		series = self._oOptions.getSeries()
		ordeSeries = sorted(series, key=self.__getTitle)
		for serie in ordeSeries:
			title = str(serie['title'])
			subtitle = serie['subtitle']
			landscape = serie['metaMedia'][0]['media']['url']
			portrait = serie['metaMedia'][1]['media']['url']
			openUrl = self.__buildUrl( {'action': 'seasons', 'slug': str(serie['slug'])} )
			self.__addItemMenu(title, portrait, openUrl, 'false', True)

	def __loadSeasons(self, _slug):
		episodes = self._oOptions.getEpisodes(_slug)
		orderEpisodes = sorted(episodes, key=self.__getTempEpi)
		seasons = []
		for episode in orderEpisodes:
			season = episode['seasonNumber']
			if season not in seasons:
				nTitle = 'Temporada ' + str(season)
				icon = ''
				if episode['poster']:
					icon = episode['poster']['src']
				internalUrl = self.__buildUrl( {'action': 'episodes', 'slug': str(_slug), 'season': str(season) } )
				self.__addItemMenu(nTitle, icon, internalUrl, 'false', True)
				seasons.append(season)

	def __loadEpisodes(self, _slug, _season):
		episodes = self._oOptions.getEpisodes(_slug)
		orderEpisodes = sorted(episodes, key=self.__getTempEpi)
		for episode in orderEpisodes:
			season = str(episode['seasonNumber'])
			if season == str(_season):
				title = episode['title']
				desc = episode['description']
				epiNumber = episode['episodeNumber']
				nTitle = "[T{0}E{1}] {2}".format(season, epiNumber, title)
				icon = ''
				if episode['poster']:
					icon = str(episode['poster']['src'])
				internalUrl = self.__buildUrl( {'action': 'episode', 'slug': str(episode['id']), 'title': nTitle, 'desc': desc, 'icon': icon} )
				self.__addItemMenu(nTitle, icon, internalUrl, 'false', False)

	def loadGuide(self):
		self.__loadGuide()
		xbmcplugin.endOfDirectory(self._handle)

	def start(self):
		#self.__loadOptGuide()
		self.__loadOptLive()
		self.__loadSeries()
		xbmcplugin.endOfDirectory(self._handle)

	def loadSeasions(self, _slug):
		self.__loadSeasons(_slug)
		xbmcplugin.endOfDirectory(self._handle)

	def loadEpisodes(self, _slug, _season):
		self.__loadEpisodes(_slug, _season)
		xbmcplugin.endOfDirectory(self._handle)
    
#xbmcplugin.addDirectoryItems()