from voltron.pages.shared.components.content_header import HeaderLine
from voltron.utils.exceptions.voltron_exception import VoltronException


class LadbrokesHeaderLine(HeaderLine):
    _back_button = None

    @property
    def back_button(self):
        raise VoltronException('There is no back button in content header')

    @property
    def has_back_button(self):
        raise VoltronException('There is no back button in content header')

    def press_back(self):
        raise VoltronException('There is no back button in content header')
