from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.pages.shared.components.home_page_components.desktop.base_desktop_module import BaseDesktopModule
from voltron.pages.shared.components.menu_carousel import MenuCarousel
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.utils.waiters import wait_for_result


class MenuCarouselDesktop(MenuCarousel):
    _item = 'xpath=.//*[@data-crlat="menu.item"]'


class InPlayLiveStreamModuleTabContent(TabContent):
    _show_more = 'xpath=.//*[@data-crlat="showMore"]'

    def has_view_all_in_play_sport_events_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._show_more, timeout=0) is not None,
                               name=f'"View All IN-PLAY <sport_name>" button in "{self.__class__.__name__}" shown status to be "{expected_result}"',
                               timeout=timeout,
                               expected_result=expected_result)

    @property
    def view_all_in_play_sport_events_button(self):
        return ButtonBase(selector=self._show_more, context=self._we)


class InPlayLiveStreamModule(BaseDesktopModule):
    _menu_carousel = 'xpath=.//*[@data-uat="mainNav"]'
    _tabs_menu = 'xpath=.//*[@data-crlat="switchers" and *[contains(@class, "switch-btn")]]'
    _tabs_menu_type = GroupingSelectionButtons
    _content = 'tag=in-play-sport-tab'
    _content_type = InPlayLiveStreamModuleTabContent
    _show_more = 'xpath=.//*[@data-crlat="showMore"]'
    _no_events_label = 'xpath=.//*[@data-crlat="noEventsFound"]'

    @property
    def tabs_menu(self):
        return self._tabs_menu_type(selector=self._tabs_menu, context=self._we, timeout=5)

    @property
    def menu_carousel(self):
        return MenuCarouselDesktop(selector=self._menu_carousel, context=self._we)

    @property
    def view_all_live_stream_sport_events_button(self):
        return ButtonBase(selector=self._show_more, context=self._we)

    def has_no_events_label(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._no_events_label, timeout=0) is not None,
                               name=f'{self.__class__.__name__} "No events" label status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)


