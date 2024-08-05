from collections import OrderedDict

from voltron.pages.shared.components.home_page_components.home_page_inplay_tab import \
    LiveNowHomePageInPlayAccordionList, UpcomingHomePageInPlayAccordionList
from voltron.pages.shared.contents.inplay import InPlayTabContent


class LiveNowHomePageLiveStreamAccordionList(LiveNowHomePageInPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.liveStream"]//*[@data-crlat="accordion"]'


class UpcomingHomePageLiveStreamAccordionList(UpcomingHomePageInPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion.upcomingLiveStream"]'


class LiveStreamTabContent(InPlayTabContent):
    _in_play_header = 'xpath=.//*[@data-crlat="inPlayHeader"]//*[contains(@data-crlat,"inplay.live") or contains(@data-crlat,"inplay.upcoming")]'

    @property
    def accordions_list(self) -> OrderedDict:
        raise NotImplementedError('Please use live_now and upcoming properties instead of accordions_list')

    @property
    def live_now(self):
        return LiveNowHomePageLiveStreamAccordionList(web_element=self._we)

    @property
    def upcoming(self):
        return UpcomingHomePageLiveStreamAccordionList(web_element=self._we)
