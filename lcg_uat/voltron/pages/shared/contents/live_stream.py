import re

from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.sport_base import SportPageBase
from voltron.pages.shared.contents.inplay_watchlive_desktop import InPlayWatchLiveDesktopTabContent
from voltron.pages.shared.contents.inplay_watchlive import InPlayWatchLiveTabContent


class LiveStreamButton(ButtonBase):
    _events_count = 'xpath=.//*[@data-crlat="switcher.eventCount"]'

    @property
    def name(self):
        raw_text = self._get_webelement_text(we=self._we, timeout=0.5)
        search = re.search('[aA-zZ\s]+', raw_text)
        result = search.group().strip() if search and search.group() else raw_text
        return result

    @property
    def event_count(self):
        raw_text = self._get_webelement_text(selector=self._events_count, timeout=1)
        res = raw_text.strip('(').strip(')') if raw_text else ""
        return res


class LiveStreamGroupingSelectionButtons(GroupingSelectionButtons):
    _list_item_type = LiveStreamButton


class LiveStream(SportPageBase, InPlayWatchLiveDesktopTabContent, InPlayWatchLiveTabContent):
    _url_pattern = r'^https?:\/\/.+\/live-stream'
    _tabs_menu = 'xpath=.//*[@data-crlat="switchers" and *[contains(@class, "switch-btn")]]'
    _tabs_menu_type = LiveStreamGroupingSelectionButtons
    _live_now_text = 'xpath=.//span[contains(text(),"Live Now")]'
    _upcoming_text = 'xpath=.//span[contains(text(),"Upcoming Events")]'

    @property
    def tabs_menu(self):
        return self._tabs_menu_type(selector=self._tabs_menu, context=self._we, timeout=5)

    @property
    def sport_menu(self):
        return self.home.menu_carousel

    @property
    def live_now_tab(self):
        return self._find_element_by_selector(selector=self._live_now_text, timeout=5)

    @property
    def upcoming_tab(self):
        return self._find_element_by_selector(selector=self._upcoming_text, timeout=5)


class DesktopLiveStream(LiveStream):
    _tab_content_type = InPlayWatchLiveDesktopTabContent
