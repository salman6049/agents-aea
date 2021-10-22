# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: oef_search.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="oef_search.proto",
    package="aea.fetchai.oef_search.v1_0_0",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=b'\n\x10oef_search.proto\x12\x1d\x61\x65\x61.fetchai.oef_search.v1_0_0"\xb8\r\n\x10OefSearchMessage\x12[\n\toef_error\x18\x05 \x01(\x0b\x32\x46.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Oef_Error_PerformativeH\x00\x12i\n\x10register_service\x18\x06 \x01(\x0b\x32M.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Register_Service_PerformativeH\x00\x12\x63\n\rsearch_result\x18\x07 \x01(\x0b\x32J.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Search_Result_PerformativeH\x00\x12g\n\x0fsearch_services\x18\x08 \x01(\x0b\x32L.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Search_Services_PerformativeH\x00\x12W\n\x07success\x18\t \x01(\x0b\x32\x44.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Success_PerformativeH\x00\x12m\n\x12unregister_service\x18\n \x01(\x0b\x32O.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Unregister_Service_PerformativeH\x00\x1a!\n\nAgentsInfo\x12\x13\n\x0b\x61gents_info\x18\x01 \x01(\x0c\x1a(\n\x0b\x44\x65scription\x12\x19\n\x11\x64\x65scription_bytes\x18\x01 \x01(\x0c\x1a\x8a\x02\n\x11OefErrorOperation\x12\x61\n\toef_error\x18\x01 \x01(\x0e\x32N.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.OefErrorOperation.OefErrorEnum"\x91\x01\n\x0cOefErrorEnum\x12\x14\n\x10REGISTER_SERVICE\x10\x00\x12\x16\n\x12UNREGISTER_SERVICE\x10\x01\x12\x13\n\x0fSEARCH_SERVICES\x10\x02\x12\x10\n\x0cSEND_MESSAGE\x10\x03\x12\x14\n\x10\x41LREADY_IN_LOBBY\x10\x04\x12\x16\n\x12\x41LREADY_REGISTERED\x10\x05\x1a\x1c\n\x05Query\x12\x13\n\x0bquery_bytes\x18\x01 \x01(\x0c\x1ay\n\x1dRegister_Service_Performative\x12X\n\x13service_description\x18\x01 \x01(\x0b\x32;.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Description\x1a{\n\x1fUnregister_Service_Performative\x12X\n\x13service_description\x18\x01 \x01(\x0b\x32;.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Description\x1a\x64\n\x1cSearch_Services_Performative\x12\x44\n\x05query\x18\x01 \x01(\x0b\x32\x35.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Query\x1a}\n\x1aSearch_Result_Performative\x12\x0e\n\x06\x61gents\x18\x01 \x03(\t\x12O\n\x0b\x61gents_info\x18\x02 \x01(\x0b\x32:.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.AgentsInfo\x1ag\n\x14Success_Performative\x12O\n\x0b\x61gents_info\x18\x01 \x01(\x0b\x32:.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.AgentsInfo\x1ax\n\x16Oef_Error_Performative\x12^\n\x13oef_error_operation\x18\x01 \x01(\x0b\x32\x41.aea.fetchai.oef_search.v1_0_0.OefSearchMessage.OefErrorOperationB\x0e\n\x0cperformativeb\x06proto3',
)


_OEFSEARCHMESSAGE_OEFERROROPERATION_OEFERRORENUM = _descriptor.EnumDescriptor(
    name="OefErrorEnum",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.OefErrorOperation.OefErrorEnum",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="REGISTER_SERVICE",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="UNREGISTER_SERVICE",
            index=1,
            number=1,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="SEARCH_SERVICES",
            index=2,
            number=2,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="SEND_MESSAGE", index=3, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ALREADY_IN_LOBBY",
            index=4,
            number=4,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="ALREADY_REGISTERED",
            index=5,
            number=5,
            serialized_options=None,
            type=None,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=877,
    serialized_end=1022,
)
_sym_db.RegisterEnumDescriptor(_OEFSEARCHMESSAGE_OEFERROROPERATION_OEFERRORENUM)


