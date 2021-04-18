import struct
from enum import auto
from .messageid import MessageIdEnum


class CreateMessage:
	"""Create a bittorrent protocol message
	"""

	@staticmethod
	def create_message(message_id: auto, data=b"") -> bytes:
		"""Add the data length and message id to the beginning of the data argument

		Args:
			message_id (auto): member variables of the MessageIdEnum class
			data (bytes, optional): binary after message id. Defaults to b"".

		Returns:
			bytes: binary with data length and message id added to the data argument
		"""
		length = len(data) + 1  # add 1 byte of message_id
		return struct.pack(">IB", length, message_id.value) + data

	@staticmethod
	def handshake(info_hash: bytes, peer_id: bytes) -> bytes:
		"""Create handshake message

		Args:
			info_hash (bytes): sha1 hash of torrentfile info dictionary
			peer_id (bytes): unique id of the client generated at startup

		Returns:
			bytes: handshake message
		"""
		encoding = "ascii"
		ptsr = "BitTorrent protocol".encode(encoding)
		ptstlen = struct.pack(">B", len(ptsr))
		empty = bytes(8)
		handshake = ptstlen + ptsr + empty + info_hash + peer_id
		return handshake

	@classmethod
	def choke(cls) -> bytes:
		"""Create choke message

		Returns:
			bytes: choke message
		"""
		return cls.create_message(MessageIdEnum.CHOKE)

	@classmethod
	def unchoke(cls) -> bytes:
		"""Create unchoke message

		Returns:
			bytes: unchoke message
		"""
		return cls.create_message(MessageIdEnum.UNCHOKE)

	@classmethod
	def interest(cls) -> bytes:
		"""Create interest message

		Returns:
			bytes: interest message
		"""
		return cls.create_message(MessageIdEnum.INTEREST)

	@classmethod
	def nointerest(cls) -> bytes:
		"""Create nointerest message

		Returns:
			bytes: nointerest message
		"""
		return cls.create_message(MessageIdEnum.NOINTEREST)

	@classmethod
	def have(cls, index: int) -> bytes:
		"""Create have message

		Args:
			index (int): piece index

		Returns:
			bytes: have message
		"""
		data = struct.pack(">I", index)
		return cls.create_message(MessageIdEnum.HAVE, data)

	@classmethod
	def bitfield(cls, bitfield: bytes) -> bytes:
		"""Create bitfield message

		Args:
			bitfield (bytes): the bitfield that indicates whether you have each piece

		Returns:
			bytes: bitfield message
		"""
		return cls.create_message(MessageIdEnum.BITFIELD, bitfield)

	@classmethod
	def request(cls, index: int, begin: int, length: int) -> bytes:
		"""Create request message

		Args:
			index (int): piece index
			begin (int): byte offset within the piece
			length (int): requested length

		Returns:
			bytes: request message
		"""
		data = struct.pack(">3I", index, begin, length)
		return cls.create_message(MessageIdEnum.REQUEST, data)

	@classmethod
	def piece(cls, index: int, begin: int, block_data: bytes) -> bytes:
		"""Create piece message

		Args:
			index (int): piece index
			begin (int): byte offset within the piece
			block_data (bytes): subset of the piece

		Returns:
			bytes: piece message
		"""
		data = struct.pack(">2I", index, begin) + block_data
		return cls.create_message(MessageIdEnum.PIECE, data)
