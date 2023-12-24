import xbmc
import xbmcgui
import xbmcplugin
import sys
from urllib.parse import urlparse

class nav:
	def __init__(self, oOptions, oMedia):
		self._oOptions = oOptions
		self._oMedia = oMedia
		self._urlBase = sys.argv[0]
		self._handle = int(sys.argv[1])
		#self._args = urlparse.parse_qs(sys.argv[2][1:])
         
	def __addItemMenu(self, _label, _thumbnail, _url, _isPlayable='false', _isFolder=False):
		newItem = xbmcgui.ListItem(_label)
		newItem.setArt({ 'thumb': _thumbnail})
		newItem.setProperty('IsPlayable', _isPlayable)
		newItem.setIsFolder(_isFolder)
		xbmcplugin.addDirectoryItem(self._handle, listitem=newItem, url=_url, isFolder=_isFolder)
        
	def __loadLive(self):
		self.__addItemMenu('[Directo]', '', '', 'true')

	def __getTitle(self, _itemTitle):
		return str(_itemTitle['title'])

	def __loadSeries(self):
		series = self._oOptions.getSeries()
		ordeSeries = sorted(series, key=self.__getTitle)
		for serie in ordeSeries:
			title = str(serie['title'])
			subtitle = serie['subtitle']
			slug = str(serie['slug'])
			landscape = serie['metaMedia'][0]['media']['url']
			portrait = serie['metaMedia'][1]['media']['url']            
			self.__addItemMenu(title, landscape, slug, 'false', True)

	def start(self):
		self.__loadLive()
		self.__loadSeries()
		xbmcplugin.endOfDirectory(self._handle)
    
#xbmcplugin.addDirectoryItems()