_OEFSEARCHMESSAGE_AGENTSINFO = _descriptor.Descriptor(
    name="AgentsInfo",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.AgentsInfo",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="agents_info",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.AgentsInfo.agents_info",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=678,
    serialized_end=711,
)

_OEFSEARCHMESSAGE_DESCRIPTION = _descriptor.Descriptor(
    name="Description",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Description",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="description_bytes",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Description.description_bytes",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=713,
    serialized_end=753,
)

_OEFSEARCHMESSAGE_OEFERROROPERATION = _descriptor.Descriptor(
    name="OefErrorOperation",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.OefErrorOperation",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="oef_error",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.OefErrorOperation.oef_error",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[_OEFSEARCHMESSAGE_OEFERROROPERATION_OEFERRORENUM,],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=756,
    serialized_end=1022,
)

_OEFSEARCHMESSAGE_QUERY = _descriptor.Descriptor(
    name="Query",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Query",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="query_bytes",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Query.query_bytes",
            index=0,
            number=1,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1024,
    serialized_end=1052,
)

_OEFSEARCHMESSAGE_REGISTER_SERVICE_PERFORMATIVE = _descriptor.Descriptor(
    name="Register_Service_Performative",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Register_Service_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="service_description",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Register_Service_Performative.service_description",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1054,
    serialized_end=1175,
)

_OEFSEARCHMESSAGE_UNREGISTER_SERVICE_PERFORMATIVE = _descriptor.Descriptor(
    name="Unregister_Service_Performative",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Unregister_Service_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="service_description",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Unregister_Service_Performative.service_description",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1177,
    serialized_end=1300,
)

_OEFSEARCHMESSAGE_SEARCH_SERVICES_PERFORMATIVE = _descriptor.Descriptor(
    name="Search_Services_Performative",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Search_Services_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="query",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Search_Services_Performative.query",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1302,
    serialized_end=1402,
)

_OEFSEARCHMESSAGE_SEARCH_RESULT_PERFORMATIVE = _descriptor.Descriptor(
    name="Search_Result_Performative",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Search_Result_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="agents",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Search_Result_Performative.agents",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="agents_info",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Search_Result_Performative.agents_info",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1404,
    serialized_end=1529,
)

_OEFSEARCHMESSAGE_SUCCESS_PERFORMATIVE = _descriptor.Descriptor(
    name="Success_Performative",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Success_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="agents_info",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Success_Performative.agents_info",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1531,
    serialized_end=1634,
)

_OEFSEARCHMESSAGE_OEF_ERROR_PERFORMATIVE = _descriptor.Descriptor(
    name="Oef_Error_Performative",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Oef_Error_Performative",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="oef_error_operation",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Oef_Error_Performative.oef_error_operation",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1636,
    serialized_end=1756,
)

_OEFSEARCHMESSAGE = _descriptor.Descriptor(
    name="OefSearchMessage",
    full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="oef_error",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.oef_error",
            index=0,
            number=5,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="register_service",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.register_service",
            index=1,
            number=6,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="search_result",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.search_result",
            index=2,
            number=7,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="search_services",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.search_services",
            index=3,
            number=8,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="success",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.success",
            index=4,
            number=9,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="unregister_service",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.unregister_service",
            index=5,
            number=10,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[
        _OEFSEARCHMESSAGE_AGENTSINFO,
        _OEFSEARCHMESSAGE_DESCRIPTION,
        _OEFSEARCHMESSAGE_OEFERROROPERATION,
        _OEFSEARCHMESSAGE_QUERY,
        _OEFSEARCHMESSAGE_REGISTER_SERVICE_PERFORMATIVE,
        _OEFSEARCHMESSAGE_UNREGISTER_SERVICE_PERFORMATIVE,
        _OEFSEARCHMESSAGE_SEARCH_SERVICES_PERFORMATIVE,
        _OEFSEARCHMESSAGE_SEARCH_RESULT_PERFORMATIVE,
        _OEFSEARCHMESSAGE_SUCCESS_PERFORMATIVE,
        _OEFSEARCHMESSAGE_OEF_ERROR_PERFORMATIVE,
    ],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="performative",
            full_name="aea.fetchai.oef_search.v1_0_0.OefSearchMessage.performative",
            index=0,
            containing_type=None,
            fields=[],
        ),
    ],
    serialized_start=52,
    serialized_end=1772,
)

