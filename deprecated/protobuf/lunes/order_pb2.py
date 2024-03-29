# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lunes/order.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import amount_pb2 as lunes_dot_amount__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='lunes/order.proto',
  package='lunes',
  syntax='proto3',
  serialized_pb=_b('\n\x11lunes/order.proto\x12\x05lunes\x1a\x12lunes/amount.proto\"<\n\tAssetPair\x12\x17\n\x0f\x61mount_asset_id\x18\x01 \x01(\x0c\x12\x16\n\x0eprice_asset_id\x18\x02 \x01(\x0c\"\xc3\x02\n\x05Order\x12\x10\n\x08\x63hain_id\x18\x01 \x01(\x05\x12\x19\n\x11sender_public_key\x18\x02 \x01(\x0c\x12\x1a\n\x12matcher_public_key\x18\x03 \x01(\x0c\x12$\n\nasset_pair\x18\x04 \x01(\x0b\x32\x10.lunes.AssetPair\x12%\n\norder_side\x18\x05 \x01(\x0e\x32\x11.lunes.Order.Side\x12\x0e\n\x06\x61mount\x18\x06 \x01(\x03\x12\r\n\x05price\x18\x07 \x01(\x03\x12\x11\n\ttimestamp\x18\x08 \x01(\x03\x12\x12\n\nexpiration\x18\t \x01(\x03\x12\"\n\x0bmatcher_fee\x18\n \x01(\x0b\x32\r.lunes.Amount\x12\x0f\n\x07version\x18\x0b \x01(\x05\x12\x0e\n\x06proofs\x18\x0c \x03(\x0c\"\x19\n\x04Side\x12\x07\n\x03\x42UY\x10\x00\x12\x08\n\x04SELL\x10\x01\x42*\n com.lunesplatform.protobuf.order\xaa\x02\x05Lunesb\x06proto3')
  ,
  dependencies=[lunes_dot_amount__pb2.DESCRIPTOR,])



_ORDER_SIDE = _descriptor.EnumDescriptor(
  name='Side',
  full_name='lunes.Order.Side',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BUY', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SELL', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=409,
  serialized_end=434,
)
_sym_db.RegisterEnumDescriptor(_ORDER_SIDE)


_ASSETPAIR = _descriptor.Descriptor(
  name='AssetPair',
  full_name='lunes.AssetPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='amount_asset_id', full_name='lunes.AssetPair.amount_asset_id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='price_asset_id', full_name='lunes.AssetPair.price_asset_id', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
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
  ],
  serialized_start=48,
  serialized_end=108,
)


_ORDER = _descriptor.Descriptor(
  name='Order',
  full_name='lunes.Order',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='chain_id', full_name='lunes.Order.chain_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sender_public_key', full_name='lunes.Order.sender_public_key', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='matcher_public_key', full_name='lunes.Order.matcher_public_key', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='asset_pair', full_name='lunes.Order.asset_pair', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='order_side', full_name='lunes.Order.order_side', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='lunes.Order.amount', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='price', full_name='lunes.Order.price', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='lunes.Order.timestamp', index=7,
      number=8, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='expiration', full_name='lunes.Order.expiration', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='matcher_fee', full_name='lunes.Order.matcher_fee', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='lunes.Order.version', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='proofs', full_name='lunes.Order.proofs', index=11,
      number=12, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ORDER_SIDE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=111,
  serialized_end=434,
)

_ORDER.fields_by_name['asset_pair'].message_type = _ASSETPAIR
_ORDER.fields_by_name['order_side'].enum_type = _ORDER_SIDE
_ORDER.fields_by_name['matcher_fee'].message_type = lunes_dot_amount__pb2._AMOUNT
_ORDER_SIDE.containing_type = _ORDER
DESCRIPTOR.message_types_by_name['AssetPair'] = _ASSETPAIR
DESCRIPTOR.message_types_by_name['Order'] = _ORDER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AssetPair = _reflection.GeneratedProtocolMessageType('AssetPair', (_message.Message,), dict(
  DESCRIPTOR = _ASSETPAIR,
  __module__ = 'lunes.order_pb2'
  # @@protoc_insertion_point(class_scope:lunes.AssetPair)
  ))
_sym_db.RegisterMessage(AssetPair)

Order = _reflection.GeneratedProtocolMessageType('Order', (_message.Message,), dict(
  DESCRIPTOR = _ORDER,
  __module__ = 'lunes.order_pb2'
  # @@protoc_insertion_point(class_scope:lunes.Order)
  ))
_sym_db.RegisterMessage(Order)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n com.lunesplatform.protobuf.order\252\002\005Lunes'))
# @@protoc_insertion_point(module_scope)
