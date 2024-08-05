from voltron.pages.coral.menus.other_menus import ExternalPageComponentWrapper, CoralMenuItem, CoralMenus
from voltron.pages.ladbrokes.components.header import GlobalHeaderLadbrokes
from voltron.pages.shared.components.content_header import HeaderLine


class CustomLadbrokesHeader(GlobalHeaderLadbrokes, HeaderLine):
    pass


class ExternalPageComponentWrapperLadbrokes(ExternalPageComponentWrapper):
    _header_line = 'xpath=.//vn-app'
    _header_line_type = CustomLadbrokesHeader


class LadbrokesMenuItem(CoralMenuItem):
    _header_type = ExternalPageComponentWrapperLadbrokes


class LadbrokesMenus(CoralMenus):
    _list_item_type = LadbrokesMenuItem
