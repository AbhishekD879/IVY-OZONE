from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class LeagueSelectorOption(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="dropdown.subMenuTitle"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class LeagueSelector(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="dropdown.subMenuItem"]'
    _list_item_type = LeagueSelectorOption


class CompetionsSelectorOption(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="dropdown.menuTitle"]'
    _sub_menu = 'xpath=.//*[@data-crlat="dropdownSubMenu"]'

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, timeout=3)

    @property
    def league_selector(self):
        return LeagueSelector(selector=self._sub_menu)


class CompetitionSelector(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="dropdown.menuItem"]'
    _list_item_type = CompetionsSelectorOption

    def _wait_active(self, timeout=15):
        self._we = self._find_myself(timeout=timeout)
        wait_for_result(lambda: self._we.size.get('height') > 10 and self._we.size.get('width') > 50,
                        timeout=timeout,
                        name='Competitions menu to appear in expanded size')
        wait_for_result(lambda: len(self._find_elements_by_selector(selector=self._item, timeout=0)) > 0,
                        name='Competitions items to be loaded',
                        timeout=timeout)
