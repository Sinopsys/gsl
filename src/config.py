"""
    Module for working with config
"""


def load():
    pass


def _read_(path: str) -> str:
    """

    """
    config = {}
    if not os.path.exists(path):
        raise OSError(f'No such file or directory {path}, please check if file\
                exists')

    with open(path, 'r') as __fd__:
        try:
            config = yaml.load(__fd__)
        except yaml.YAMLError as err:
            __logger__.exception(
                f'Error {err.__class__.__name__} occurred when parse yaml\
                parse config file, {err}'
            )
        except Exception as err:
            __logger__.exception(
                f'Unknown error {err.__class__.__name__} occurred when parse\
                yaml parse config file, {err}'
            )

    return config

