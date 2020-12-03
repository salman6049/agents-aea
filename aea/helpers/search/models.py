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

"""Useful classes for the OEF search."""

import logging
from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from math import asin, cos, radians, sin, sqrt
from typing import Any, Dict, List, Mapping, Optional, Tuple, Type, Union, cast

from aea.exceptions import enforce
import aea.helpers.search.models_pb2 as models_pb2


_default_logger = logging.getLogger(__name__)


class Location:
    """Data structure to represent locations (i.e. a pair of latitude and longitude)."""

    def __init__(self, latitude: float, longitude: float):
        """
        Initialize a location.

        :param latitude: the latitude of the location.
        :param longitude: the longitude of the location.
        """
        self.latitude = latitude
        self.longitude = longitude

    @property
    def tuple(self) -> Tuple[float, float]:
        """Get the tuple representation of a location."""
        return self.latitude, self.longitude

    def distance(self, other: "Location") -> float:
        """
        Get the distance to another location.

        :param other: the other location
        :retun: the distance
        """
        return haversine(self.latitude, self.longitude, other.latitude, other.longitude)

    def __eq__(self, other):
        """Compare equality of two locations."""
        if not isinstance(other, Location):
            return False  # pragma: nocover
        return self.latitude == other.latitude and self.longitude == other.longitude

    def __str__(self):
        """Get the string representation of the data model."""
        return "Location(latitude={},longitude={})".format(
            self.latitude, self.longitude
        )

    def encode(self) -> models_pb2.Query.Location():
        """
        Encode an instance of this class into a protocol buffer object.

        :return: the matching protocol buffer object
        """
        location_pb = models_pb2.Query.Location()
        location_pb.lat = self.latitude
        location_pb.lon = self.longitude
        return location_pb

    @classmethod
    def decode(cls, location_protobuf_object) -> "Location":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        :param location_protobuf_object: the protocol buffer object corresponding with this class.
        :return: A new instance of this class matching the protocol buffer object
        """
        latitude = location_protobuf_object.lat
        longitude = location_protobuf_object.lon
        return cls(latitude, longitude)


"""
The allowable types that an Attribute can have
"""
ATTRIBUTE_TYPES = Union[float, str, bool, int, Location]
ALLOWED_ATTRIBUTE_TYPES = [float, str, bool, int, Location]


class AttributeInconsistencyException(Exception):
    """
    Raised when the attributes in a Description are inconsistent.

    Inconsistency is defined when values do not meet their respective schema, or if the values
    are not of an allowed type.
    """

    pass


class Attribute:
    """Implements an attribute for an OEF data model."""

    _attribute_type_to_pb = {
        bool: models_pb2.Query.Attribute.BOOL,
        int: models_pb2.Query.Attribute.INT,
        float: models_pb2.Query.Attribute.DOUBLE,
        str: models_pb2.Query.Attribute.STRING,
        Location: models_pb2.Query.Attribute.LOCATION
    }

    def __init__(
        self,
        name: str,
        type_: Type[ATTRIBUTE_TYPES],
        is_required: bool,
        description: str = "",
    ):
        """
        Initialize an attribute.

        :param name: the name of the attribute.
        :param type_: the type of the attribute.
        :param is_required: whether the attribute is required by the data model.
        :param description: an (optional) human-readable description for the attribute.
        """
        self.name = name
        self.type = type_
        self.is_required = is_required
        self.description = description

    def __eq__(self, other):
        """Compare with another object."""
        return (
            isinstance(other, Attribute)
            and self.name == other.name
            and self.type == other.type
            and self.is_required == other.is_required
        )

    def __str__(self):
        """Get the string representation of the data model."""
        return "Attribute(name={},type={},is_required={})".format(
            self.name, self.type, self.is_required
        )

    def encode(self) -> models_pb2.Query.Attribute():
        """
        Encode an instance of this class into a protocol buffer object.

        :return: the matching protocol buffer object
        """
        attribute = models_pb2.Query.Attribute()
        attribute.name = self.name
        attribute.type = self._attribute_type_to_pb[self.type]
        attribute.required = self.is_required
        if self.description is not None:
            attribute.description = self.description
        return attribute

    @classmethod
    def decode(cls, attribute_protobuf_object) -> "Attribute":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        :param attribute_protobuf_object: the protocol buffer object corresponding with this class.
        :return: A new instance of this class matching the protocol buffer object
        """
        return cls(attribute_protobuf_object.name,
                   dict(map(reversed, cls._attribute_type_to_pb.items()))[attribute_protobuf_object.type],
                   attribute_protobuf_object.required,
                   attribute_protobuf_object.description if attribute_protobuf_object.description else None)


