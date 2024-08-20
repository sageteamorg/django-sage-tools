"""This module provides a set of functions to convert between different units
of measurement.

It includes conversions between bytes and megabytes, days and seconds,
and seconds and minutes.

"""

from sage_tools.helpers.typings import Byte, Day, MegaByte, Minute, Second


class UnitConvertor:
    """A utility class for converting units between various scales of
    measurement.

    This class provides static methods for converting between bytes and
    megabytes, days and seconds, and seconds and minutes.

    """

    @staticmethod
    def convert_byte_to_megabyte(value: Byte) -> MegaByte:
        """Convert bytes to megabytes.

        :param value: The number of bytes.
        :type value: Byte
        :return: The equivalent number of megabytes.
        :rtype: MegaByte

        """
        return value * 1e-6

    @staticmethod
    def convert_megabyte_to_byte(value: MegaByte) -> Byte:
        """Convert megabytes to bytes.

        :param value: The number of megabytes.
        :type value: MegaByte
        :return: The equivalent number of bytes.
        :rtype: Byte

        """
        return value * 1_000_000

    @staticmethod
    def convert_days_to_seconds(value: Day) -> Second:
        """Convert days to seconds.

        :param value: The number of days.
        :type value: Day
        :return: The equivalent number of seconds.
        :rtype: Second

        """
        return 60 * 60 * 24 * value

    @staticmethod
    def convert_seconds_to_minutes(value: Second) -> Minute:
        """Convert seconds to minutes.

        :param value: The number of seconds.
        :type value: Second
        :return: The equivalent number of minutes.
        :rtype: Minute

        """
        return value / 60.0

    @staticmethod
    def convert_minutes_to_seconds(value: Minute) -> Second:
        """Convert minutes to seconds.

        :param value: The number of minutes.
        :type value: Minute
        :return: The equivalent number of seconds.
        :rtype: Second

        """
        return int(value * 60)
