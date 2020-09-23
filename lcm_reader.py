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

class Event:
	def __init__(self, file=None):
		self.event_number = None
		self.timestamp = None
		self.channel = None
		self.data = None
		if file:
			self.read(file)
	
	def read(self, f):
		syncword = f.read(4)
		assert syncword == LCM_SYNCWORD
		
		self.event_number = int.from_bytes(f.read(EVENT_NUMBER_BYTES), 'big')
		self.timestamp = int.from_bytes(f.read(TIMESTAMP_BYTES), 'big')
		
		channel_length = int.from_bytes(f.read(CHANNEL_LENGTH_BYTES), 'big')
		data_length = int.from_bytes(f.read(DATA_LENGTH_BYTES), 'big')
		
		self.channel = f.read(channel_length).decode()
		self.data = f.read(data_length)
		

class LogReader:
	def __init__(self, filepath):
		self.filepath = filepath
		self.file = open(filepath, 'rb')
	
	def __del__(self):
		self.file.close()
	
	def __next__(self):
		try:
			return Event(self.file)
		except:
			return None


class EventIndex:
	def __init__(self, event_number, timestamp, byte_index):
		self.event_number = event_number
		self.timestamp = timestamp
		self.byte_index = byte_index


class LogExtractor:
	def __init__(self, filepath):
		self.reader = LogReader(filepath)
		self.index = []
		self._index()

	def _index(self):
		self.index.clear()
		byte_idx = self.reader.file.tell()
		while ev := next(self.reader):
			self.index.append(EventIndex(ev.event_number, ev.timestamp, byte_idx))
			byte_idx = self.reader.file.tell()
