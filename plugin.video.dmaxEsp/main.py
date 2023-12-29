import sys
from lib import nav
from lib import dmax
from lib import media
from urllib.parse import parse_qs

def main():
	try:
		args = parse_qs(sys.argv[2][1:])
		type = None


		oOptions = dmax.Dmax()
		oMedia = media.Media(oOptions)
		oMenu = nav.nav(oOptions)

		if 'action' in args:
			type = args['action']

		if type is None:
			oMenu.start()

		elif type[0] == 'seasons':
			slug = str(args['slug'][0])
			wallpaper = str(args['wallpaper'][0])
			oMenu.loadSeasions(slug, wallpaper)

		elif type[0] == 'episodes':
			slug = str(args['slug'][0])
			season = str(args['season'][0])
			wallpaper = ''
			if 'wallpaper' in args:
				wallpaper = str(args['wallpaper'][0])
			oMenu.loadEpisodes(slug, season, wallpaper)

		elif type[0] == 'episode':
			slug = str(args['slug'][0])
			title = str(args['title'][0])
			desc = str(args['desc'][0])
			icon = ''
			if 'icon' in args:
				icon = str(args['icon'][0])
			oMedia.play(slug, title, desc, icon)

		elif type[0] == 'live':
			oMedia.play()

		elif type[0] == 'series':
			oMenu.loadSeries()

		elif type[0] == 'search-series':
			oMenu.searchSeries()

		elif type[0] == 'guide':
			oMenu.loadGuide()

		elif type[0] == 'other-guide':
			slug = str(args['slug'][0])
			oMenu.loadGuide(slug)

	except Exception as e:
		media.log(e)
main()