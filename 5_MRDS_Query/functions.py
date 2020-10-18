from ConfigParser import SafeConfigParser
import sys, os

class LoadLogin:

	def __init__(self, user, pwd):
		#self.user = user
#self.pwd = pwd
		self.login = "login"

	def setLogin ( self, user, pwd):
		fname = os.path.dirname(os.path.abspath(__file__))+ '/config.ini'
		config = SafeConfigParser()
		config.read(fname)
		section  =self.login
		
		if section not in config.sections():
			config.add_section(section)
			config.set(section, 'user', user)
			config.set(section, 'pwd', pwd)
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

		# getfloat() raises an exception if the value is not a float
		#a_float = config.getfloat('main', 'a_float')

		# getint() and getboolean() also do this for their respective types
		#an_int = config.getint('main', 'an_int')




	
