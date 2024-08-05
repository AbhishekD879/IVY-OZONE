from voltron.pages.shared.components.in_play_module import InPlayModuleEventGroup, InplayHeader, UpcomingHeader
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.sport_list_item import SportEventListItem
from voltron.pages.shared.contents.inplay import InPlayAccordionList, InPlayTabContent
from voltron.utils.waiters import wait_for_result


class InPlayEventGroupHomePage(InPlayModuleEventGroup,SportEventListItem):
    _watch_live_icon = 'xpath=.//*[@data-crlat="watchLive"]'

    @property
    def event_name(self):
        self.scroll_to()
        return self.name

    def has_watch_live_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._watch_live_icon, timeout=0),
                               name=f'"Watch Live" icon in "{self.__class__.__name__}" shown status to be "{expected_result}"',
                               timeout=timeout,
                               expected_result=expected_result)


class InPlaySportGroupHomePage(EventGroup):
    _item = 'xpath=.//*[@data-crlat="accordion"][*]'
    _list_item_type = InPlayEventGroupHomePage
    _show_more_leagues_button = 'xpath=.//*[@data-crlat="showMoreLeagues"]'

    def has_show_more_leagues_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._show_more_leagues_button, timeout=0) is not None,
                               name=f'"Show More Leagues" button in "{self.__class__.__name__}" shown status to be "{expected_result}"',
                               timeout=timeout,
                               expected_result=expected_result)

    @property
    def show_more_leagues_button(self):
        return ButtonBase(selector=self._show_more_leagues_button, context=self._we)

    @property
    def event_name(self):
        self.scroll_to()
        return self.name


class LiveNowHomePageInPlayAccordionList(EventGroup, InPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.livenow"]/*[@data-crlat="accordion"]'
    _list_item_type = InPlaySportGroupHomePage
    _in_play_header = 'xpath=.//*[@data-crlat="inPlayHeader"]'
    _upcoming_header = 'xpath=.//*[contains(@class, "upcoming-header")]'

    @property
    def live_now_header(self):
        return InplayHeader(selector=self._in_play_header, context=self._we, timeout=1)

    @property
    def upcoming_header(self):
        return UpcomingHeader(selector=self._upcoming_header, context=self._we, timeout=2)


class UpcomingHomePageInPlayAccordionList(LiveNowHomePageInPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.upcoming"]/*[@data-crlat="accordion"]'


class HomeInPlayTabContent(InPlayTabContent):

    @property
    def live_now(self):
        return LiveNowHomePageInPlayAccordionList(web_element=self._we, selector=self._selector)

    @property
    def upcoming(self):
        return UpcomingHomePageInPlayAccordionList(web_element=self._we, selector=self._selector)
