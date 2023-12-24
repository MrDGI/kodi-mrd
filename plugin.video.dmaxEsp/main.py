from lib import dmax
from lib import media
from lib import nav

def main(_episode=''):
	try:
		oDmax = dmax.Dmax()
		oMedia = media.Media(oDmax)


		if _episode == '':
			oMedia.play()	
		else:
			
			series = oDmax.getSeries()
			for serie in series:
				title = serie['title']
				subtitle = serie['subtitle']
				slug = serie['slug']
				episodes = oDmax.getEpisodes(slug)
				for episode in episodes:
					sid = episode['id']
					title = episode['title']
					desc = episode['description']
					temporada = episode['seasonNumber']
					episodio = episode['episodeNumber']
					if episode['poster']:
						icon = episode['poster']['src']

				landscape = serie['metaMedia'][0]['media']['url']
				portrait = serie['metaMedia'][1]['media']['url']
					
					
			oMedia.play(_episode)
			
	except Exception as e:
		media.log(e)
#"1647"
#main()

oDmax = dmax.Dmax()
oMedia = media.Media(oDmax)
menu = nav.nav(oDmax, oMedia)
menu.start()