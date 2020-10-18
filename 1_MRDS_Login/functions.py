from ConfigParser import *
import sys, os

class LoadLogin:

	def __init__(self):
		#self.user = user
        #self.pwd = pwd
		self.login = "login"

	def setLogin ( self, user, pwd, server):
		fname = os.path.dirname(os.path.abspath(__file__))+ '/config.ini'
		config = SafeConfigParser()
		config.read(fname)
		section  =self.login

		if section not in config.sections():
			config.add_section(section)
    		config.set(section, 'user', user)
    		config.set(section, 'pwd', pwd)
    		config.set(section,'server',server)
    		with open(fname, 'w') as f:
    			config.write(f)

	def getLoginUser( self):

		config = SafeConfigParser()
		fname = os.path.dirname(os.path.abspath(__file__))+ '/config.ini'
		config.read(fname)
		section='login'

		try:
			user = config.get(section, 'user')
		except NoSectionError, NoOptionError:
			user = None
		return(user)

	def getLoginPwd( self):

		config = SafeConfigParser()
		fname = os.path.dirname(os.path.abspath(__file__))+ '/config.ini'
		config.read(fname)
		section='login'

		try:
			pwd = config.get(section, 'pwd')
		except NoSectionError, NoOptionError:
			pwd = None

		return(pwd)

	def getLoginServer( self):

		config = SafeConfigParser()
		fname = os.path.dirname(os.path.abspath(__file__))+ '/config.ini'
		config.read(fname)
		section='login'

		try:
			server = config.get(section, 'server')
		except NoSectionError, NoOptionError:
			server = None

		return(server)

		# getfloat() raises an exception if the value is not a float
		#a_float = config.getfloat('main', 'a_float')

		# getint() and getboolean() also do this for their respective types
		#an_int = config.getint('main', 'an_int')