class DataModel:
    """Implements an OEF data model."""

    def __init__(self, name: str, attributes: List[Attribute], description: str = ""):
        """
        Initialize a data model.

        :param name: the name of the data model.
        :param attributes: the attributes of the data model.
        """
        self.name: str = name
        self.attributes = sorted(
            attributes, key=lambda x: x.name
        )  # type: List[Attribute]
        self._check_validity()
        self.attributes_by_name = {a.name: a for a in self.attributes}
        self.description = description

    def _check_validity(self):
        # check if there are duplicated attribute names
        attribute_names = [attribute.name for attribute in self.attributes]
        if len(attribute_names) != len(set(attribute_names)):
            raise ValueError(
                "Invalid input value for type '{}': duplicated attribute name.".format(
                    type(self).__name__
                )
            )

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return (
            isinstance(other, DataModel)
            and self.name == other.name
            and self.attributes == other.attributes
        )

    def __str__(self):
        """Get the string representation of the data model."""
        return "DataModel(name={},attributes={},description={})".format(
            self.name, {a.name: str(a) for a in self.attributes}, self.description
        )

    def encode(self) -> models_pb2.Query.DataModel():
        """
        Encode an instance of this class into a protocol buffer object.

        :return: the matching protocol buffer object
        """
        model = models_pb2.Query.DataModel()
        model.name = self.name
        model.attributes.extend([attr.encode() for attr in self.attributes])
        if self.description is not None:
            model.description = self.description
        return model

    @classmethod
    def decode(cls, data_model_protobuf_object) -> "DataModel":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        :param data_model_protobuf_object: the protocol buffer object corresponding with this class.
        :return: A new instance of this class matching the protocol buffer object
        """
        name = data_model_protobuf_object.name
        attributes = [Attribute.decode(attr_pb) for attr_pb in data_model_protobuf_object.attributes]
        description = data_model_protobuf_object.description
        return cls(name, attributes, description)


def generate_data_model(
    model_name: str, attribute_values: Mapping[str, ATTRIBUTE_TYPES]
) -> DataModel:
    """
    Generate a data model that matches the values stored in this description.

    That is, for each attribute (name, value), generate an Attribute.
    It is assumed that each attribute is required.

    :param model_name: the name of the model.
    :param attribute_values: the values of each attribute
    :return: the schema compliant with the values specified.
    """
    return DataModel(
        model_name,
        [Attribute(key, type(value), True) for key, value in attribute_values.items()],
    )


class Description:
    """Implements an OEF description."""

    def __init__(
        self,
        values: Mapping[str, ATTRIBUTE_TYPES],
        data_model: Optional[DataModel] = None,
        data_model_name: str = "",
    ):
        """
        Initialize the description object.

        :param values: the values in the description.
        :param data_model: the data model (optional)
        :pram data_model_name: the data model name if a datamodel is created on the fly.
        """
        _values = deepcopy(values)
        self._values = _values
        if data_model is not None:
            self.data_model = data_model
        else:
            self.data_model = generate_data_model(data_model_name, values)
        self._check_consistency()

    @property
    def values(self) -> Dict:
        """Get the values."""
        return cast(Dict, self._values)

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return (
            isinstance(other, Description)
            and self.values == other.values
            and self.data_model == other.data_model
        )

    def __iter__(self):
        """Create an iterator."""
        return iter(self.values)

    def _check_consistency(self):
        """
        Check the consistency of the values of this description.

        If an attribute has been provided, values are checked against that. If no attribute
        schema has been provided then minimal checking is performed based on the values in the
        provided attribute_value dictionary.
        :raises AttributeInconsistencyException: if values do not meet the schema, or if no schema is present
                                               | if they have disallowed types.
        """
        # check that all required attributes in the schema are contained in the description
        required_attributes = [
            attribute.name
            for attribute in self.data_model.attributes
            if attribute.is_required
        ]
        if not all(
            attribute_name in self.values for attribute_name in required_attributes
        ):
            raise AttributeInconsistencyException("Missing required attribute.")

        # check that all values are defined in the data model
        all_attributes = [attribute.name for attribute in self.data_model.attributes]
        if not all(key in all_attributes for key in self.values.keys()):
            raise AttributeInconsistencyException(
                "Have extra attribute not in data model."
            )

        # check that each of the provided values are consistent with that specified in the data model
        for key, value in self.values.items():
            attribute = next(
                (
                    attribute
                    for attribute in self.data_model.attributes
                    if attribute.name == key
                ),
                None,
            )
            if not isinstance(value, attribute.type):
                # values does not match type in data model
                raise AttributeInconsistencyException(
                    "Attribute {} has incorrect type: {}".format(
                        attribute.name, attribute.type
                    )
                )
            if not type(value) in ALLOWED_ATTRIBUTE_TYPES:
                # value type matches data model, but it is not an allowed type
                raise AttributeInconsistencyException(
                    "Attribute {} has unallowed type: {}. Allowed types: {}".format(
                        attribute.name, type(value), ALLOWED_ATTRIBUTE_TYPES,
                    )
                )

    def __str__(self):
        """Get the string representation of the description."""
        return "Description(values={},data_model={})".format(
            self._values, self.data_model
        )

    @staticmethod
    def _to_key_value_pb(key: str, value: ATTRIBUTE_TYPES) -> models_pb2.Query.KeyValue:
        """
        From a (key, attribute value) pair to the associated Protobuf object.

        :param key: the key of the attribute.
        :param value: the value of the attribute.

        :return: the associated Protobuf object.
        """

        kv = models_pb2.Query.KeyValue()
        kv.key = key
        if type(value) == bool:
            kv.value.b = value
        elif type(value) == int:
            kv.value.i = value
        elif type(value) == float:
            kv.value.d = value
        elif type(value) == str:
            kv.value.s = value
        elif type(value) == Location:
            kv.value.l.CopyFrom(value.encode())

        return kv

    def encode(self) -> models_pb2.Query.Instance():
        """
        Encode an instance of this class into a protocol buffer object.

        :return: the matching protocol buffer object
        """
        instance = models_pb2.Query.Instance()
        instance.model.CopyFrom(self.data_model.encode())
        instance.values.extend([self._to_key_value_pb(key, value) for key, value in self.values.items()])
        return instance

    @staticmethod
    def _extract_value(value: models_pb2.Query.Value) -> ATTRIBUTE_TYPES:
        """
        From a Protobuf query value object to attribute type.
        :param value: an instance of models_pb2.Query.Value.
        :return: the associated attribute type.
        """
        value_case = value.WhichOneof("value")
        if value_case == "s":
            return value.s
        elif value_case == "b":
            return bool(value.b)
        elif value_case == "i":
            return value.i
        elif value_case == "d":
            return value.d
        elif value_case == "l":
            return Location.decode(value.l)

    @classmethod
    def decode(cls, description_protobuf_object) -> "Description":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        :param description_protobuf_object: the protocol buffer object corresponding with this class.
        :return: A new instance of this class matching the protocol buffer object
        """
        model = DataModel.decode(description_protobuf_object.model)
        values = dict([(attr.key, cls._extract_value(attr.value)) for attr in description_protobuf_object.values])
        return cls(values, model)


