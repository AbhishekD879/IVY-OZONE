from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.menus.right_menu import RightMenuItem
from voltron.utils.waiters import wait_for_result


class AllSportsSectionItem(Accordion):
    _item_name = 'xpath=.//*[@data-crlat="title"]'
    _item_icon = 'xpath=.//*[@data-crlat="icon"]'

    @property
    def name(self):
        return self.item_name

    @property
    def item_name(self):
        return self._get_webelement_text(selector=self._item_name, context=self._we, timeout=1)

    @property
    def item_icon(self):
        self.scroll_to_we()
        return ButtonBase(selector=self._item_icon, context=self._we)


class AllSportsSection(Accordion):
    _item = 'xpath=.//*[@data-crlat="menu.listItem"]/*[@data-crlat="link"]'
    _list_item_type = AllSportsSectionItem


class AllSports(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/az-sports'
    _a_z_sports_page_container = 'xpath=.//*[@data-crlat="az-sports"]'
    _top_sports_page_container = 'xpath=.//*[@data-crlat="top-sports"]'
    _connect_page_container = 'xpath=.//retail-menu//section[@data-crlat="pageContainer"]'
    _item = 'xpath=.//*[@data-crlat="menu.listItem"]'
    _list_item_type = RightMenuItem

    def _wait_active(self, timeout=0):
        wait_for_result(
            lambda: self._find_element_by_selector(selector=self._item, context=self._context, timeout=0),
            name='AZSports - AZSportsSection Items to load',
            timeout=3)

    @property
    def a_z_sports_section(self):
        return AZSportsSection(selector=self._a_z_sports_page_container, context=self._we)

    @property
    def top_sports_section(self):
        return TopSportsSection(selector=self._top_sports_page_container, context=self._we)

    @property
    def connect_section(self):
        return ConnectSection(selector=self._connect_page_container, context=self._we)


class AZSportsSection(AllSportsSection):
    pass


class TopSportsSection(AllSportsSection):
    pass


class ConnectSection(AllSportsSection):
    pass
