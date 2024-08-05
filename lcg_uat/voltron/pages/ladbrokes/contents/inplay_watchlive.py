from voltron.pages.shared.components.home_page_components.home_page_inplay_tab import HomeInPlayTabContent, \
    LiveNowHomePageInPlayAccordionList, InPlaySportGroupHomePage


class LiveNowInPlayAccordionListLadbrokes(LiveNowHomePageInPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.liveStream"]'
    _list_item_type = InPlaySportGroupHomePage


class UpcomingInPlayAccordionList(LiveNowInPlayAccordionListLadbrokes):
    _item = 'xpath=.//*[@data-crlat="accordion.upcomingLiveStream"]'


class InPlayWatchLiveTabContentLadbrokes(HomeInPlayTabContent):
    _item = 'xpath=.//*[@data-crlat="accordionsList"]'
    _live_now_counter_number = 'xpath=.//*[@data-crlat="inplay.liveStream"]/following-sibling::*[@data-crlat="inplayCountLabel"]'
    _upcoming_counter_number = 'xpath=.//*[@data-crlat="inplay.upcomingLiveStream"]/following-sibling::*[@data-crlat="inplayCountLabel"]'

    @property
    def live_now(self):
        return LiveNowInPlayAccordionListLadbrokes(web_element=self._we, selector=self._selector)

    @property
    def upcoming(self):
        return UpcomingInPlayAccordionList(web_element=self._we, selector=self._selector)
