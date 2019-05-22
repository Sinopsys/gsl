"""
    gsl -- Goodsteel ledger. A program for building an own distributed ledger

    Copyright (C) 2019  Kirill Kupriyanov

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
"""
    Utils, function and classes for output
"""


class ASCIIColors:
    """
        Class container for save ASCII
    """
    ENDS = '\033[0m'
    LIGHT_CYAN = '\033[96m'
    YELLOW = '\033[33m'
    WHITE = '\033[97m'
    BACK_LIGHT_BLUE = '\033[104m'
    BACK_BLUE = '\033[44m'
    INVERTED = '\033[7m'


class NestedPrint:
    """
        Console nested outputter
    """

    def printf(self, output, space):
        """
            Wrapper function for output all passed param
        :param output:
        :param space: int
        :return:
        """
        if isinstance(output, dict):
            self.pdict(output, space)
        elif isinstance(output, list):
            self.plist(output, space)
        else:
            print('{0}{1}- {2}{3}'.format(
                ''.rjust(space, ' '),
                ASCIIColors.INVERTED,
                output,
                ASCIIColors.ENDS
            ))

    def pdict(self, output, space):
        for key, val in output.items():
            print('{0}{1}{2}:{3}'.format(
                ''.rjust(space, ' '),
                ASCIIColors.LIGHT_CYAN,
                key,
                ASCIIColors.INVERTED
            ))
            self.printf(val, space=(space + 4))

    def plist(self, output, space):
        for item in output:
            if isinstance(item, dict):
                self.pdict(item, space=(space + 4))
            else:
                print(
                    '{0}{1}- {2}{3}'.format(
                        ''.rjust(space, ' '),
                        ASCIIColors.INVERTED,
                        item,
                        ASCIIColors.ENDS
                    )
                )


print_nested = NestedPrint().printf

