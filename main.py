from lib import dmax
from lib import media

def main():
	try:
		oDmax = dmax.Dmax()
		oMedia = media.Media(oDmax)
		oMedia.play()
	except ValueError as e:
		media.log(e)

main()