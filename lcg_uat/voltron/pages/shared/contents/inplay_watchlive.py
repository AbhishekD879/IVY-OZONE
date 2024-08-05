import tests
from voltron.pages.shared.components.home_page_components.home_page_inplay_tab import HomeInPlayTabContent, \
    LiveNowHomePageInPlayAccordionList, InPlaySportGroupHomePage
from collections import OrderedDict


class LiveNowInPlayAccordionList(LiveNowHomePageInPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.liveStream"]/*[@data-crlat="accordion"]'
    _list_item_type = InPlaySportGroupHomePage


class LadbrokesLiveNowInPlayAccordionList(LiveNowInPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.liveStream"]'


class UpcomingInPlayAccordionList(LiveNowInPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.upcomingLiveStream"]/*[@data-crlat="accordion"]'


class LadbrokesUpcomingInPlayAccordionList(UpcomingInPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.upcomingLiveStream"]'


class InPlayWatchLiveTabContent(HomeInPlayTabContent):
    _item = 'xpath=.//*[@data-crlat="accordionsList"]'
    _live_now_counter_number = 'xpath=.//*[@data-crlat="inplay.liveStream"]/following-sibling::*[@data-crlat="inplayCountLabel"]'
    _upcoming_counter_number = 'xpath=.//*[@data-crlat="inplay.upcomingLiveStream"]/following-sibling::*[@data-crlat="inplayCountLabel"]'
    _live_now_type = LiveNowInPlayAccordionList if tests.settings.brand == 'bma' else LadbrokesLiveNowInPlayAccordionList
    _upcoming_type = UpcomingInPlayAccordionList if tests.settings.brand == 'bma' else LadbrokesUpcomingInPlayAccordionList

    @property
    def live_now(self):
        return self._live_now_type(web_element=self._we, selector=self._selector)

    @property
    def upcoming(self):
        return self._upcoming_type(web_element=self._we, selector=self._selector)
