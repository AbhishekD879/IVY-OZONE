from voltron.pages.shared.components.home_page_components.desktop.base_desktop_module import BaseDesktopModule
from voltron.pages.shared.components.home_page_components.home_page_desktop_next_races import \
    HomePageDesktopNextRacesModuleContent
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroupHeader
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.utils.waiters import wait_for_result


class Next4GroupHeader(EventGroupHeader):
    _chevron_arrow = 'xpath=.//*[@data-crlat="chevronArrow"]'

    @property
    def chevron_arrow(self):
        return self._find_element_by_selector(selector=self._chevron_arrow, timeout=1)

    def has_chevron_arrow(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._chevron_arrow,
                                                   timeout=0) is not None,
            name=f'Checkbox area status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class NextRaceModule(BaseDesktopModule):
    _content = 'xpath=.//*[@data-crlat="tab.showNextRacesModule"]'
    _content_type = HomePageDesktopNextRacesModuleContent
    _header_type = Next4GroupHeader
    _expanded_criteria = 'xpath=.//*[@data-crlat="accordion"]'
    _view_all_horse_racing_events = 'xpath=.//a[@data-crlat="showMore"]/span'

    def is_expanded(self, timeout=0.6, expected_result=True):
        section = self._find_element_by_selector(selector=self._expanded_criteria, timeout=timeout)
        if section:
            result = wait_for_result(lambda: 'is-expanded' in section.get_attribute('class'),
                                     name=f'Accordion expand status to be "{expected_result}"',
                                     expected_result=expected_result,
                                     timeout=timeout)
            self._logger.debug(f'*** Accordion expanded status is {result}')
            return result
        return False

    @property
    def view_all_horse_racing_events(self):
        return self._find_element_by_selector(selector=self._view_all_horse_racing_events)

    @property
    def group_header(self):
        header = self._header_type(self._header, context=self._we, timeout=2)
        header.scroll_to()
        return header

    @property
    def tab_content(self) -> TabContent:
        return self._content_type(selector=self._content)
