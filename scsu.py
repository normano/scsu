#!/usr/bin/env python3
# -*- coding: us-ascii -*-


class SCSU:

    SIGNATURE = b'\x0e\xfe\xff'

    TAG_SQ0 = 0x01
    TAG_SQ1 = 0x02
    TAG_SQ2 = 0x03
    TAG_SQ3 = 0x04
    TAG_SQ4 = 0x05
    TAG_SQ5 = 0x06
    TAG_SQ6 = 0x07
    TAG_SQ7 = 0x08
    TAG_SQn = (TAG_SQ0, TAG_SQ1, TAG_SQ2, TAG_SQ3, TAG_SQ4, TAG_SQ5, TAG_SQ6, TAG_SQ7)

    TAG_SDX = 0x0B
    TAG_SRX = 0x0C
    TAG_SQU = 0x0E
    TAG_SCU = 0x0F

    TAG_SC0 = 0x10
    TAG_SC1 = 0x11
    TAG_SC2 = 0x12
    TAG_SC3 = 0x13
    TAG_SC4 = 0x14
    TAG_SC5 = 0x15
    TAG_SC6 = 0x16
    TAG_SC7 = 0x17
    TAG_SCn = (TAG_SC0, TAG_SC1, TAG_SC2, TAG_SC3, TAG_SC4, TAG_SC5, TAG_SC6, TAG_SC7)

    TAG_SD0 = 0x18
    TAG_SD1 = 0x19
    TAG_SD2 = 0x1A
    TAG_SD3 = 0x1B
    TAG_SD4 = 0x1C
    TAG_SD5 = 0x1D
    TAG_SD6 = 0x1E
    TAG_SD7 = 0x1F
    TAG_SDn = (TAG_SD0, TAG_SD1, TAG_SD2, TAG_SD3, TAG_SD4, TAG_SD5, TAG_SD6, TAG_SD7)

    TAG_UC0 = 0xE0
    TAG_UC1 = 0xE1
    TAG_UC2 = 0xE2
    TAG_UC3 = 0xE3
    TAG_UC4 = 0xE4
    TAG_UC5 = 0xE5
    TAG_UC6 = 0xE6
    TAG_UC7 = 0xE7
    TAG_UCn = (TAG_UC0, TAG_UC1, TAG_UC2, TAG_UC3, TAG_UC4, TAG_UC5, TAG_UC6, TAG_UC7)

    TAG_UD0 = 0xE8
    TAG_UD1 = 0xE9
    TAG_UD2 = 0xEA
    TAG_UD3 = 0xEB
    TAG_UD4 = 0xEC
    TAG_UD5 = 0xED
    TAG_UD6 = 0xEE
    TAG_UD7 = 0xEF
    TAG_UDn = (TAG_UD0, TAG_UD1, TAG_UD2, TAG_UD3, TAG_UD4, TAG_UD5, TAG_UD6, TAG_UD7)

    TAG_UQU = 0xF0
    TAG_UDX = 0xF1
    TAG_URX = 0xF2

    MODE_SINGLE_BYTE = 1
    MODE_UNICODE = 2

    SPECIAL_WINDOW_POSITIONS = {
        0xF9: 0x00C0,
        0xFA: 0x0250,
        0xFB: 0x0370,
        0xFC: 0x0530,
        0xFD: 0x3040,
        0xFE: 0x30A0,
        0xFF: 0xFF60
    }

    static_window_keys = (0x00, 0x01, 0x02, 0x06, 0x40, 0x41, 0x42, 0x60)
    static_window_positions = (0x0000, 0x0080, 0x0100, 0x0300, 0x2000, 0x2080, 0x2100, 0x3000)

    default_dynamic_window_keys = (0x01, 0xF9, 0x08, 0x0C, 0x12, 0xFD, 0xFE, 0xA6)
    default_dynamic_window_positions = (0x0080, 0x00C0, 0x0400, 0x0600, 0x0900, 0x3040, 0x30A0, 0xFF00)

    default_dynamic_window_key = 0x01
    default_dynamic_window_position = 0x0080

    @staticmethod
    def codepoint_is_ascii(codepoint: int) -> bool:
        """
        Determine if a given codepoint can be represented with a single octet the 7-bit ASCII character set.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :rtype: bool
        :return: True if the Unicode codepoint is in ASCII; false otherwise.
        """
        return codepoint <= 127

    @staticmethod
    def octet_conflicts_with_reserved_octet(octet: int) -> bool:
        """
        Determine if a given octet needs to be preceded with an SQ0 octet when used in single-byte mode.

        :type octet: int
        :param octet: An integer between 0 and 255, inclusive.
        :rtype: bool
        :return: True if the given octet requires escaping; false otherwise.
        """
        return (octet in SCSU.TAG_SQn) or octet == SCSU.TAG_SDX or octet == SCSU.TAG_SRX or octet == SCSU.TAG_SQU \
            or octet == SCSU.TAG_SCU or (octet in SCSU.TAG_SCn) or (octet in SCSU.TAG_SDn)

    @staticmethod
    def encode_codepoint_as_utf16be_array(codepoint: int) -> list:
        """
        Encode a Unicode codepoint as a list of octets representing a UTF-16 big endian string.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :rtype: list
        :return: A list of two or four octets.
        """
        return list(chr(codepoint).encode('UTF-16BE'))

    @staticmethod
    def octet_conflicts_with_reserved_unicode_hbyte(octet: int) -> bool:
        """
        Determine if a given octet needs to be preceded with an UQU octet when used in Unicode mode.

        :type octet: int
        :param octet: An integer between 0 and 255, inclusive.
        :rtype: bool
        :return: True if the given octet requires escaping; false otherwise.
        """
        return (octet in SCSU.TAG_UCn) or (octet in SCSU.TAG_UDn) or octet == SCSU.TAG_UQU or octet == SCSU.TAG_UDX \
            or octet == SCSU.TAG_URX

    @staticmethod
    def codepoint_is_compressible(codepoint: int) -> bool:
        """
        Determine if a given octet can be "compressed" by putting it in a window.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :rtype: bool
        :return: True if the given codepoint can be compressed; false otherwise.
        """
        return codepoint < 0x3400 or codepoint >= 0xE000

    @staticmethod
    def codepoint_is_in_bmp(codepoint: int) -> bool:
        """
        Determine if a given codepoint is in the Basic Multilingual Plane.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :rtype: bool
        :return: True if the given codepoint is in the BMP; false otherwise.
        """
        return codepoint <= 0xFFFF

    @staticmethod
    def codepoint_fits_in_window(codepoint: int, window_position: int) -> bool:
        """
        Determine if a given codepoint fits in a defined window position.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :type window_position: int
        :param window_position: The Unicode codepoint for the window position.
        :rtype: bool
        :return: True if the given codepoint fits in the window; false otherwise.
        """
        return window_position <= codepoint <= (window_position + 127)

    @staticmethod
    def codepoint_fits_in_any_static_window(codepoint: int) -> bool:
        """
        Determine if the given codepoint fits in any static window.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :rtype: bool
        :return: True if the given codepoint fits in any static window; false otherwise.
        """
        return any([SCSU.codepoint_fits_in_window(codepoint, w) for w in SCSU.static_window_positions])

    @staticmethod
    def find_static_window_index_for_codepoint(codepoint: int) -> int:
        """
        Find a static window that a given codepoint fits in.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :rtype: int
        :return: The static window that the codepoint fits in.
        """
        assert SCSU.codepoint_fits_in_any_static_window(codepoint)
        return next((static_window_index for static_window_index, static_window_position
                     in enumerate(SCSU.static_window_positions)
                     if SCSU.codepoint_fits_in_window(codepoint, static_window_position)), None)

    @staticmethod
    def codepoint_in_static_window_as_encoded_octet(codepoint: int, window_position: int) -> int:
        """
        Encode a codepoint as an octet for a given static window position.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :type window_position: int
        :param window_position: The Unicode codepoint for the static window position.
        :rtype: int
        :return: The octet for a codepoint in a static window.
        """
        assert SCSU.codepoint_fits_in_window(codepoint, window_position)
        return codepoint - window_position

    @staticmethod
    def codepoint_in_dynamic_window_as_encoded_octet(codepoint: int, window_position: int) -> int:
        """
        Encode a codepoint as an octet for a given dynamic window position.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :type window_position: int
        :param window_position: The Unicode codepoint for the dynamic window position.
        :rtype: int
        :return: The octet for a codepoint in a dynamic window.
        """
        assert SCSU.codepoint_fits_in_window(codepoint, window_position)
        return (codepoint - window_position) + 128

    @staticmethod
    def get_window_key_for_window_position(window_position: int) -> int:
        """
        Compute the window key for a given window position.

        :type window_position: int
        :param window_position: The Unicode codepoint for the window position.
        :rtype: int
        :return: The octet for selecting a window position.
        """
        assert SCSU.codepoint_is_in_bmp(window_position) and SCSU.codepoint_is_compressible(window_position)

        # If the window position is zero, the window key is zero.
        if window_position == 0:
            return 0

        # Iterate through each special window position and check if the special window position matches the given
        # window position.
        special_window_key = next((index for index, special_window_position
                                   in enumerate(SCSU.SPECIAL_WINDOW_POSITIONS)
                                   if special_window_position == window_position), None)

        # If the window position matches a special window position, return that.
        if special_window_key is not None:
            return special_window_key

        # Is the window position before the end of the CJK Compatibility block?
        if window_position <= 0x33FF:
            window_key = window_position >> 7
            return window_key

        # Is the window position in or after the Private Use Area?
        if window_position >= 0xE000:
            window_key = (window_position - 0xAC00) >> 7
            return window_key

    @staticmethod
    def find_window_position_for_codepoint(codepoint: int) -> int:
        """
        Find the Unicode codepoint for a window position that contains a given Unicode codepoint.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :rtype: int
        :return: The Unicode codepoint for the window position.
        """
        assert SCSU.codepoint_is_in_bmp(codepoint) and SCSU.codepoint_is_compressible(codepoint)

        # If the codepoint is in the ASCII range, the window position is zero.
        if SCSU.codepoint_is_ascii(codepoint):
            return 0

        # Iterate through each special window position and check if the codepoint fits in any of those windows.
        special_window_position = next((window_position for index, window_position
                                        in enumerate(SCSU.SPECIAL_WINDOW_POSITIONS)
                                        if SCSU.codepoint_fits_in_window(codepoint, window_position)), None)

        # If we found a special window position, return that.
        if special_window_position is not None:
            return special_window_position

        # Compute a window position for the half-block the codepoint is in and use that value.
        window_position = codepoint & ~0x7F
        return window_position

    @staticmethod
    def encode_supplementary_codepoint_window_base(dynamic_window_index: int, codepoint: int) -> tuple:
        """
        Encode the dynamic window index and window position for a supplementary codepoint into a 16-bit integer and
        split that integer into a big-endian tuple of two octets.

        :type dynamic_window_index: int
        :param dynamic_window_index: The dynamic window index.
        :param codepoint: The Unicode codepoint.
        :rtype: tuple
        :return: A tuple containing two octets.
        """
        assert 0 <= dynamic_window_index < 8
        assert not SCSU.codepoint_is_in_bmp(codepoint)

        codepoint_window_base = (dynamic_window_index << 13) | ((codepoint - 0x10000) >> 7)
        return codepoint_window_base >> 8, codepoint_window_base & 0xFF


