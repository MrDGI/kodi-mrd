import xbmcgui
import xbmcplugin
import sys
import urllib.parse as urllib
from lib import utils

class nav:
	def __init__(self, oOptions):
		self._oOptions = oOptions
		self._urlBase = sys.argv[0]
		self._handle = int(sys.argv[1])
		self._series = ''
		self._slug = ''
		self._episodes = ''
         
	def __addItemMenu(self, _title, _desc, _thumbnail, _wallpaper, _url, _isPlayable='false', _isFolder=False):
		if _title is None:
			_title = _desc.replace('\n', '')
		if _title is not None and _desc is not None:
			_title = _title + ": " + _desc.replace('\n', ' ').replace('\t', ' ')
		newItem = xbmcgui.ListItem(_title)
		newItem.setArt({ 'title': _title, 'thumb': _thumbnail, 'poster': _thumbnail, 'fanart': _wallpaper, 'banner': _wallpaper })
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
	
	def __loadOptGuide(self):
		title = "[Guia] (Guide)"
		openUrl = self.__buildUrl( {'action': 'guide'} )
		self.__addItemMenu(title, '', '', '', openUrl, 'false', True)

	def __tFrm(self, _text):
		_text = str(_text)
		_text = utils.rmSpecialCharts(_text)
		_text = _text.replace(" ", "").lower()
		_text = utils.tFrm( _text )
		return _text

	def __searchProgram(self, _title, _desc):
		_title = self.__tFrm(_title)
		_desc = self.__tFrm(_desc)
		slug = ''
		landscape = ''
		if self._series == '':
			self._series = self._oOptions.getSeries()
		for serie in self._series:
			title = self.__tFrm(serie['title'])
			if title in _title:
				slug = str(serie['slug'])
				landscape = serie['metaMedia'][0]['media']['url']
				break
		resp = ''
		if slug != '':
			if self._slug != slug:
				self._slug = slug
				self._episodes = self._oOptions.getEpisodes(self._slug)
			
			for episode in self._episodes:
				eTitle = episode['title']
				efTitle = self.__tFrm(eTitle)
				desc = episode['description']
				if efTitle in _desc:
					epiNumber = episode['episodeNumber']
					season = episode['seasonNumber']
					nTitle = "[T{0}E{1}] {2}".format(season, epiNumber, eTitle)
					icon = ''
					if 'poster' in episode and episode['poster'] is not None:
						icon = episode['poster']['src']
					resp = {'icon': icon, 'wallpaper': landscape, 'media': self.__buildUrl( {'action': 'episode', 'slug': str(episode['id']), 'title': nTitle, 'desc': desc, 'icon': icon} )}
					break
		return resp

	def __loadOldGuides(self):
		programDates = self._oOptions.getOldPrograms()
		for program in programDates:
			date = str(program)
			openUrl = self.__buildUrl({'action': 'other-guide', 'slug': date})
			self.__addItemMenu(date, '', '', '', openUrl, 'false', True)

	def __loadNewGuides(self):
		programDates = self._oOptions.getNewPrograms()
		for program in programDates:
			date = str(program)
			openUrl = self.__buildUrl({'action': 'other-guide', 'slug': date})
			self.__addItemMenu(date, '', '', '', openUrl, 'false', True)

	def __loadGuide(self, _date=''):
		programList = self._oOptions.getProgramList(_date)
		autoSearch = self._oOptions.getAutoSearchValue()
		for program in programList:
			title = str(program['title'])
			icon = str(program['icon'])
			desc = str(program['desc'])
			time = str(program['time'])
			openUrl = self.__buildUrl({})
			wallpaper = ''
			if autoSearch:
				direct = self.__searchProgram(str(program['oTitle']), str(program['oDesc']))
				if direct != '':
					openUrl = direct['media']
					icon = str(direct['icon'])
					wallpaper = str(direct['wallpaper'])
			self.__addItemMenu( utils.tFrm(title) , time, icon, wallpaper, openUrl, 'false', False)

	def __loadOptLive(self):
		landscape = self._oOptions.getLandscape()
		title = '[Directo] (Live)' + landscape['title']
		icon = landscape['icon']
		openUrl = self.__buildUrl( {'action': 'live'} )
		self.__addItemMenu(title,'', icon, '', openUrl, 'false', False)

	def __loadSeries(self):
		if self._series == '':
			self._series = self._oOptions.getSeries()
		ordeSeries = sorted(self._series, key=self.__getTitle)
		for serie in ordeSeries:
			title = str(serie['title'])
			subtitle = serie['subtitle']
			landscape = serie['metaMedia'][0]['media']['url']
			portrait = serie['metaMedia'][1]['media']['url']
			openUrl = self.__buildUrl( {'action': 'seasons', 'slug': str(serie['slug']), 'wallpaper': landscape} )
			self.__addItemMenu(title, subtitle, portrait, landscape, openUrl, 'false', True)

	def __loadSeasons(self, _slug, _wallpaper=''):
		episodes = self._oOptions.getEpisodes(_slug)
		orderEpisodes = sorted(episodes, key=self.__getTempEpi)
		seasons = []
		for episode in orderEpisodes:
			season = episode['seasonNumber']
			if season not in seasons:
				nTitle = 'Temporada ' + str(season)
				icon = ''
				if 'poster' in episode and episode['poster'] is not None:
					icon = episode['poster']['src']
				openUrl = self.__buildUrl( {'action': 'episodes', 'slug': str(_slug), 'season': str(season), 'wallpaper': _wallpaper } )
				self.__addItemMenu(nTitle, '', icon, _wallpaper, openUrl, 'false', True)
				seasons.append(season)

	def __loadEpisodes(self, _slug, _season, _wallpaper=''):
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
				if 'poster' in episode and episode['poster'] is not None:
					icon = episode['poster']['src']
				openUrl = self.__buildUrl( {'action': 'episode', 'slug': str(episode['id']), 'title': nTitle, 'desc': desc, 'icon': icon} )
				self.__addItemMenu(nTitle, desc, icon, _wallpaper, openUrl, 'false', False)

	def start(self):
		self.__loadOptGuide()
		self.__loadOptLive()
		self.__loadSeries()
		xbmcplugin.endOfDirectory(self._handle)

	def loadSeasions(self, _slug, _wallpaper=''):
		self.__loadSeasons(_slug, _wallpaper)
		xbmcplugin.endOfDirectory(self._handle)

	def loadEpisodes(self, _slug, _season, _wallpaper=''):
		self.__loadEpisodes(_slug, _season, _wallpaper)
		xbmcplugin.endOfDirectory(self._handle)

	def loadGuide(self, _date=''):
		if _date == '':
			self.__loadNewGuides()
			self.__loadOldGuides()
		else:
			self.__loadGuide(_date)
		xbmcplugin.endOfDirectory(self._handle)
