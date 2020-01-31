# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the tests of the messages module."""

from typing import cast

from aea.configurations.base import ProtocolConfig, PublicId
from aea.mail.base import Envelope
from aea.protocols.base import (
    JSONSerializer,
    Message,
    ProtobufSerializer,
    Protocol,
    Serializer,
)

from ..conftest import UNKNOWN_PROTOCOL_PUBLIC_ID


class TestBaseSerializations:
    """Test that the base serializations work."""

    @classmethod
    def setup_class(cls):
        """Set up the use case."""
        cls.message = Message(content="hello")
        cls.message2 = Message(body={"content": "hello"})

    def test_default_protobuf_serialization(self):
        """Test that the default Protobuf serialization works."""
        message_bytes = ProtobufSerializer().encode(self.message)
        envelope = Envelope(
            to="receiver",
            sender="sender",
            protocol_id=UNKNOWN_PROTOCOL_PUBLIC_ID,
            message=message_bytes,
        )
        envelope_bytes = envelope.encode()

        expected_envelope = Envelope.decode(envelope_bytes)
        actual_envelope = envelope
        assert expected_envelope == actual_envelope

        expected_msg = ProtobufSerializer().decode(expected_envelope.message)
        actual_msg = self.message
        assert expected_msg == actual_msg

    def test_default_json_serialization(self):
        """Test that the default JSON serialization works."""
        message_bytes = JSONSerializer().encode(self.message)
        envelope = Envelope(
            to="receiver",
            sender="sender",
            protocol_id=UNKNOWN_PROTOCOL_PUBLIC_ID,
            message=message_bytes,
        )
        envelope_bytes = envelope.encode()

        expected_envelope = Envelope.decode(envelope_bytes)
        actual_envelope = envelope
        assert expected_envelope == actual_envelope

        expected_msg = JSONSerializer().decode(expected_envelope.message)
        actual_msg = self.message
        assert expected_msg == actual_msg

    def test_str(self):
        """Test the __str__ of the message."""
        assert "hello" in str(self.message2)

    def test_set(self):
        """Test that the set method works."""
        key, value = "temporary_key", "temporary_value"
        assert self.message.get(key) is None
        self.message.set(key, value)
        assert self.message.get(key) == value

    def test_unset(self):
        """Test the unset function of the message."""
        self.message2.unset("content")
        assert "content" not in self.message2.body.keys()

    def test_body_setter(self):
        """Test the body setter."""
        m_dict = {"Hello": "World"}
        self.message2.body = m_dict
        assert "Hello" in self.message2.body.keys()

    def test_protocols_config(self):
        """Test the protocol config."""
        protocol = Protocol(
            protocol_id=PublicId.from_str("author/my_own_protocol:0.1.0"),
            serializer=cast(Serializer, ProtobufSerializer),
            config=ProtocolConfig(),
        )
        assert protocol.config is not None
