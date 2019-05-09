def get_version() -> str:
    """
    Get package version
    :return: str
    """
    with open('../VERSION', 'r') as __fd__:
        return __fd__.read_lines()

