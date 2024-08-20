"""This module defines several custom type annotations for use in applications
where specific data types need to be more clearly represented. These types are
created using the `NewType` helper function from the `typing` module, which
creates distinct types based on existing ones, but they are still treated as
their base types by the Python interpreter. used to emphasize its role in
representing time in seconds.

Usage:
    These types can be used in function signatures, class attributes,
    and other places where you want to make clear that a specific
    kind of value is expected or being used, rather than a general
    integer or string.

"""

from typing import NewType

MegaByte = NewType("MegaByte", int)
Byte = NewType("Byte", int)
Second = NewType("Second", int)
Minute = NewType("Minute", float)

Dimension = NewType("Dimension", str)
Day = NewType("Day", int)
Second = NewType("Second", int)