class SCSUEncoder(SCSU):

    current_mode = None

    dynamic_window_keys = None
    dynamic_window_positions = None

    current_dynamic_window_key = None
    current_dynamic_window_position = None

    used_dynamic_window_index_list = None

    def __init__(self):
        """
        Instantiate a SCSU encoder object.
        """

        self.reset()

    def reset(self):
        """
        Reset the internal codec status.
        """
        self.current_mode = self.MODE_SINGLE_BYTE

        self.dynamic_window_keys = list(self.default_dynamic_window_keys)
        self.dynamic_window_positions = list(self.default_dynamic_window_positions)

        self.current_dynamic_window_key = self.default_dynamic_window_key
        self.current_dynamic_window_position = self.default_dynamic_window_position

        self.used_dynamic_window_index_list = list(range(8))

    def codepoint_fits_in_current_dynamic_window(self, codepoint: int) -> bool:
        """
        Determine if a given codepoint fits in the current dynamic window.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :rtype: bool
        :return: True if the given codepoint fits in the current dynamic window; false otherwise.
        """
        return self.codepoint_fits_in_window(codepoint, self.current_dynamic_window_position)

    def codepoint_fits_in_any_dynamic_window(self, codepoint: int) -> bool:
        """
        Determine if the given codepoint fits in any currently defined dynamic window.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :rtype: bool
        :return: True if the given codepoint fits in any dynamic window; false otherwise.
        """
        return any([self.codepoint_fits_in_window(codepoint, w) for w in self.dynamic_window_positions])

    def find_dynamic_window_index_for_codepoint(self, codepoint: int) -> int:
        """
        Find a dynamic window that a given codepoint fits in.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :rtype: int
        :return: The dynamic window that the codepoint fits in.
        """
        assert self.codepoint_fits_in_any_dynamic_window(codepoint)
        return next((dynamic_window_index for dynamic_window_index, dynamic_window_position
                     in enumerate(self.dynamic_window_positions)
                     if self.codepoint_fits_in_window(codepoint, dynamic_window_position)), None)

    def codepoint_in_current_dynamic_window_as_encoded_octet(self, codepoint: int) -> int:
        """
        Encode a codepoint as an octet for the current dynamic window position.

        :type codepoint: int
        :param codepoint: The Unicode codepoint.
        :rtype: int
        :return: The octet for a codepoint in the current dynamic window.
        """
        assert self.codepoint_fits_in_current_dynamic_window(codepoint)
        return (codepoint - self.current_dynamic_window_position) + 128

    def get_unused_dynamic_window_index(self) -> int:
        """
        Get an unused, or rarely used, dynamic window index.

        :rtype: int
        :return: A dynamic window index.
        """
        return self.used_dynamic_window_index_list[-1]

    def move_dynamic_window_index_to_front(self, dynamic_window_index: int):
        """
        Move a dynamic window index to the front of the dynamic window index list.

        :type dynamic_window_index: int
        :param dynamic_window_index: The dynamic window index.
        """
        assert 0 <= dynamic_window_index < 8

        if self.used_dynamic_window_index_list[0] != dynamic_window_index:
            self.used_dynamic_window_index_list.remove(dynamic_window_index)
            self.used_dynamic_window_index_list.insert(0, dynamic_window_index)

    def train(self, unicode_string: str):
        """
        Train the compressor by analyzing a Unicode string and rearranging the dynamic window availability.

        :type unicode_string: str
        :param unicode_string: The Unicode string to analyze.
        """

        # Define a dictionary for counting the use of each dynamic window and set the counts to zero.
        dynamic_window_usage = {dynamic_window_index: 0 for dynamic_window_index in self.used_dynamic_window_index_list}

        # Iterate through each character.
        for current_character in unicode_string:

            # Convert the current character to an integer.
            current_codepoint = ord(current_character)

            # Does the current codepoint fit in any of the defined dynamic windows?
            if self.codepoint_fits_in_any_dynamic_window(current_codepoint):

                # Find the dynamic window index that the current codepoint fits in.
                dynamic_window_index = self.find_dynamic_window_index_for_codepoint(current_codepoint)

                # Increment the count for the dynamic window index.
                dynamic_window_usage[dynamic_window_index] += 1

        # Sort the dictionary by the value in reverse and store the resulting list.
        dynamic_window_index_list = sorted(dynamic_window_usage, key=dynamic_window_usage.get, reverse=True)
        self.used_dynamic_window_index_list = dynamic_window_index_list

    def encode(self, unicode_string: str) -> bytearray:
        """
        Encode a Unicode string into a SCSU byte array.

        :type unicode_string: str
        :param unicode_string: The Unicode string to encode.
        :rtype: bytearray
        :return: The encoded byte array.
        """

        # Get the last index of the Unicode string.
        last_index = len(unicode_string) - 1

        # Temporarily store the return value in a byte array.
        encoded_byte_array = bytearray()

        # Iterate through each character.
        for current_index, current_character in enumerate(unicode_string):

            # Convert the current character to an integer.
            current_codepoint = ord(current_character)

            # Convert the next character into an integer, or use None if there is no next character.
            next_codepoint = ord(unicode_string[current_index + 1]) \
                if current_index < last_index else None

            # Are we in single-byte mode?
            if self.current_mode == self.MODE_SINGLE_BYTE:

                # Is the current codepoint in the ASCII range?
                if self.codepoint_is_ascii(current_codepoint):

                    # Does the octet conflict with a reserved octet?
                    if self.octet_conflicts_with_reserved_octet(current_codepoint):

                        # Output an SQ0 tag.
                        encoded_byte_array.append(self.TAG_SQ0)

                    # Output the codepoint as a single byte.
                    encoded_byte_array.append(current_codepoint)

                # Otherwise, is the current codepoint compressible?
                elif self.codepoint_is_compressible(current_codepoint):

                    # Does the current codepoint fit in the current dynamic window?
                    if self.codepoint_fits_in_current_dynamic_window(current_codepoint):

                        # Output the codepoint as an encoded octet for the current dynamic window.
                        encoded_byte_array.append(
                            self.codepoint_in_current_dynamic_window_as_encoded_octet(current_codepoint)
                        )

                    # Does the current codepoint fit in any of the defined dynamic windows?
                    elif self.codepoint_fits_in_any_dynamic_window(current_codepoint):

                        # Find the dynamic window index that the current codepoint fits in.
                        new_dynamic_window_index = self.find_dynamic_window_index_for_codepoint(current_codepoint)

                        # Get the position of the new dynamic window.
                        new_dynamic_window_position = self.dynamic_window_positions[new_dynamic_window_index]

                        # Encode the current codepoint as an octet in the temporary dynamic window.
                        new_dynamic_window_octet = \
                            self.codepoint_in_dynamic_window_as_encoded_octet(current_codepoint,
                                                                              new_dynamic_window_position)

                        # Does the next codepoint fit in the current dynamic window?
                        if next_codepoint is not None \
                                and self.codepoint_fits_in_current_dynamic_window(next_codepoint):

                            # Output an SQn tag followed by an encoded codepoint.
                            encoded_byte_array.append(self.TAG_SQn[new_dynamic_window_index])
                            encoded_byte_array.append(new_dynamic_window_octet)

                        # We don't have a character after this one, or the next codepoint isn't in the current dynamic
                        # window.
                        else:

                            # Get the window key for the new new dynamic window position.
                            new_dynamic_window_key = self.dynamic_window_keys[new_dynamic_window_index]

                            # Output an SCn tag followed by an encoded codepoint.
                            encoded_byte_array.append(self.TAG_SCn[new_dynamic_window_index])
                            encoded_byte_array.append(new_dynamic_window_octet)

                            # Set the current dynamic window to the new dynamic window.
                            self.current_dynamic_window_key = new_dynamic_window_key
                            self.current_dynamic_window_position = new_dynamic_window_position

                            # Move the new dynamic window index to the front of the used dynamic window index list.
                            self.move_dynamic_window_index_to_front(new_dynamic_window_index)

                    # Is the current codepoint in the Basic Multilingual Plane?
                    elif self.codepoint_is_in_bmp(current_codepoint):

                        # Does the current codepoint fit in the any of the static windows?
                        if self.codepoint_fits_in_any_static_window(current_codepoint):

                            # Find the static window index that the current codepoint fits in.
                            static_window_index = self.find_static_window_index_for_codepoint(current_codepoint)

                            # Get the position of the static window.
                            static_window_position = self.static_window_positions[static_window_index]

                            # Encode the current codepoint as an octet in the static window.
                            static_window_octet = \
                                self.codepoint_in_static_window_as_encoded_octet(current_codepoint,
                                                                                 static_window_position)

                            # Output an SQn tag for that window, followed by the static window octet.
                            encoded_byte_array.append(self.TAG_SQn[static_window_index])
                            encoded_byte_array.append(static_window_octet)

                        # The current codepoint doesn't fit in any of the static windows.
                        else:

                            # Get an unused (or rarely used) dynamic window index.
                            unused_dynamic_window_index = self.get_unused_dynamic_window_index()
                            new_dynamic_window_index = unused_dynamic_window_index

                            # Find a window position that the current character fits in.
                            new_dynamic_window_position = self.find_window_position_for_codepoint(current_codepoint)

                            # Find a window key for the window position.
                            new_dynamic_window_key = \
                                self.get_window_key_for_window_position(new_dynamic_window_position)

                            # Set the new current dynamic window key and position.
                            self.current_dynamic_window_key = new_dynamic_window_key
                            self.current_dynamic_window_position = new_dynamic_window_position

                            # Remember the new dynamic window key and position in the key and position lists.
                            self.dynamic_window_keys[new_dynamic_window_index] = new_dynamic_window_key
                            self.dynamic_window_positions[new_dynamic_window_index] = new_dynamic_window_position

                            # Move the new dynamic window index to the front of the used dynamic window index list.
                            self.move_dynamic_window_index_to_front(new_dynamic_window_index)

                            # Output an SDn tag followed by an encoded dynamic window position.
                            encoded_byte_array.append(self.TAG_SDn[new_dynamic_window_index])
                            encoded_byte_array.append(new_dynamic_window_key)

                            # Encode the current codepoint as an octet in the new dynamic window.
                            new_dynamic_window_octet = \
                                self.codepoint_in_dynamic_window_as_encoded_octet(current_codepoint,
                                                                                  new_dynamic_window_position)

                            # Output the encoded codepoint.
                            encoded_byte_array.append(new_dynamic_window_octet)

                    # The current codepoint is in the supplementary code space.
                    else:

                        # Get an unused (or rarely used) dynamic window index.
                        unused_dynamic_window_index = self.get_unused_dynamic_window_index()
                        new_dynamic_window_index = unused_dynamic_window_index

                        # Encoding the new dynamic window position for a supplementary codepoint only involves clearing
                        # the seven least significant bits from the codepoint.
                        new_dynamic_window_position = current_codepoint & ~0x7F

                        # There is no current dynamic window key for supplementary codepoints.
                        self.current_dynamic_window_key = None
                        self.current_dynamic_window_position = new_dynamic_window_position

                        # Move the new dynamic window index to the front of the userd dynamic window index list.
                        self.move_dynamic_window_index_to_front(new_dynamic_window_index)

                        # Encode the new dynamic window index with the supplementary codepoint as two octets.
                        hbyte, lbyte = self.encode_supplementary_codepoint_window_base(new_dynamic_window_index,
                                                                                       current_codepoint)

                        # Output an SDX tag followed by the encoded octets for the dynamic window index and
                        # supplementary codepoint.
                        encoded_byte_array.append(self.TAG_SDX)
                        encoded_byte_array.append(hbyte)
                        encoded_byte_array.append(lbyte)

                        # Encode the current codepoint as an octet in the new dynamic window.
                        new_dynamic_window_octet = \
                            self.codepoint_in_dynamic_window_as_encoded_octet(current_codepoint,
                                                                              new_dynamic_window_position)

                        # Output the encoded codepoint.
                        encoded_byte_array.append(new_dynamic_window_octet)

                # The current codepoint is not compressible.
                else:

                    # Is the current codepoint in the Basic Multilingual Plane, and is the next codepoint compressible?
                    if self.codepoint_is_in_bmp(current_codepoint) and \
                                    next_codepoint is not None and self.codepoint_is_compressible(next_codepoint):

                        # Output an SQU tag.
                        encoded_byte_array.append(self.TAG_SQU)

                        # Encode the current codepoint as a UTF-16 big-endian octet array.
                        hbyte, lbyte = self.encode_codepoint_as_utf16be_array(current_codepoint)

                        # Output the two codepoint octets.
                        encoded_byte_array.append(hbyte)
                        encoded_byte_array.append(lbyte)

                    # The current codepoint is not in the Basic Multilingual Plane, or the next codepoint is not
                    # compressible.
                    else:

                        # Output an SCU tag and switch to Unicode mode.
                        encoded_byte_array.append(self.TAG_SCU)
                        self.current_mode = self.MODE_UNICODE

                        # Encode the current codepoint as a UTF-16 big-endian octet array.
                        current_codepoint_octets = self.encode_codepoint_as_utf16be_array(current_codepoint)

                        # Iterate through each two codepoint octets.
                        for hbyte, lbyte in [current_codepoint_octets[octet_index:octet_index + 2]
                                             for octet_index in range(0, len(current_codepoint_octets), 2)]:

                            # Does the high byte conflict with a reserved Unicode high byte?
                            if self.octet_conflicts_with_reserved_unicode_hbyte(hbyte):
                                # Output a UQU tag.
                                encoded_byte_array.append(self.TAG_UQU)

                            # Output the two codepoint octets.
                            encoded_byte_array.append(hbyte)
                            encoded_byte_array.append(lbyte)

            # We are in Unicode mode.
            else:

                # Is the current codepoint compressible, and is the next codepoint compressible?
                if self.codepoint_is_compressible(current_codepoint) \
                        and next_codepoint is not None and self.codepoint_is_compressible(next_codepoint):

                    # Is the current codepoint in the ASCII range?
                    if self.codepoint_is_ascii(current_codepoint):

                        # Get the last dynamic window used.
                        new_dynamic_window_index = self.used_dynamic_window_index_list[0]

                        # Get the position of the new dynamic window.
                        new_dynamic_window_position = self.dynamic_window_positions[new_dynamic_window_index]

                        # Get the window key for the new new dynamic window position.
                        new_dynamic_window_key = self.dynamic_window_keys[new_dynamic_window_index]

                        # Encode the current codepoint as an octet in the current dynamic window.
                        new_dynamic_window_octet = \
                            self.codepoint_in_dynamic_window_as_encoded_octet(current_codepoint,
                                                                              new_dynamic_window_position)

                        # Output a UCn tag for the last-used dynamic window and switch to single-byte mode.
                        encoded_byte_array.append(self.TAG_UCn[new_dynamic_window_index])
                        encoded_byte_array.append(new_dynamic_window_octet)
                        self.current_mode = self.MODE_SINGLE_BYTE

                        # Set the current dynamic window to the new dynamic window.
                        self.current_dynamic_window_key = new_dynamic_window_key
                        self.current_dynamic_window_position = new_dynamic_window_position

                    # Does the current codepoint fit in any of the defined dynamic windows?
                    elif self.codepoint_fits_in_any_dynamic_window(current_codepoint):

                        # Find the dynamic window index that the current codepoint fits in.
                        new_dynamic_window_index = self.find_dynamic_window_index_for_codepoint(current_codepoint)

                        # Get the position of the new dynamic window.
                        new_dynamic_window_position = self.dynamic_window_positions[new_dynamic_window_index]

                        # Get the window key for the new new dynamic window position.
                        new_dynamic_window_key = self.dynamic_window_keys[new_dynamic_window_index]

                        # Encode the current codepoint as an octet in the new dynamic window.
                        new_dynamic_window_octet = \
                            self.codepoint_in_dynamic_window_as_encoded_octet(current_codepoint,
                                                                              new_dynamic_window_position)

                        # Set the current dynamic window to the new dynamic window.
                        self.current_dynamic_window_key = new_dynamic_window_key
                        self.current_dynamic_window_position = new_dynamic_window_position

                        # Output a UCn tag for the new dynamic window and switch to single-byte mode.
                        encoded_byte_array.append(self.TAG_UCn[new_dynamic_window_index])
                        encoded_byte_array.append(new_dynamic_window_octet)
                        self.current_mode = self.MODE_SINGLE_BYTE

                    # Is the current codepoint in the Basic Multilingual Plane?
                    elif self.codepoint_is_in_bmp(current_codepoint):

                        # Get an unused (or rarely used) dynamic window index.
                        unused_dynamic_window_index = self.get_unused_dynamic_window_index()
                        new_dynamic_window_index = unused_dynamic_window_index

                        # Find a window position that the current character fits in.
                        new_dynamic_window_position = self.find_window_position_for_codepoint(current_codepoint)

                        # Find a window key for the window position.
                        new_dynamic_window_key = \
                            self.get_window_key_for_window_position(new_dynamic_window_position)

                        # Set the new current dynamic window key and position.
                        self.current_dynamic_window_key = new_dynamic_window_key
                        self.current_dynamic_window_position = new_dynamic_window_position

                        # Move the new dynamic window index to the front of the used dynamic window index list.
                        self.move_dynamic_window_index_to_front(new_dynamic_window_index)

                        # Output a UDn tag followed by an encoded dynamic window position and switch to single-byte
                        # mode.
                        encoded_byte_array.append(self.TAG_UDn[new_dynamic_window_index])
                        encoded_byte_array.append(new_dynamic_window_key)
                        self.current_mode = self.MODE_SINGLE_BYTE

                        # Encode the current codepoint as an octet in the new dynamic window.
                        new_dynamic_window_octet = \
                            self.codepoint_in_dynamic_window_as_encoded_octet(current_codepoint,
                                                                              new_dynamic_window_position)

                        # Output the encoded codepoint.
                        encoded_byte_array.append(new_dynamic_window_octet)

                    # The current codepoint is in the supplementary code space.
                    else:

                        # Get an unused (or rarely used) dynamic window index.
                        unused_dynamic_window_index = self.get_unused_dynamic_window_index()
                        new_dynamic_window_index = unused_dynamic_window_index

                        # Encoding the new dynamic window position for a supplementary codepoint only involves clearing
                        # the seven least significant bits from the codepoint.
                        new_dynamic_window_position = current_codepoint & ~0x7F

                        # There is no current dynamic window key for supplementary codepoints.
                        self.current_dynamic_window_key = None
                        self.current_dynamic_window_position = new_dynamic_window_position

                        # Move the new dynamic window index to the front of the userd dynamic window index list.
                        self.move_dynamic_window_index_to_front(new_dynamic_window_index)

                        # Encode the new dynamic window index with the supplementary codepoint as two octets.
                        hbyte, lbyte = self.encode_supplementary_codepoint_window_base(new_dynamic_window_index,
                                                                                       current_codepoint)

                        # Output a UDX tag followed by the encoded octets for the dynamic window index and
                        # supplementary codepoint and switch to single-byte mode.
                        encoded_byte_array.append(self.TAG_UDX)
                        encoded_byte_array.append(hbyte)
                        encoded_byte_array.append(lbyte)
                        self.current_mode = self.MODE_SINGLE_BYTE

                        # Encode the current codepoint as an octet in the new dynamic window.
                        new_dynamic_window_octet = \
                            self.codepoint_in_dynamic_window_as_encoded_octet(current_codepoint,
                                                                              new_dynamic_window_position)

                        # Output the encoded codepoint.
                        encoded_byte_array.append(new_dynamic_window_octet)

                # The current codepoint and the next codepoint are not both compressible.
                else:

                    # Encode the current codepoint as a UTF-16 big-endian octet array.
                    current_codepoint_octets = self.encode_codepoint_as_utf16be_array(current_codepoint)

                    # Iterate through each two codepoint octets.
                    for hbyte, lbyte in [current_codepoint_octets[octet_index:octet_index+2]
                                         for octet_index in range(0, len(current_codepoint_octets), 2)]:

                        # Does the high byte conflict with a reserved Unicode high byte?
                        if self.octet_conflicts_with_reserved_unicode_hbyte(hbyte):

                            # Output a UQU tag.
                            encoded_byte_array.append(self.TAG_UQU)

                        # Output the two codepoint octets.
                        encoded_byte_array.append(hbyte)
                        encoded_byte_array.append(lbyte)

        return encoded_byte_array


class SCSUDecoder(SCSU):

    def __init__(self):

        # TODO: Write a decoder!
        raise NotImplementedError('No SCSU decoder has been written yet.')
