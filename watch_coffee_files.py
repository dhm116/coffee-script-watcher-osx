from fsevents import Observer, Stream
from subprocess import call
import logging

def callback(event):
	logger = logging.getLogger('FileMonitor')
	#logger.debug('Got: {}'.format(repr(event)))
	
	if 'coffee' in event.name:
		logger.info('Compiling coffeescript: {}'.format(event.name))
		call(['coffee', '-c', event.name])
	elif '.js' in event.name:
		logger.info('Coffeescript compilation complete')

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger('Main')

	location = 'public/javascripts/'
	logger.info('Monitoring for coffeescripts in {}'.format(location))
	
	try:
		observer = Observer()
		observer.daemon = True
		observer.start()
	
		stream = Stream(callback, location, file_events=True)
	
		observer.schedule(stream)
		#observer.join()
		raw_input('')
	except Exception as ex:
		logger.exception('An error has occurred')
	except KeyboardInterrupt:
		logger.info('CTRL-C pressed, exiting application...')
	finally:
		logger.info('Done')