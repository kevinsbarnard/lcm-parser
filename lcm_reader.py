LCM_SYNCWORD = (0xEDA1DA01).to_bytes(4, 'big')
EVENT_NUMBER_BYTES = 8
TIMESTAMP_BYTES = 8
CHANNEL_LENGTH_BYTES = 4
DATA_LENGTH_BYTES = 4

TEST_LOG = 'B:\\Projects\ML-Tracking\\20200720-21_RachelCarson_MiniROV\\lcmLogs.July.21.2020\\lcmlog-2020-07-21.00'

'''
Event structure:
	Header: 28 bytes
	Channel: {channel length} bytes, UTF-8 encoded
	Data: {data length} bytes

Header structure:
	LCM Sync Word: 4 bytes (0xEDA1DA01)
	Event Number: 8 bytes
	Timestamp: 8 bytes
	Channel length: 4 bytes
	Data length: 4 bytes
'''


class Header:
	def __init__(self, event_number, timestamp, channel_length, data_length):
		self.event_number = event_number
		self.timestamp = timestamp
		self.channel_length = channel_length
		self.data_length = data_length


class Event:
	def __init__(self, file):
		self.file = file

		self.header_idx = None

		self.header = None
		self.channel = None
		self.data = None

	def read(self, read_data=True):
		self.header_idx = self.file.tell()

		# Ensure syncword
		syncword = self.file.read(4)
		assert syncword == LCM_SYNCWORD

		# Read header data
		event_number = int.from_bytes(self.file.read(EVENT_NUMBER_BYTES), 'big')
		timestamp = int.from_bytes(self.file.read(TIMESTAMP_BYTES), 'big')
		channel_length = int.from_bytes(self.file.read(CHANNEL_LENGTH_BYTES), 'big')
		data_length = int.from_bytes(self.file.read(DATA_LENGTH_BYTES), 'big')
		self.header = Header(event_number, timestamp, channel_length, data_length)

		# Read channel
		self.channel = self.file.read(channel_length).decode()

		# Read data if read_data is True, else seek past data
		if read_data:
			self.data = self.file.read(data_length)
		else:
			self.file.seek(data_length, whence=1)
		

class LogReader:
	def __init__(self, filepath):
		self.filepath = filepath
		self.file = open(filepath, 'rb')
	
	def __del__(self):
		self.file.close()
	
	def next(self, read_data=True):
		try:
			ev = Event(self.file)
			ev.read(read_data=read_data)
		except:
			return None


class LogExtractor:
	def __init__(self, filepath):
		self.reader = LogReader(filepath)
		self.index = []
		self._index()

	def _index(self):
		self.index.clear()
		print('Indexing {}, this may take some time...'.format(self.reader.filepath))
		while ev := self.reader.next(read_data=False):
			self.index.append(ev)
