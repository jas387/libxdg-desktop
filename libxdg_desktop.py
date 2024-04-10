import os


class LocaleString:
	'''
	 Name=Foo
	 Name[sr_YU]=...
	 Name[sr@Latn]=...
	 Name[sr]=...
	'''
	def __init__(self, name: str):
		self.key = name
		self.value = None
		self.values = {}

	def add(self, line: str):
		key, value = line.split('=', maxsplit=1)
		if '[' in key:
			key, locale = key.split('[',maxsplit=1)
			locale = locale[:-1]
		else:
			locale = None
		
		if key == self.key:
			if locale is None:
				self.value = value.strip()
			else:
				self.values[locale]=value.strip()

	def get(self, locale: str=None):
		if locale is None:
			return self.value
		else:
			return self.values[locale]

	def set(self, value: str=None, locale: str=None):
		if locale is None:
			self.value = value
		else:
			self.values[locale]=value

	def __str__(self):
		string=f'''{self.key}: {self.value}'''
		if len(self.values.keys())>0:
			for locale,value in self.values.items():
				string+=f'''
			{self.key}[{locale}]: {value}'''
		return string

class Desktop:
	def __init__(self, path: str):
		if not os.path.isfile(path):
			raise OSError(f'path: {path}')
		if not path.endswith('.desktop'):
			raise ValueError(f'no valid desktop file: {path}')
		self.__path = path # internal path to .desktop
		self.type = None # MUST HAVE
		self.version = None
		self.name = LocaleString('Name') # MUST HAVE
		self.generic_name = LocaleString('GenericName')
		self.no_display = False
		self.comment = LocaleString('Comment')
		self.icon = None
		self.hidden = False
		self.only_showin = None
		self.not_showin = None
		self.dbus_activatable = False
		self.try_exec = None
		self.exec = None
		self.path = None
		self.terminal = False
		self.actions = None
		self.mime_type = None
		self.categories = None
		self.implements = None
		self.keywords = LocaleString('Keywords')
		self.startup_notify = False
		self.startup_wm_class = None
		self.url = None
		self.prefers_non_default_gpu = False
		self.single_main_window = False
		self.load()

	def __str__(self):
		return f'''
			Type: {self.type}
			Version: {self.version}
			Name: {self.name}
			GenericName: {self.generic_name}
			NoDisplay: {self.no_display}
			Comment: {self.comment}
			Icon: {self.icon}
			Hidden: {self.hidden}
			OnlyShowIn: {self.only_showin}
			NotShowIn: {self.not_showin}
			DBusActivatable: {self.dbus_activatable}
			TryExec: {self.try_exec}
			Exec: {self.exec}
			Path: {self.path}
			Terminal: {self.terminal}
			Actions: {self.actions}
			MimeType: {self.mime_type}
			Categories: {self.categories}
			Implements: {self.implements}
			Keywords: {self.keywords}
			StartupNotify: {self.startup_notify}
			StartupWMClass: {self.startup_wm_class}
			URL: {self.url}
			PrefersNonDefaultGPU: {self.prefers_non_default_gpu}
			SingleMainWindow: {self.single_main_window}
			'''

	def load(self):
		'load .desktop file info'
		with open(self.__path, 'r') as file:
			for line in file.readlines():
				if '[Desktop Entry]' in line:
					continue
				try:
					key, value = line.split('=', maxsplit=1)
				except ValueError as e:
					print(line, e.args)
					continue
				key = key.strip()
				if '[' in key:
					key = key.split('[')[0] 
				value = value.strip()
				match(key):
					case 'Type':
						self.type = value
					case 'Version':
						self.version = value
					case 'Name':
						self.name.add(line)
					case 'GenericName':
						self.generic_name.add(line)
					case 'NoDisplay':
						self.no_display = (value=='true')
					case 'Comment':
						self.comment.add(line)
					case 'Icon':
						self.icon = value
					case 'Hidden':
						self.hidden = value=='true'
					case 'OnlyShowIn':
						self.only_showin = value
					case 'NotShowIn':
						self.not_showin = value
					case 'DBusActivatable':
						self.dbus_activatable = value=='true'
					case 'TryeExec':
						self.try_exec = value
					case 'Exec':
						self.exec = value
					case 'Path':
						self.path = value
					case 'Terminal':
						self.terminal = value=='true'
					case 'Actions':
						self.actions = value
					case 'MimeType':
						self.mime_type = value
					case 'Categories':
						self.categories = value
					case 'Implements':
						self.implements = value
					case 'Keywords':
						self.keywords.add(line)
					case 'StartupNotify':
						self.startup_notify = value == 'true'
					case 'StartupWMClass':
						self.startup_wm_class = value
					case 'URL':
						self.url = value
					case 'PrefersNonDefaultGPU':
						self.prefers_non_default_gpu = value=='true'
					case 'SingleMainWindow':
						self.single_main_window = value=='true'
					case _:
						print('invalid:',key,value)
						pass

