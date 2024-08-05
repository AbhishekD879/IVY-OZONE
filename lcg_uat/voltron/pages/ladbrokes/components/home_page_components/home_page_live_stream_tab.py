from voltron.pages.shared.components.home_page_components.home_page_live_stream_tab \
    import LiveNowHomePageLiveStreamAccordionList, LiveStreamTabContent


class LadbrokesLiveNowHomePageLiveStreamAccordionList(LiveNowHomePageLiveStreamAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.liveStream"]'


class LadbrokesLiveStreamTabContent(LiveStreamTabContent):

    @property
    def live_now(self):
        return LadbrokesLiveNowHomePageLiveStreamAccordionList(web_element=self._we)
