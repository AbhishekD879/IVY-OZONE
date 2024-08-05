from voltron.environments.constants.base.regex import Regex


class LadbrokesRegex(Regex):
    """
    For storing regex variables
    """
    EXPECTED_EACH_WAY_FORMAT_FEATURED = r'^Each Way:\s?([\d/]*)\sodds\s-\splaces\s([\d,]*)$'  # Using on featured module/tab
