from voltron.pages.shared.components.base import ComponentBase


class InternationalToteEvent(ComponentBase):
    _event_time = 'xpath=.//*[@data-crlat="eventTime" or @data-crlat="raceGrid.raceTime"]'
    _event_name = 'xpath=.//*[@data-crlat="eventName" or @data-crlat="raceGrid.raceName"]'

    @property
    def is_resulted(self):
        return self.get_attribute('class') == 'race-resulted'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._event_name, context=self._we)

    @property
    def event_time(self):
        return self._get_webelement_text(selector=self._event_time, context=self._we)


class ToteEventsCarousel(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="toteEvent" or @data-crlat="raceGrid.event"]'
    _header = 'xpath=.//*[@data-crlat="carouselHeader" or @data-crlat="headerTitle.leftMessage"]'
    _list_item_type = InternationalToteEvent
    _meeting_name = 'xpath=.//*[@data-crlat="raceGrid.meeting.name"]'

    @property
    def header(self):
        return self._get_webelement_text(selector=self._header, context=self._we)

    @property
    def meeting_name(self):
        return self._get_webelement_text(selector=self._meeting_name, context=self._we)
