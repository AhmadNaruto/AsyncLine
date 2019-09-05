# -*- coding: utf-8 -*-
from . import config
from .http_client import HttpClient
from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory
from frugal.provider import FServiceProvider
from frugal.context import FContext
from .proto import LegyProtocolFactory
from .lib.Gen import f_LineService

class Connection(object):
	def __init__(self, uri_path):
		self.context = FContext()
		self.transport = HttpClient(config.BASE_URL + uri_path)
		self.protocol_factory = TCompactProtocolAcceleratedFactory()
		self.wrapper_factory  = LegyProtocolFactory(self.protocol_factory)
		self.service_provider = FServiceProvider(self.transport, self.wrapper_factory)
		self.client = self.ClientFactory()
		
	def call(self, rfunc: str, *args, **kws) -> callable:
		assert isinstance(rfunc, str), 'Function name must be str not '+type(rfunc).__name__
		rfr = getattr(self.client, rfunc, None)
		if rfr:
			return rfr(self.context, *args, **kws)
		else:
			raise Exception(rfunc + ' is not exist')

	def renew(self):
		self.client = self.ClientFactory()

	def ClientFactory(self):
		return f_LineService.Client(self.service_provider)
		
	def setHeaders(self, dict_key_val):
		self.transport._headers = dict_key_val
		
	def updateHeaders(self, dict_key_val):
		self.transport._headers.update(dict_key_val)
		
	def url(self, path='/'):
		self.transport._url = config.BASE_URL + path