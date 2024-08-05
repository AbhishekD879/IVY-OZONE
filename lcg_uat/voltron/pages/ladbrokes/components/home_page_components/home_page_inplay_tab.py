from voltron.pages.shared.components.home_page_components.home_page_inplay_tab import HomeInPlayTabContent, \
    LiveNowHomePageInPlayAccordionList, UpcomingHomePageInPlayAccordionList


class LadbrokesLiveNowHomePageInPlayAccordionList(LiveNowHomePageInPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.livenow"]'


class LadbrokesUpcomingHomePageInPlayAccordionList(UpcomingHomePageInPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.upcoming"]'


class LadbrokesHomeInPlayTabContent(HomeInPlayTabContent):

    @property
    def live_now(self):
        return LadbrokesLiveNowHomePageInPlayAccordionList(web_element=self._we, selector=self._selector)

    @property
    def upcoming(self):
        return LadbrokesUpcomingHomePageInPlayAccordionList(web_element=self._we, selector=self._selector)
