from voltron.pages.shared.components.home_page_components.home_page_inplay_tab import InPlayEventGroupHomePage, \
    InPlaySportGroupHomePage
from voltron.pages.shared.contents.inplay import InPlayAccordionList
from voltron.pages.shared.contents.inplay_desktop import InPlayDesktopTabContent
from voltron.utils.waiters import wait_for_result


class WatchLiveEventGroupInPlayPageDesktop(InPlayEventGroupHomePage):
    _header = 'xpath=.//*[@data-crlat="containerHeader"]'


class WatchLiveSportGroupInPlayPage(InPlaySportGroupHomePage):
    _item = 'xpath=.//*[@data-crlat="accordion"][*]'
    _list_item_type = WatchLiveEventGroupInPlayPageDesktop
    _show_more = 'xpath=.//*[@data-crlat="showMore"]'

    @property
    def view_all_in_play_sport_events_button(self):
        return self._find_element_by_selector(selector=self._show_more, timeout=1)

    def has_view_all_in_play_sport_events_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._show_more, timeout=1) is not None,
            name=f'view all <Sport Name> in play events button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class InPlayWatchLiveAccordionList(InPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordionsList"]/*[@data-crlat="accordion"]'
    _list_item_type = WatchLiveSportGroupInPlayPage


class InPlayWatchLiveDesktopTabContent(InPlayDesktopTabContent):
    _accordions_list = 'xpath=.//*[@data-crlat="tab.showWatchLiveContent"]'
    _accordions_list_type = InPlayWatchLiveAccordionList
