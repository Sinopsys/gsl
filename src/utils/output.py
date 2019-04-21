"""
    Utils, function and classes for output
"""


class ASCIIColors:
    """
        Class container for save ASCII
    """
    ENDS = "\033[0m"
    LIGHT_CYAN = "\033[96m"
    YELLOW = "\033[33m"
    WHITE = "\033[97m"


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
                ASCIIColors.WHITE,
                output,
                ASCIIColors.ENDS
            ))

    def pdict(self, output, space):
        for key, val in output.items():
            print('{0}{1}{2}:{3}'.format(
                ''.rjust(space, ' '),
                ASCIIColors.LIGHT_CYAN,
                key,
                ASCIIColors.WHITE
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
                        ASCIIColors.WHITE,
                        item,
                        ASCIIColors.ENDS
                    )
                )


print_nested = NestedPrint().printf

