import sys
import xbmc
import xbmcgui
import xbmcplugin

def log(_message):
	xbmc.log(_message)

class Media:
	def __init__(self, oMedia):
		self._player = xbmc.Player()
		self._media = oMedia
		self._landscape = self._media.getLandscape()

	def __call__(self):
		player = self._player
		player.setVideoStream(1)
		return player

	def __getLayoutItem(self, _item):
		landscape = self._landscape
		if len(landscape) >= 3:
			_item.setArt({'thumb': landscape['icon']})
			linfo = _item.getVideoInfoTag()
			linfo.setTitle(landscape['title'])
			linfo.setPlot(landscape['desc'])
			return _item

	def __getLayout(self):
		newItem = xbmcgui.ListItem()
		return self.__getLayoutItem(newItem)

	def __updateMediaInfo(self):
		player = self._player
		currentItem = player.getPlayingItem()
		player.updateInfoTag( self.__getLayoutItem(currentItem) )

	def __refeshLandscape(self):
		self._landscape = self._media.refreshLandscape()
		self.__updateMediaInfo()

	def __refreshPlay(self):
		player = self._player
		monitor = xbmc.Monitor()
		while player.isPlaying():
			landscape = self._landscape
			monitor.waitForAbort(landscape['timeout'])
			if player.isPlaying():
				self.__refeshLandscape()

	def play(self, autoRefresh=1):
		try:
			stream = self._media.getStreaming()
			data = {'url': '', 'type': ''}
			if len(stream) >= 2:
				data = {'url': stream['url'], 'type': stream['type']}

			player = self._player
			mime = 'application/video'
			if data['type'] == 'dash':
				mime = 'application/xml+dash'
			if data['type'] == 'hls':
				mime = 'aplicación/x-mpegURL'

			streaming = xbmcgui.ListItem(label='media',path=data['url'],offscreen=True)
			streaming.setMimeType(mime)
			streaming.setProperty("isPlayable", "true")
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, streaming)
			playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
			playlist.clear()
			playlist.add(streaming.getPath(), self.__getLayout() )
			play = player.play(playlist)
			if autoRefresh:
				self.__refreshPlay()
			return play
		except:
			raise Exception('Unknown error on play > media')