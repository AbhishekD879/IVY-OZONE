from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.coral.menus.other_menus import ExternalPageComponentWrapper, CoralMenus, CoralMenuItem


class ExternalPageComponentWrapperDesktop(ExternalPageComponentWrapper):
    _transactions_left_nav_menu = 'xpath=.//div[contains(@class, "nav-left")]'
    _details_top_nav_menu = 'xpath=.//nav[contains(@class, "navbar navbar-expand-sm")]'

    @property
    def transactions_left_nav_menu(self):
        return TransactionsLeftNavMenu(selector=self._transactions_left_nav_menu, timeout=20)

    @property
    def details_top_nav_menu(self):
        return DetailsTopNavMenu(selector=self._details_top_nav_menu, timeout=20)


class TransactionsLeftNavMenu(ComponentBase):
    _item = 'xpath=.//a[contains(@class, "nav-link")]'
    _active_link = 'xpath=.//a[contains(@class, "active")]'
    _list_item_type = LinkBase

    @property
    def active_link(self):
        return LinkBase(selector=self._active_link, context=self._we)


class DetailsTopNavMenu(ComponentBase):
    _item = 'xpath=.//a[contains(@class, "tab-nav-link")]'
    _active_link = 'xpath=.//li[contains(@class, "active")]/a'
    _list_item_type = LinkBase

    @property
    def active_link(self):
        return LinkBase(selector=self._active_link, context=self._we)


class CoralMenuItemDesktop(CoralMenuItem):
    _header_type = ExternalPageComponentWrapperDesktop

    @property
    def get_header(self):
        # Return header of the outer page
        return self._header_type()


class CoralMenusDesktop(CoralMenus):
    _list_item_type = CoralMenuItemDesktop
