# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: inner.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0binner.proto\x12\x0binnervoting\x1a\x1fgoogle/protobuf/timestamp.proto\"$\n\x05Voter\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\r\n\x05group\x18\x02 \x02(\t\"\x16\n\x06Status\x12\x0c\n\x04\x63ode\x18\x01 \x02(\x05\"g\n\x08\x45lection\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0e\n\x06groups\x18\x02 \x03(\t\x12\x0f\n\x07\x63hoices\x18\x03 \x03(\t\x12,\n\x08\x65nd_date\x18\x04 \x02(\x0b\x32\x1a.google.protobuf.Timestamp\"2\n\x04Vote\x12\x15\n\relection_name\x18\x01 \x02(\t\x12\x13\n\x0b\x63hoice_name\x18\x02 \x02(\t\"\x1c\n\x0c\x45lectionName\x12\x0c\n\x04name\x18\x01 \x02(\t\"/\n\tVoteCount\x12\x13\n\x0b\x63hoice_name\x18\x01 \x02(\t\x12\r\n\x05\x63ount\x18\x02 \x02(\x05\"G\n\x0e\x45lectionResult\x12\x0e\n\x06status\x18\x01 \x02(\x05\x12%\n\x05\x63ount\x18\x02 \x03(\x0b\x32\x16.innervoting.VoteCount\"\xa4\x01\n\x0e\x45lectionStatus\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0e\n\x06groups\x18\x02 \x03(\t\x12\x0f\n\x07\x63hoices\x18\x03 \x03(\t\x12%\n\x05\x63ount\x18\x04 \x03(\x0b\x32\x16.innervoting.VoteCount\x12\x0e\n\x06voters\x18\x05 \x03(\t\x12,\n\x08\x65nd_date\x18\x06 \x02(\x0b\x32\x1a.google.protobuf.Timestamp\";\n\tElections\x12.\n\telections\x18\x01 \x03(\x0b\x32\x1b.innervoting.ElectionStatus2\x97\x02\n\x0e\x65VotingReplica\x12=\n\x0f\x45lectionReplica\x12\x15.innervoting.Election\x1a\x13.innervoting.Status\x12\x39\n\x0f\x43\x61stVoteReplica\x12\x11.innervoting.Vote\x1a\x13.innervoting.Status\x12J\n\x10GetResultReplica\x12\x19.innervoting.ElectionName\x1a\x1b.innervoting.ElectionResult\x12?\n\x10\x45lectionRecovery\x12\x13.innervoting.Status\x1a\x16.innervoting.Elections')



_VOTER = DESCRIPTOR.message_types_by_name['Voter']
_STATUS = DESCRIPTOR.message_types_by_name['Status']
_ELECTION = DESCRIPTOR.message_types_by_name['Election']
_VOTE = DESCRIPTOR.message_types_by_name['Vote']
_ELECTIONNAME = DESCRIPTOR.message_types_by_name['ElectionName']
_VOTECOUNT = DESCRIPTOR.message_types_by_name['VoteCount']
_ELECTIONRESULT = DESCRIPTOR.message_types_by_name['ElectionResult']
_ELECTIONSTATUS = DESCRIPTOR.message_types_by_name['ElectionStatus']
_ELECTIONS = DESCRIPTOR.message_types_by_name['Elections']
Voter = _reflection.GeneratedProtocolMessageType('Voter', (_message.Message,), {
  'DESCRIPTOR' : _VOTER,
  '__module__' : 'inner_pb2'
  # @@protoc_insertion_point(class_scope:innervoting.Voter)
  })
_sym_db.RegisterMessage(Voter)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'inner_pb2'
  # @@protoc_insertion_point(class_scope:innervoting.Status)
  })
_sym_db.RegisterMessage(Status)

Election = _reflection.GeneratedProtocolMessageType('Election', (_message.Message,), {
  'DESCRIPTOR' : _ELECTION,
  '__module__' : 'inner_pb2'
  # @@protoc_insertion_point(class_scope:innervoting.Election)
  })
_sym_db.RegisterMessage(Election)

Vote = _reflection.GeneratedProtocolMessageType('Vote', (_message.Message,), {
  'DESCRIPTOR' : _VOTE,
  '__module__' : 'inner_pb2'
  # @@protoc_insertion_point(class_scope:innervoting.Vote)
  })
_sym_db.RegisterMessage(Vote)

ElectionName = _reflection.GeneratedProtocolMessageType('ElectionName', (_message.Message,), {
  'DESCRIPTOR' : _ELECTIONNAME,
  '__module__' : 'inner_pb2'
  # @@protoc_insertion_point(class_scope:innervoting.ElectionName)
  })
_sym_db.RegisterMessage(ElectionName)

VoteCount = _reflection.GeneratedProtocolMessageType('VoteCount', (_message.Message,), {
  'DESCRIPTOR' : _VOTECOUNT,
  '__module__' : 'inner_pb2'
  # @@protoc_insertion_point(class_scope:innervoting.VoteCount)
  })
_sym_db.RegisterMessage(VoteCount)

ElectionResult = _reflection.GeneratedProtocolMessageType('ElectionResult', (_message.Message,), {
  'DESCRIPTOR' : _ELECTIONRESULT,
  '__module__' : 'inner_pb2'
  # @@protoc_insertion_point(class_scope:innervoting.ElectionResult)
  })
_sym_db.RegisterMessage(ElectionResult)

ElectionStatus = _reflection.GeneratedProtocolMessageType('ElectionStatus', (_message.Message,), {
  'DESCRIPTOR' : _ELECTIONSTATUS,
  '__module__' : 'inner_pb2'
  # @@protoc_insertion_point(class_scope:innervoting.ElectionStatus)
  })
_sym_db.RegisterMessage(ElectionStatus)

Elections = _reflection.GeneratedProtocolMessageType('Elections', (_message.Message,), {
  'DESCRIPTOR' : _ELECTIONS,
  '__module__' : 'inner_pb2'
  # @@protoc_insertion_point(class_scope:innervoting.Elections)
  })
_sym_db.RegisterMessage(Elections)

_EVOTINGREPLICA = DESCRIPTOR.services_by_name['eVotingReplica']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _VOTER._serialized_start=61
  _VOTER._serialized_end=97
  _STATUS._serialized_start=99
  _STATUS._serialized_end=121
  _ELECTION._serialized_start=123
  _ELECTION._serialized_end=226
  _VOTE._serialized_start=228
  _VOTE._serialized_end=278
  _ELECTIONNAME._serialized_start=280
  _ELECTIONNAME._serialized_end=308
  _VOTECOUNT._serialized_start=310
  _VOTECOUNT._serialized_end=357
  _ELECTIONRESULT._serialized_start=359
  _ELECTIONRESULT._serialized_end=430
  _ELECTIONSTATUS._serialized_start=433
  _ELECTIONSTATUS._serialized_end=597
  _ELECTIONS._serialized_start=599
  _ELECTIONS._serialized_end=658
  _EVOTINGREPLICA._serialized_start=661
  _EVOTINGREPLICA._serialized_end=940
# @@protoc_insertion_point(module_scope)
