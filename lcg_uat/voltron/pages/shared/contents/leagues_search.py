from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.base_content import BaseContent


class LeagueName(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class LeaguesAccordionsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="listItemLink"]'
    _list_item_type = LeagueName


class LeagueTabContent(TabContent):
    _accordions_list_type = LeaguesAccordionsList


class LeagueSearch(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/search-leagues'
    _tab_content_type = LeagueTabContent

    def _wait_active(self, timeout=15):
        try:
            self._find_element_by_selector(selector=self._tab_content, context=self._context,
                                           bypass_exceptions=(NoSuchElementException, ), timeout=3)

        except StaleElementReferenceException:
            self._logger.debug('*** Overriding StaleElementReferenceException in %s' % self.__class__.__name__)
