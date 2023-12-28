import sys
from lib import nav
from lib import dmax
from lib import media
from urllib.parse import parse_qs

def main():
	try:
		args = parse_qs(sys.argv[2][1:])
		oOptions = dmax.Dmax()
		oMedia = media.Media(oOptions)
		oMenu = nav.nav(oOptions)
		type = None

		if len(args) > 0:
			type = args['action']

		if type is None:
			oMenu.start()

		elif type[0] == 'seasons':
			slug = str(args['slug'][0])
			oMenu.loadSeasions(slug)

		elif type[0] == 'episodes':
			slug = str(args['slug'][0])
			season = str(args['season'][0])
			oMenu.loadEpisodes(slug, season)

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
			
		elif type[0] == 'guide':
			oMenu.loadGuide()

		elif type[0] == 'other-guide':
			slug = str(args['slug'][0])
			oMenu.loadGuide(slug)

	except Exception as e:
		media.log(e)
main()