class ConstraintTypes(Enum):
    """Types of constraint."""

    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_THAN_EQ = "<="
    GREATER_THAN = ">"
    GREATER_THAN_EQ = ">="
    WITHIN = "within"
    IN = "in"
    NOT_IN = "not_in"
    DISTANCE = "distance"

    def __str__(self):  # pragma: nocover
        """Get the string representation."""
        return str(self.value)


class ConstraintType:
    """
    Type of constraint.

    Used with the Constraint class, this class allows to specify constraint over attributes.

    Examples:
        Equal to three
        >>> equal_3 = ConstraintType(ConstraintTypes.EQUAL, 3)

    You can also specify a type of constraint by using its string representation, e.g.:
        >>> equal_3 = ConstraintType("==", 3)
        >>> not_equal_london = ConstraintType("!=", "London")
        >>> less_than_pi = ConstraintType("<", 3.14)
        >>> within_range = ConstraintType("within", (-10.0, 10.0))
        >>> in_a_set = ConstraintType("in", [1, 2, 3])
        >>> not_in_a_set = ConstraintType("not_in", {"C", "Java", "Python"})

    """

    def __init__(self, type_: Union[ConstraintTypes, str], value: Any):
        """
        Initialize a constraint type.

        :param type_: the type of the constraint.
                   | Either an instance of the ConstraintTypes enum,
                   | or a string representation associated with the type.
        :param value: the value that defines the constraint.
        :raises ValueError: if the type of the constraint is not
        """
        self.type = ConstraintTypes(type_)
        self.value = value
        enforce(self.check_validity(), "ConstraintType initialization inconsistent.")

    def check_validity(self):
        """
        Check the validity of the input provided.

        :return: None
        :raises ValueError: if the value is not valid wrt the constraint type.
        """
        try:
            if self.type == ConstraintTypes.EQUAL:
                enforce(
                    isinstance(self.value, (int, float, str, bool)),
                    f"Expected one of type in (int, float, str, bool), got {self.value}",
                )
            elif self.type == ConstraintTypes.NOT_EQUAL:
                enforce(
                    isinstance(self.value, (int, float, str, bool)),
                    f"Expected one of type in (int, float, str, bool), got {self.value}",
                )
            elif self.type == ConstraintTypes.LESS_THAN:
                enforce(
                    isinstance(self.value, (int, float, str)),
                    f"Expected one of type in (int, float, str), got {self.value}",
                )
            elif self.type == ConstraintTypes.LESS_THAN_EQ:
                enforce(
                    isinstance(self.value, (int, float, str)),
                    f"Expected one of type in (int, float, str), got {self.value}",
                )
            elif self.type == ConstraintTypes.GREATER_THAN:
                enforce(
                    isinstance(self.value, (int, float, str)),
                    f"Expected one of type in (int, float, str), got {self.value}",
                )
            elif self.type == ConstraintTypes.GREATER_THAN_EQ:
                enforce(
                    isinstance(self.value, (int, float, str)),
                    f"Expected one of type in (int, float, str), got {self.value}",
                )
            elif self.type == ConstraintTypes.WITHIN:
                enforce(
                    isinstance(self.value, (list, tuple)),
                    f"Expected one of type in (list, tuple), got {self.value}",
                )
                enforce(
                    len(self.value) == 2, f"Expected length=2, got {len(self.value)}"
                )
                enforce(
                    isinstance(self.value[0], type(self.value[1])), "Invalid types."
                )
                enforce(
                    isinstance(self.value[1], type(self.value[0])), "Invalid types."
                )
            elif self.type == ConstraintTypes.IN:
                enforce(
                    isinstance(self.value, (list, tuple, set)),
                    f"Expected one of type in (list, tuple, set), got {self.value}",
                )
                if len(self.value) > 0:
                    _type = type(next(iter(self.value)))
                    enforce(
                        all(isinstance(obj, _type) for obj in self.value),
                        "Invalid types.",
                    )
            elif self.type == ConstraintTypes.NOT_IN:
                enforce(
                    isinstance(self.value, (list, tuple, set)),
                    f"Expected one of type in (list, tuple, set), got {self.value}",
                )
                if len(self.value) > 0:
                    _type = type(next(iter(self.value)))
                    enforce(
                        all(isinstance(obj, _type) for obj in self.value),
                        "Invalid types.",
                    )
            elif self.type == ConstraintTypes.DISTANCE:
                enforce(
                    isinstance(self.value, (list, tuple)),
                    f"Expected one of type in (list, tuple), got {self.value}",
                )
                enforce(
                    len(self.value) == 2, f"Expected length=2, got {len(self.value)}"
                )
                enforce(
                    isinstance(self.value[0], Location),
                    "Invalid type, expected Location.",
                )
                enforce(
                    isinstance(self.value[1], float), "Invalid type, expected Location."
                )
            else:  # pragma: nocover
                raise ValueError("Type not recognized.")
        except ValueError:
            return False  # pragma: nocover

        return True

    def is_valid(self, attribute: Attribute) -> bool:
        """
        Check if the constraint type is valid wrt a given attribute.

        A constraint type is valid wrt an attribute if the
        type of its operand(s) is the same of the attribute type.

        >>> attribute = Attribute("year", int, True)
        >>> valid_constraint_type = ConstraintType(ConstraintTypes.GREATER_THAN, 2000)
        >>> valid_constraint_type.is_valid(attribute)
        True

        >>> valid_constraint_type = ConstraintType(ConstraintTypes.WITHIN, (2000, 2001))
        >>> valid_constraint_type.is_valid(attribute)
        True

        The following constraint is invalid: the year is in a string variable,
        whereas the attribute is defined over integers.

        >>> invalid_constraint_type = ConstraintType(ConstraintTypes.GREATER_THAN, "2000")
        >>> invalid_constraint_type.is_valid(attribute)
        False

        :param attribute: the data model used to check the validity of the constraint type.
        :return: ``True`` if the constraint type is valid wrt the attribute, ``False`` otherwise.
        """
        return self.get_data_type() == attribute.type

    def get_data_type(self) -> Type[ATTRIBUTE_TYPES]:
        """
        Get the type of the data used to define the constraint type.

        For instance:
        >>> c = ConstraintType(ConstraintTypes.EQUAL, 1)
        >>> c.get_data_type()
        <class 'int'>

        """
        if isinstance(self.value, (list, tuple, set)):
            value = next(iter(self.value))
        else:
            value = self.value
        value = cast(ATTRIBUTE_TYPES, value)
        return type(value)

    def check(self, value: ATTRIBUTE_TYPES) -> bool:
        """
        Check if an attribute value satisfies the constraint.

        The implementation depends on the constraint type.

        :param value: the value to check.
        :return: True if the value satisfy the constraint, False otherwise.
        :raises ValueError: if the constraint type is not recognized.
        """
        if self.type == ConstraintTypes.EQUAL:
            return self.value == value
        if self.type == ConstraintTypes.NOT_EQUAL:
            return self.value != value
        if self.type == ConstraintTypes.LESS_THAN:
            return self.value < value
        if self.type == ConstraintTypes.LESS_THAN_EQ:
            return self.value <= value
        if self.type == ConstraintTypes.GREATER_THAN:
            return self.value > value
        if self.type == ConstraintTypes.GREATER_THAN_EQ:
            return self.value >= value
        if self.type == ConstraintTypes.WITHIN:
            low = self.value[0]
            high = self.value[1]
            return low <= value <= high
        if self.type == ConstraintTypes.IN:
            return value in self.value
        if self.type == ConstraintTypes.NOT_IN:
            return value not in self.value
        if self.type == ConstraintTypes.DISTANCE:
            if not isinstance(value, Location):  # pragma: nocover
                raise ValueError("Value must be of type Location.")
            location = cast(Location, self.value[0])
            distance = self.value[1]
            return location.distance(value) <= distance
        raise ValueError("Constraint type not recognized.")  # pragma: nocover

    def __eq__(self, other):
        """Check equality with another object."""
        return (
            isinstance(other, ConstraintType)
            and self.value == other.value
            and self.type == other.type
        )

    def __str__(self):
        """Get the string representation of the constraint type."""
        return "ConstraintType(value={},type={})".format(self.value, self.type)

    def encode(self):
        """
        Encode an instance of this class into a protocol buffer object.

        :return: the matching protocol buffer object
        """
        encoding = None

        if (
            self.type == ConstraintTypes.EQUAL
            or self.type == ConstraintTypes.NOT_EQUAL
            or self.type == ConstraintTypes.LESS_THAN
            or self.type == ConstraintTypes.LESS_THAN_EQ
            or self.type == ConstraintTypes.GREATER_THAN
            or self.type == ConstraintTypes.GREATER_THAN_EQ
        ):
            relation = models_pb2.Query.Relation()

            if self.type == ConstraintTypes.EQUAL:
                relation.op = models_pb2.Query.Relation.EQ
            elif self.type == ConstraintTypes.NOT_EQUAL:
                relation.op = models_pb2.Query.Relation.NOTEQ
            elif self.type == ConstraintTypes.LESS_THAN:
                relation.op = models_pb2.Query.Relation.LT
            elif self.type == ConstraintTypes.LESS_THAN_EQ:
                relation.op = models_pb2.Query.Relation.LTEQ
            elif self.type == ConstraintTypes.GREATER_THAN:
                relation.op = models_pb2.Query.Relation.GT
            elif self.type == ConstraintTypes.GREATER_THAN_EQ:
                relation.op = models_pb2.Query.Relation.GTEQ

            query_value = models_pb2.Query.Value()

            if isinstance(self.value, bool):
                query_value.b = self.value
            elif isinstance(self.value, int):
                query_value.i = self.value
            elif isinstance(self.value, float):
                query_value.d = self.value
            elif isinstance(self.value, str):
                query_value.s = self.value
            elif isinstance(self.value, Location):
                query_value.l.CopyFrom(self.value.encode())
            relation.val.CopyFrom(query_value)

            encoding = relation

        elif self.type == ConstraintTypes.WITHIN:
            range_ = models_pb2.Query.Range()

            if type(self.value[0]) == str:
                values = models_pb2.Query.StringPair()
                values.first = self.value[0]
                values.second = self.value[1]
                range_.s.CopyFrom(values)
            elif type(self.value[0]) == int:
                values = models_pb2.Query.IntPair()
                values.first = self.value[0]
                values.second = self.value[1]
                range_.i.CopyFrom(values)
            elif type(self.value[0]) == float:
                values = models_pb2.Query.DoublePair()
                values.first = self.value[0]
                values.second = self.value[1]
                range_.d.CopyFrom(values)
            elif type(self.value[0]) == Location:
                values = models_pb2.Query.LocationPair()
                values.first.CopyFrom(self.value[0].encode())
                values.second.CopyFrom(self.value[1].encode())
                range_.l.CopyFrom(values)
            encoding = range_

        elif self.type == ConstraintTypes.IN or self.type == ConstraintTypes.NOT_IN:
            set_ = models_pb2.Query.Set()

            if self.type == ConstraintTypes.IN:
                set_.op = models_pb2.Query.Set.IN
            elif self.type == ConstraintTypes.NOT_IN:
                set_.op = models_pb2.Query.Set.NOTIN

            value_type = type(self.value[0]) if len(self.value) > 0 else str

            if value_type == str:
                values = models_pb2.Query.Set.Values.Strings()
                values.vals.extend(self.value)
                set_.vals.s.CopyFrom(values)
            elif value_type == bool:
                values = models_pb2.Query.Set.Values.Bools()
                values.vals.extend(self.value)
                set_.vals.b.CopyFrom(values)
            elif value_type == int:
                values = models_pb2.Query.Set.Values.Ints()
                values.vals.extend(self.value)
                set_.vals.i.CopyFrom(values)
            elif value_type == float:
                values = models_pb2.Query.Set.Values.Doubles()
                values.vals.extend(self.value)
                set_.vals.d.CopyFrom(values)
            elif value_type == Location:
                values = models_pb2.Query.Set.Values.Locations()
                values.vals.extend([value.encode() for value in self.value])
                set_.vals.l.CopyFrom(values)

            encoding = set_

        elif self.type == ConstraintTypes.DISTANCE:
            distance_pb = models_pb2.Query.Distance()
            distance_pb.distance = self.value[1]
            distance_pb.center.CopyFrom(self.value[0].encode())

            encoding = distance_pb

        return encoding

    @classmethod
    def decode(cls, constraint_type_protobuf_object, category: str) -> Optional["ConstraintType"]:
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        :param constraint_type_protobuf_object: the protocol buffer object corresponding with this class.
        :param category: the category of the constraint ('relation', 'set', 'range', 'distance).

        :return: A new instance of this class matching the protocol buffer object
        """
        decoding = None

        type_from_pb = {
            models_pb2.Query.Relation.GTEQ: ConstraintTypes.GREATER_THAN_EQ,
            models_pb2.Query.Relation.GT: ConstraintTypes.GREATER_THAN,
            models_pb2.Query.Relation.LTEQ: ConstraintTypes.LESS_THAN_EQ,
            models_pb2.Query.Relation.LT: ConstraintTypes.LESS_THAN,
            models_pb2.Query.Relation.NOTEQ: ConstraintTypes.NOT_EQUAL,
            models_pb2.Query.Relation.EQ: ConstraintTypes.EQUAL,
            models_pb2.Query.Set.IN: ConstraintTypes.IN,
            models_pb2.Query.Set.NOTIN: ConstraintTypes.NOT_IN
        }

        if category == "relation":
            relation_enum = type_from_pb[constraint_type_protobuf_object.op]
            value_case = constraint_type_protobuf_object.val.WhichOneof("value")
            if value_case == "s":
                decoding = ConstraintType(relation_enum, constraint_type_protobuf_object.val.s)
            elif value_case == "b":
                decoding = ConstraintType(relation_enum, constraint_type_protobuf_object.val.b)
            elif value_case == "i":
                decoding = ConstraintType(relation_enum, constraint_type_protobuf_object.val.i)
            elif value_case == "d":
                decoding = ConstraintType(relation_enum, constraint_type_protobuf_object.val.d)
            elif value_case == "l":
                decoding = ConstraintType(relation_enum, Location.decode(constraint_type_protobuf_object.val.l))
        elif category == "range":
            range_enum = ConstraintTypes.WITHIN
            range_case = constraint_type_protobuf_object.WhichOneof("pair")
            if range_case == "s":
                decoding = ConstraintType(range_enum, (constraint_type_protobuf_object.s.first, constraint_type_protobuf_object.s.second))
            elif range_case == "i":
                decoding = ConstraintType(range_enum, (constraint_type_protobuf_object.i.first, constraint_type_protobuf_object.i.second))
            elif range_case == "d":
                decoding = ConstraintType(range_enum, (constraint_type_protobuf_object.d.first, constraint_type_protobuf_object.d.second))
            elif range_case == "l":
                decoding = ConstraintType(range_enum, (Location.decode(constraint_type_protobuf_object.l.first), Location.decode(constraint_type_protobuf_object.l.second)))
        elif category == "set":
            set_enum = type_from_pb[constraint_type_protobuf_object.op]
            value_case = constraint_type_protobuf_object.vals.WhichOneof("values")
            if value_case == "s":
                decoding = ConstraintType(set_enum, constraint_type_protobuf_object.vals.s.vals)
            elif value_case == "b":
                decoding = ConstraintType(set_enum, constraint_type_protobuf_object.vals.b.vals)
            elif value_case == "i":
                decoding = ConstraintType(set_enum, constraint_type_protobuf_object.vals.i.vals)
            elif value_case == "d":
                decoding = ConstraintType(set_enum, constraint_type_protobuf_object.vals.d.vals)
            elif value_case == "l":
                locations = [Location.decode(loc) for loc in constraint_type_protobuf_object.vals.l.vals]
                decoding = ConstraintType(set_enum, locations)
        elif category == "distance":
            distance_enum = ConstraintTypes.DISTANCE
            center = Location.decode(constraint_type_protobuf_object.center)
            distance = constraint_type_protobuf_object.distance
            decoding = ConstraintType(distance_enum, (center, distance))
        else:
            raise ValueError(f"Incorrect category. Expected either 'relation', 'range', 'set', or 'distance'. Found {category}.")
        return decoding


class ConstraintExpr(ABC):
    """Implementation of the constraint language to query the OEF node."""

    @abstractmethod
    def check(self, description: Description) -> bool:
        """
        Check if a description satisfies the constraint expression.

        :param description: the description to check.
        :return: True if the description satisfy the constraint expression, False otherwise.
        """

    @abstractmethod
    def is_valid(self, data_model: DataModel) -> bool:
        """
        Check whether a constraint expression is valid wrt a data model.

         Specifically, check the following conditions:
        - If all the attributes referenced by the constraints are correctly associated with the Data Model attributes.

        :param data_model: the data model used to check the validity of the constraint expression.
        :return: ``True`` if the constraint expression is valid wrt the data model, ``False`` otherwise.
        """

    def check_validity(self) -> None:  # pylint: disable=no-self-use  # pragma: nocover
        """
        Check whether a Constraint Expression satisfies some basic requirements.

        :return ``None``
        :raises ValueError: if the object does not satisfy some requirements.
        """
        return None

    @staticmethod
    def _encode(expression) -> models_pb2.Query.ConstraintExpr():
        """
        Encode an instance of this class into a protocol buffer object.

        :return: the matching protocol buffer object
        """
        constraint_expr_pb = models_pb2.Query.ConstraintExpr()
        expression_pb = expression.encode()
        if isinstance(expression, And):
            constraint_expr_pb.and_.CopyFrom(expression_pb)
        elif isinstance(expression, Or):
            constraint_expr_pb.or_.CopyFrom(expression_pb)
        elif isinstance(expression, Not):
            constraint_expr_pb.not_.CopyFrom(expression_pb)
        elif isinstance(expression, Constraint):
            constraint_expr_pb.constraint.CopyFrom(expression_pb)

        return constraint_expr_pb

    @staticmethod
    def _decode(constraint_expression_protobuf_object) -> "ConstraintExpr":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        :param constraint_expression_protobuf_object: the protocol buffer object corresponding with this class.
        :return: A new instance of this class matching the protocol buffer object
        """
        expression = constraint_expression_protobuf_object.WhichOneof("expression")
        if expression == "and_":
            return And.decode(constraint_expression_protobuf_object.and_)
        elif expression == "or_":
            return Or.decode(constraint_expression_protobuf_object.or_)
        elif expression == "not_":
            return Not.decode(constraint_expression_protobuf_object.not_)
        elif expression == "constraint":
            return Constraint.decode(constraint_expression_protobuf_object.constraint)


class And(ConstraintExpr):
    """Implementation of the 'And' constraint expression."""

    def __init__(self, constraints: List[ConstraintExpr]):
        """
        Initialize an 'And' expression.

        :param constraints: the list of constraints expression (in conjunction).
        """
        self.constraints = constraints

    def check(self, description: Description) -> bool:
        """
        Check if a value satisfies the 'And' constraint expression.

        :param description: the description to check.
        :return: True if the description satisfy the constraint expression, False otherwise.
        """
        return all(expr.check(description) for expr in self.constraints)

    def is_valid(self, data_model: DataModel) -> bool:
        """
        Check whether the constraint expression is valid wrt a data model.

        :param data_model: the data model used to check the validity of the constraint expression.
        :return: ``True`` if the constraint expression is valid wrt the data model, ``False`` otherwise.
        """
        return all(constraint.is_valid(data_model) for constraint in self.constraints)

    def check_validity(self):
        """
        Check whether the Constraint Expression satisfies some basic requirements.

        :return ``None``
        :raises ValueError: if the object does not satisfy some requirements.
        """
        if len(self.constraints) < 2:  # pragma: nocover
            raise ValueError(
                "Invalid input value for type '{}': number of "
                "subexpression must be at least 2.".format(type(self).__name__)
            )
        for constraint in self.constraints:
            constraint.check_validity()

    def __eq__(self, other):  # pragma: nocover
        """Compare with another object."""
        return isinstance(other, And) and self.constraints == other.constraints

    def encode(self) -> models_pb2.Query.ConstraintExpr.And():
        """
        Encode an instance of this class into a protocol buffer object.

        :return: the matching protocol buffer object
        """
        and_pb = models_pb2.Query.ConstraintExpr.And()
        constraint_expr_pbs = [ConstraintExpr._encode(constraint) for constraint in self.constraints]
        and_pb.expr.extend(constraint_expr_pbs)
        return and_pb

    @classmethod
    def decode(cls, and_protobuf_object) -> "And":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        :param and_protobuf_object: the protocol buffer object corresponding with this class.
        :return: A new instance of this class matching the protocol buffer object
        """
        expr = [ConstraintExpr._decode(c) for c in and_protobuf_object.expr]
        return cls(expr)


class Or(ConstraintExpr):
    """Implementation of the 'Or' constraint expression."""

    def __init__(self, constraints: List[ConstraintExpr]):
        """
        Initialize an 'Or' expression.

        :param constraints: the list of constraints expressions (in disjunction).
        """
        self.constraints = constraints

    def check(self, description: Description) -> bool:
        """
        Check if a value satisfies the 'Or' constraint expression.

        :param description: the description to check.
        :return: True if the description satisfy the constraint expression, False otherwise.
        """
        return any(expr.check(description) for expr in self.constraints)

    def is_valid(self, data_model: DataModel) -> bool:
        """
        Check whether the constraint expression is valid wrt a data model.

        :param data_model: the data model used to check the validity of the constraint expression.
        :return: ``True`` if the constraint expression is valid wrt the data model, ``False`` otherwise.
        """
        return all(constraint.is_valid(data_model) for constraint in self.constraints)

    def check_validity(self):
        """
        Check whether the Constraint Expression satisfies some basic requirements.

        :return ``None``
        :raises ValueError: if the object does not satisfy some requirements.
        """
        if len(self.constraints) < 2:  # pragma: nocover
            raise ValueError(
                "Invalid input value for type '{}': number of "
                "subexpression must be at least 2.".format(type(self).__name__)
            )
        for constraint in self.constraints:
            constraint.check_validity()

    def __eq__(self, other):  # pragma: nocover
        """Compare with another object."""
        return isinstance(other, Or) and self.constraints == other.constraints

    def encode(self) -> models_pb2.Query.ConstraintExpr.Or():
        """
        Encode an instance of this class into a protocol buffer object.

        :return: the matching protocol buffer object
        """
        or_pb = models_pb2.Query.ConstraintExpr.Or()
        constraint_expr_pbs = [ConstraintExpr._encode(constraint) for constraint in self.constraints]
        or_pb.expr.extend(constraint_expr_pbs)
        return or_pb

    @classmethod
    def decode(cls, or_protobuf_object) -> "Or":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        :param or_protobuf_object: the protocol buffer object corresponding with this class.
        :return: A new instance of this class matching the protocol buffer object
        """
        expr = [ConstraintExpr._decode(c) for c in or_protobuf_object.expr]
        return cls(expr)


class Not(ConstraintExpr):
    """Implementation of the 'Not' constraint expression."""

    def __init__(self, constraint: ConstraintExpr):
        """
        Initialize a 'Not' expression.

        :param constraint: the constraint expression to negate.
        """
        self.constraint = constraint

    def check(self, description: Description) -> bool:
        """
        Check if a value satisfies the 'Not' constraint expression.

        :param description: the description to check.
        :return: True if the description satisfy the constraint expression, False otherwise.
        """
        return not self.constraint.check(description)

    def is_valid(self, data_model: DataModel) -> bool:
        """
        Check whether the constraint expression is valid wrt a data model.

        :param data_model: the data model used to check the validity of the constraint expression.
        :return: ``True`` if the constraint expression is valid wrt the data model, ``False`` otherwise.
        """
        return self.constraint.is_valid(data_model)

    def __eq__(self, other):  # pragma: nocover
        """Compare with another object."""
        return isinstance(other, Not) and self.constraint == other.constraint

    def encode(self) -> models_pb2.Query.ConstraintExpr.Not():
        """
        Encode an instance of this class into a protocol buffer object.

        :return: the matching protocol buffer object
        """
        not_pb = models_pb2.Query.ConstraintExpr.Not()
        constraint_expr_pb = ConstraintExpr._encode(self.constraint)
        not_pb.expr.CopyFrom(constraint_expr_pb)
        return not_pb

    @classmethod
    def decode(cls, not_protobuf_object) -> "Not":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        :param not_protobuf_object: the protocol buffer object corresponding with this class.
        :return: A new instance of this class matching the protocol buffer object
        """
        expression = ConstraintExpr._decode(not_protobuf_object.expr)
        return cls(expression)


class Constraint(ConstraintExpr):
    """The atomic component of a constraint expression."""

    def __init__(self, attribute_name: str, constraint_type: ConstraintType):
        """
        Initialize a constraint.

        :param attribute_name: the name of the attribute to be constrained.
        :param constraint_type: the constraint type.
        """
        self.attribute_name = attribute_name
        self.constraint_type = constraint_type

    def check(self, description: Description) -> bool:
        """
        Check if a description satisfies the constraint. The implementation depends on the type of the constraint.

        :param description: the description to check.
        :return: True if the description satisfies the constraint, False otherwise.

        Examples:
            >>> attr_author = Attribute("author" , str, True, "The author of the book.")
            >>> attr_year   = Attribute("year",    int, True, "The year of publication of the book.")
            >>> attr_genre   = Attribute("genre",  str, True, "The genre of the book.")
            >>> c1 = Constraint("author", ConstraintType("==", "Stephen King"))
            >>> c2 = Constraint("year", ConstraintType(">", 1990))
            >>> c3 = Constraint("genre", ConstraintType("in", {"horror", "science_fiction"}))
            >>> book_1 = Description({"author": "Stephen King",  "year": 1991, "genre": "horror"})
            >>> book_2 = Description({"author": "George Orwell", "year": 1948, "genre": "horror"})

            The "author" attribute instantiation satisfies the constraint, so the result is True.

            >>> c1.check(book_1)
            True

            Here, the "author" does not satisfy the constraints. Hence, the result is False.

            >>> c1.check(book_2)
            False

            In this case, there is a missing field specified by the query, that is "year"
            So the result is False, even in the case it is not required by the schema:

            >>> c2.check(Description({"author": "Stephen King"}))
            False

            If the type of some attribute of the description is not correct, the result is False.
            In this case, the field "year" has a string instead of an integer:

            >>> c2.check(Description({"author": "Stephen King", "year": "1991"}))
            False

            >>> c3.check(Description({"author": "Stephen King", "genre": False}))
            False

        """
        # if the name of the attribute is not present, return false.
        name = self.attribute_name
        if name not in description.values:
            return False

        # if the type of the value is different from the type of the attribute, return false.
        value = description.values[name]
        if type(self.constraint_type.value) in {list, tuple, set} and not isinstance(
            value, type(next(iter(self.constraint_type.value)))
        ):
            return False
        if type(self.constraint_type.value) not in {
            list,
            tuple,
            set,
        } and not isinstance(value, type(self.constraint_type.value)):
            return False

        # dispatch the check to the right implementation for the concrete constraint type.
        return self.constraint_type.check(value)

    def is_valid(self, data_model: DataModel) -> bool:
        """
        Check whether the constraint expression is valid wrt a data model.

        :param data_model: the data model used to check the validity of the constraint expression.
        :return: ``True`` if the constraint expression is valid wrt the data model, ``False`` otherwise.
        """
        # if the attribute name of the constraint is not present in the data model, the constraint is not valid.
        if self.attribute_name not in data_model.attributes_by_name:
            return False

        attribute = data_model.attributes_by_name[self.attribute_name]
        return self.constraint_type.is_valid(attribute)

    def __eq__(self, other):
        """Compare with another object."""
        return (
            isinstance(other, Constraint)
            and self.attribute_name == other.attribute_name
            and self.constraint_type == other.constraint_type
        )

    def __str__(self):
        """Get the string representation of the constraint."""
        return "Constraint(attribute_name={},constraint_type={})".format(
            self.attribute_name, self.constraint_type
        )

    def encode(self) -> models_pb2.Query.ConstraintExpr.Constraint():
        """
        Encode an instance of this class into a protocol buffer object.

        :return: the matching protocol buffer object
        """
        constraint = models_pb2.Query.ConstraintExpr.Constraint()
        constraint.attribute_name = self.attribute_name

        if (
            self.constraint_type.type == ConstraintTypes.EQUAL
            or self.constraint_type.type == ConstraintTypes.NOT_EQUAL
            or self.constraint_type.type == ConstraintTypes.LESS_THAN
            or self.constraint_type.type == ConstraintTypes.LESS_THAN_EQ
            or self.constraint_type.type == ConstraintTypes.GREATER_THAN
            or self.constraint_type.type == ConstraintTypes.GREATER_THAN_EQ
        ):
            constraint.relation.CopyFrom(self.constraint_type.encode())
        elif self.constraint_type.type == ConstraintTypes.WITHIN:
            constraint.range_.CopyFrom(self.constraint_type.encode())
        elif (
            self.constraint_type.type == ConstraintTypes.IN
            or self.constraint_type.type == ConstraintTypes.NOT_IN
        ):
            constraint.set_.CopyFrom(self.constraint_type.encode())
        elif self.constraint_type.type == ConstraintTypes.DISTANCE:
            constraint.distance.CopyFrom(self.constraint_type.encode())
        else:
            raise ValueError("The constraint type is not valid: {}".format(self.constraint_type))
        return constraint

    @classmethod
    def decode(cls, constraint_protobuf_object) -> "Constraint":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        :param constraint_protobuf_object: the protocol buffer object corresponding with this class.
        :return: A new instance of this class matching the protocol buffer object
        """
        constraint_case = constraint_protobuf_object.WhichOneof("constraint")
        constraint_type = None
        if constraint_case == "relation":
            constraint_type = ConstraintType.decode(constraint_protobuf_object.relation, "relation")
        elif constraint_case == "set_":
            constraint_type = ConstraintType.decode(constraint_protobuf_object.set_, "set")
        elif constraint_case == "range_":
            constraint_type = ConstraintType.decode(constraint_protobuf_object.range_, "range")
        elif constraint_case == "distance":
            constraint_type = ConstraintType.decode(constraint_protobuf_object.distance, "distance")

        return cls(constraint_protobuf_object.attribute_name, constraint_type)


class Query:
    """This class lets you build a query for the OEF."""

    def __init__(
        self, constraints: List[ConstraintExpr], model: Optional[DataModel] = None
    ) -> None:
        """
        Initialize a query.

        :param constraints: a list of constraint expressions.
        :param model: the data model that the query refers to.
        """
        self.constraints = constraints
        self.model = model
        self.check_validity()

    def check(self, description: Description) -> bool:
        """
        Check if a description satisfies the constraints of the query.

        The constraints are interpreted as conjunction.

        :param description: the description to check.
        :return: True if the description satisfies all the constraints, False otherwise.
        """
        return all(c.check(description) for c in self.constraints)

    def is_valid(self, data_model: DataModel) -> bool:
        """
        Given a data model, check whether the query is valid for that data model.

        :return: ``True`` if the query is compliant with the data model, ``False`` otherwise.
        """
        if data_model is None:
            return True

        return all(c.is_valid(data_model) for c in self.constraints)

    def check_validity(self):
        """
        Check whether the` object is valid.

        :return ``None``
        :raises ValueError: if the query does not satisfy some sanity requirements.
        """
        if not isinstance(self.constraints, list):
            raise ValueError(
                "Constraints must be a list (`List[Constraint]`). Instead is of type '{}'.".format(
                    type(self.constraints).__name__
                )
            )
        if len(self.constraints) < 1:
            _default_logger.warning(
                "DEPRECATION WARNING: "
                "Invalid input value for type '{}': empty list of constraints. The number of "
                "constraints must be at least 1.".format(type(self).__name__)
            )
        if not self.is_valid(self.model):
            raise ValueError(
                "Invalid input value for type '{}': the query is not valid "
                "for the given data model.".format(type(self).__name__)
            )

    def __eq__(self, other):
        """Compare with another object."""
        return (
            isinstance(other, Query)
            and self.constraints == other.constraints
            and self.model == other.model
        )

    def __str__(self):
        """Get the string representation of the constraint."""
        return "Query(constraints={},model={})".format(
            [str(c) for c in self.constraints], self.model
        )

    def encode(self) -> models_pb2.Query.Model():
        """
        Encode an instance of this class into a protocol buffer object.

        :return: the matching protocol buffer object
        """
        query = models_pb2.Query.Model()
        constraint_expr_pbs = [ConstraintExpr._encode(constraint) for constraint in self.constraints]
        query.constraints.extend(constraint_expr_pbs)

        if self.model is not None:
            query.model.CopyFrom(self.model.encode())
        return query

    @classmethod
    def decode(cls, query_protobuf_object) -> "Query":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        :param query_protobuf_object: the protocol buffer object corresponding with this class.
        :return: A new instance of this class matching the protocol buffer object
        """
        constraints = [ConstraintExpr._decode(c) for c in query_protobuf_object.constraints]
        return cls(constraints, DataModel.decode(query_protobuf_object.model) if query_protobuf_object.HasField("model") else None)


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Compute the Haversine distance between two locations (i.e. two pairs of latitude and longitude).

    :param lat1: the latitude of the first location.
    :param lon1: the longitude of the first location.
    :param lat2: the latitude of the second location.
    :param lon2: the longitude of the second location.
    :return: the Haversine distance.
    """
    lat1, lon1, lat2, lon2, = map(radians, [lat1, lon1, lat2, lon2])
    # average earth radius
    earth_radius = 6372.8
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    sin_lat_squared = sin(dlat * 0.5) * sin(dlat * 0.5)
    sin_lon_squared = sin(dlon * 0.5) * sin(dlon * 0.5)
    computation = asin(sqrt(sin_lat_squared + sin_lon_squared * cos(lat1) * cos(lat2)))
    d = 2 * earth_radius * computation
    return d
