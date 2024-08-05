from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.sports_tab_contents.competitions_tab_content import LeagueName


class CompetitionItem(Accordion):
    _name = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _item = 'xpath=.//*[@data-crlat="linkListItem"]'
    _list_item_type = LeagueName
    _fade_out_overlay = True
    _verify_spinner = True

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=2)


class CompetitionListDropDown(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="accordionComp"]'
    _list_item_type = CompetitionItem
    _fade_out_overlay = True
    _verify_spinner = True

    def _wait_active(self, timeout=2):
        self._we = self._find_myself(timeout=timeout)
        try:
            self._find_element_by_selector(selector=self._item,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=timeout)
        except StaleElementReferenceException:
            self._we = self._find_myself(timeout=timeout)