_OEFSEARCHMESSAGE_AGENTSINFO.containing_type = _OEFSEARCHMESSAGE
_OEFSEARCHMESSAGE_DESCRIPTION.containing_type = _OEFSEARCHMESSAGE
_OEFSEARCHMESSAGE_OEFERROROPERATION.fields_by_name[
    "oef_error"
].enum_type = _OEFSEARCHMESSAGE_OEFERROROPERATION_OEFERRORENUM
_OEFSEARCHMESSAGE_OEFERROROPERATION.containing_type = _OEFSEARCHMESSAGE
_OEFSEARCHMESSAGE_OEFERROROPERATION_OEFERRORENUM.containing_type = (
    _OEFSEARCHMESSAGE_OEFERROROPERATION
)
_OEFSEARCHMESSAGE_QUERY.containing_type = _OEFSEARCHMESSAGE
_OEFSEARCHMESSAGE_REGISTER_SERVICE_PERFORMATIVE.fields_by_name[
    "service_description"
].message_type = _OEFSEARCHMESSAGE_DESCRIPTION
_OEFSEARCHMESSAGE_REGISTER_SERVICE_PERFORMATIVE.containing_type = _OEFSEARCHMESSAGE
_OEFSEARCHMESSAGE_UNREGISTER_SERVICE_PERFORMATIVE.fields_by_name[
    "service_description"
].message_type = _OEFSEARCHMESSAGE_DESCRIPTION
_OEFSEARCHMESSAGE_UNREGISTER_SERVICE_PERFORMATIVE.containing_type = _OEFSEARCHMESSAGE
_OEFSEARCHMESSAGE_SEARCH_SERVICES_PERFORMATIVE.fields_by_name[
    "query"
].message_type = _OEFSEARCHMESSAGE_QUERY
_OEFSEARCHMESSAGE_SEARCH_SERVICES_PERFORMATIVE.containing_type = _OEFSEARCHMESSAGE
_OEFSEARCHMESSAGE_SEARCH_RESULT_PERFORMATIVE.fields_by_name[
    "agents_info"
].message_type = _OEFSEARCHMESSAGE_AGENTSINFO
_OEFSEARCHMESSAGE_SEARCH_RESULT_PERFORMATIVE.containing_type = _OEFSEARCHMESSAGE
_OEFSEARCHMESSAGE_SUCCESS_PERFORMATIVE.fields_by_name[
    "agents_info"
].message_type = _OEFSEARCHMESSAGE_AGENTSINFO
_OEFSEARCHMESSAGE_SUCCESS_PERFORMATIVE.containing_type = _OEFSEARCHMESSAGE
_OEFSEARCHMESSAGE_OEF_ERROR_PERFORMATIVE.fields_by_name[
    "oef_error_operation"
].message_type = _OEFSEARCHMESSAGE_OEFERROROPERATION
_OEFSEARCHMESSAGE_OEF_ERROR_PERFORMATIVE.containing_type = _OEFSEARCHMESSAGE
_OEFSEARCHMESSAGE.fields_by_name[
    "oef_error"
].message_type = _OEFSEARCHMESSAGE_OEF_ERROR_PERFORMATIVE
_OEFSEARCHMESSAGE.fields_by_name[
    "register_service"
].message_type = _OEFSEARCHMESSAGE_REGISTER_SERVICE_PERFORMATIVE
_OEFSEARCHMESSAGE.fields_by_name[
    "search_result"
].message_type = _OEFSEARCHMESSAGE_SEARCH_RESULT_PERFORMATIVE
_OEFSEARCHMESSAGE.fields_by_name[
    "search_services"
].message_type = _OEFSEARCHMESSAGE_SEARCH_SERVICES_PERFORMATIVE
_OEFSEARCHMESSAGE.fields_by_name[
    "success"
].message_type = _OEFSEARCHMESSAGE_SUCCESS_PERFORMATIVE
_OEFSEARCHMESSAGE.fields_by_name[
    "unregister_service"
].message_type = _OEFSEARCHMESSAGE_UNREGISTER_SERVICE_PERFORMATIVE
_OEFSEARCHMESSAGE.oneofs_by_name["performative"].fields.append(
    _OEFSEARCHMESSAGE.fields_by_name["oef_error"]
)
_OEFSEARCHMESSAGE.fields_by_name[
    "oef_error"
].containing_oneof = _OEFSEARCHMESSAGE.oneofs_by_name["performative"]
_OEFSEARCHMESSAGE.oneofs_by_name["performative"].fields.append(
    _OEFSEARCHMESSAGE.fields_by_name["register_service"]
)
_OEFSEARCHMESSAGE.fields_by_name[
    "register_service"
].containing_oneof = _OEFSEARCHMESSAGE.oneofs_by_name["performative"]
_OEFSEARCHMESSAGE.oneofs_by_name["performative"].fields.append(
    _OEFSEARCHMESSAGE.fields_by_name["search_result"]
)
_OEFSEARCHMESSAGE.fields_by_name[
    "search_result"
].containing_oneof = _OEFSEARCHMESSAGE.oneofs_by_name["performative"]
_OEFSEARCHMESSAGE.oneofs_by_name["performative"].fields.append(
    _OEFSEARCHMESSAGE.fields_by_name["search_services"]
)
_OEFSEARCHMESSAGE.fields_by_name[
    "search_services"
].containing_oneof = _OEFSEARCHMESSAGE.oneofs_by_name["performative"]
_OEFSEARCHMESSAGE.oneofs_by_name["performative"].fields.append(
    _OEFSEARCHMESSAGE.fields_by_name["success"]
)
_OEFSEARCHMESSAGE.fields_by_name[
    "success"
].containing_oneof = _OEFSEARCHMESSAGE.oneofs_by_name["performative"]
_OEFSEARCHMESSAGE.oneofs_by_name["performative"].fields.append(
    _OEFSEARCHMESSAGE.fields_by_name["unregister_service"]
)
_OEFSEARCHMESSAGE.fields_by_name[
    "unregister_service"
].containing_oneof = _OEFSEARCHMESSAGE.oneofs_by_name["performative"]
DESCRIPTOR.message_types_by_name["OefSearchMessage"] = _OEFSEARCHMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OefSearchMessage = _reflection.GeneratedProtocolMessageType(
    "OefSearchMessage",
    (_message.Message,),
    {
        "AgentsInfo": _reflection.GeneratedProtocolMessageType(
            "AgentsInfo",
            (_message.Message,),
            {
                "DESCRIPTOR": _OEFSEARCHMESSAGE_AGENTSINFO,
                "__module__": "oef_search_pb2"
                # @@protoc_insertion_point(class_scope:aea.fetchai.oef_search.v1_0_0.OefSearchMessage.AgentsInfo)
            },
        ),
        "Description": _reflection.GeneratedProtocolMessageType(
            "Description",
            (_message.Message,),
            {
                "DESCRIPTOR": _OEFSEARCHMESSAGE_DESCRIPTION,
                "__module__": "oef_search_pb2"
                # @@protoc_insertion_point(class_scope:aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Description)
            },
        ),
        "OefErrorOperation": _reflection.GeneratedProtocolMessageType(
            "OefErrorOperation",
            (_message.Message,),
            {
                "DESCRIPTOR": _OEFSEARCHMESSAGE_OEFERROROPERATION,
                "__module__": "oef_search_pb2"
                # @@protoc_insertion_point(class_scope:aea.fetchai.oef_search.v1_0_0.OefSearchMessage.OefErrorOperation)
            },
        ),
        "Query": _reflection.GeneratedProtocolMessageType(
            "Query",
            (_message.Message,),
            {
                "DESCRIPTOR": _OEFSEARCHMESSAGE_QUERY,
                "__module__": "oef_search_pb2"
                # @@protoc_insertion_point(class_scope:aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Query)
            },
        ),
        "Register_Service_Performative": _reflection.GeneratedProtocolMessageType(
            "Register_Service_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _OEFSEARCHMESSAGE_REGISTER_SERVICE_PERFORMATIVE,
                "__module__": "oef_search_pb2"
                # @@protoc_insertion_point(class_scope:aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Register_Service_Performative)
            },
        ),
        "Unregister_Service_Performative": _reflection.GeneratedProtocolMessageType(
            "Unregister_Service_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _OEFSEARCHMESSAGE_UNREGISTER_SERVICE_PERFORMATIVE,
                "__module__": "oef_search_pb2"
                # @@protoc_insertion_point(class_scope:aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Unregister_Service_Performative)
            },
        ),
        "Search_Services_Performative": _reflection.GeneratedProtocolMessageType(
            "Search_Services_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _OEFSEARCHMESSAGE_SEARCH_SERVICES_PERFORMATIVE,
                "__module__": "oef_search_pb2"
                # @@protoc_insertion_point(class_scope:aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Search_Services_Performative)
            },
        ),
        "Search_Result_Performative": _reflection.GeneratedProtocolMessageType(
            "Search_Result_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _OEFSEARCHMESSAGE_SEARCH_RESULT_PERFORMATIVE,
                "__module__": "oef_search_pb2"
                # @@protoc_insertion_point(class_scope:aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Search_Result_Performative)
            },
        ),
        "Success_Performative": _reflection.GeneratedProtocolMessageType(
            "Success_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _OEFSEARCHMESSAGE_SUCCESS_PERFORMATIVE,
                "__module__": "oef_search_pb2"
                # @@protoc_insertion_point(class_scope:aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Success_Performative)
            },
        ),
        "Oef_Error_Performative": _reflection.GeneratedProtocolMessageType(
            "Oef_Error_Performative",
            (_message.Message,),
            {
                "DESCRIPTOR": _OEFSEARCHMESSAGE_OEF_ERROR_PERFORMATIVE,
                "__module__": "oef_search_pb2"
                # @@protoc_insertion_point(class_scope:aea.fetchai.oef_search.v1_0_0.OefSearchMessage.Oef_Error_Performative)
            },
        ),
        "DESCRIPTOR": _OEFSEARCHMESSAGE,
        "__module__": "oef_search_pb2"
        # @@protoc_insertion_point(class_scope:aea.fetchai.oef_search.v1_0_0.OefSearchMessage)
    },
)
_sym_db.RegisterMessage(OefSearchMessage)
_sym_db.RegisterMessage(OefSearchMessage.AgentsInfo)
_sym_db.RegisterMessage(OefSearchMessage.Description)
_sym_db.RegisterMessage(OefSearchMessage.OefErrorOperation)
_sym_db.RegisterMessage(OefSearchMessage.Query)
_sym_db.RegisterMessage(OefSearchMessage.Register_Service_Performative)
_sym_db.RegisterMessage(OefSearchMessage.Unregister_Service_Performative)
_sym_db.RegisterMessage(OefSearchMessage.Search_Services_Performative)
_sym_db.RegisterMessage(OefSearchMessage.Search_Result_Performative)
_sym_db.RegisterMessage(OefSearchMessage.Success_Performative)
_sym_db.RegisterMessage(OefSearchMessage.Oef_Error_Performative)


# @@protoc_insertion_point(module_scope)
