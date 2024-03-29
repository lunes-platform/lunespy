# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lunes/recipient.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='lunes/recipient.proto',
  package='lunes',
  syntax='proto3',
  serialized_pb=_b('\n\x15lunes/recipient.proto\x12\x05lunes\"D\n\tRecipient\x12\x19\n\x0fpublic_key_hash\x18\x01 \x01(\x0cH\x00\x12\x0f\n\x05\x61lias\x18\x02 \x01(\tH\x00\x42\x0b\n\trecipientB0\n&com.lunesplatform.protobuf.transaction\xaa\x02\x05Lunesb\x06proto3')
)




_RECIPIENT = _descriptor.Descriptor(
  name='Recipient',
  full_name='lunes.Recipient',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='public_key_hash', full_name='lunes.Recipient.public_key_hash', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='alias', full_name='lunes.Recipient.alias', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='recipient', full_name='lunes.Recipient.recipient',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=32,
  serialized_end=100,
)

_RECIPIENT.oneofs_by_name['recipient'].fields.append(
  _RECIPIENT.fields_by_name['public_key_hash'])
_RECIPIENT.fields_by_name['public_key_hash'].containing_oneof = _RECIPIENT.oneofs_by_name['recipient']
_RECIPIENT.oneofs_by_name['recipient'].fields.append(
  _RECIPIENT.fields_by_name['alias'])
_RECIPIENT.fields_by_name['alias'].containing_oneof = _RECIPIENT.oneofs_by_name['recipient']
DESCRIPTOR.message_types_by_name['Recipient'] = _RECIPIENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Recipient = _reflection.GeneratedProtocolMessageType('Recipient', (_message.Message,), dict(
  DESCRIPTOR = _RECIPIENT,
  __module__ = 'lunes.recipient_pb2'
  # @@protoc_insertion_point(class_scope:lunes.Recipient)
  ))
_sym_db.RegisterMessage(Recipient)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n&com.lunesplatform.protobuf.transaction\252\002\005Lunes'))
# @@protoc_insertion_point(module_scope)
