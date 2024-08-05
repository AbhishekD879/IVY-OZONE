from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.utils.waiters import wait_for_result

from voltron.pages.shared.contents.base_contents.racing_base_components.event_off_times import EventOffTime
from voltron.pages.shared.contents.base_contents.racing_base_components.event_off_times import EventOffTimesList


class VirtualEventOffTime(EventOffTime):
    _name = 'xpath=.//*[@data-crlat="tab"]'

    @property
    def name(self):
        return self._we.text


class VirtualEventOffTimesList(EventOffTimesList):
    _item = 'xpath=.//*[@data-crlat="tab.tpTabs"]/a'
    _list_item_type = VirtualEventOffTime
    _selected_item = 'xpath=.//*[@data-crlat="tab.tpTabs" and contains(@class, "active")]'


class VirtualChildSportElement(ComponentBase):
    _timer = 'xpath=.//*[@data-crlat="timer"]'
    _name = 'xpath=.//*[@data-crlat="name"]'

    @property
    def timer(self):
        return self._wait_for_not_empty_web_element_text(selector=self._timer, context=self._we, timeout=1)

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, context=self._we, timeout=1)


class VirtualChildSportMenuCarousel(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="menuElement"]'
    _list_item_type = VirtualChildSportElement


class BaseVirtualsTabContent(TabContent):
    """
    Common elements for Sport/Racing Virtuals EDP
    """
    _sport_event_time = 'xpath=.//*[@data-crlat="eventTime"]'
    _sport_event_name = 'xpath=.//*[@data-crlat="eventName"]'
    _sport_event_timer = 'xpath=.//*[@data-crlat="countDownTimer"]//span'
    _stream_window = 'xpath=.//*[@data-crlat="vsVideoStream"]'
    _event_off_times_list = 'xpath=.//*[@data-crlat="panel.tabs"]'
    _event_off_times_list_type = VirtualEventOffTimesList
    _child_sport_carousel = 'xpath=.//*[@data-crlat="childVirtualCarouselMenu"]'
    _child_sport_carousel_type = VirtualChildSportMenuCarousel
    _cta_button = 'xpath=.//*[@data-crlat="buttonSubmit"] | .//*[@data-crlat="addToBetslipButton"]'

    @property
    def event_off_times_list(self):
        return self._event_off_times_list_type(selector=self._event_off_times_list, context=self._we)

    @property
    def sport_event_time(self):
        return TextBase(selector=self._sport_event_time, context=self._we)

    @property
    def sport_event_name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._sport_event_name, context=self._we, timeout=1)

    @property
    def sport_event_timer(self):
        return self._wait_for_not_empty_web_element_text(selector=self._sport_event_timer, context=self._we, timeout=4)

    def has_timer(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._sport_event_timer, timeout=0) and
                               self._find_element_by_selector(selector=self._sport_event_timer, timeout=0).is_displayed(),
                               name=f'{self.__class__.__name__} Timer status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def stream_window(self):
        return ComponentBase(selector=self._stream_window, context=self._we)

    @property
    def child_sport_carousel(self):
        return self._child_sport_carousel_type(selector=self._child_sport_carousel, context=self._we)

    @property
    def cta_button(self):
        return ButtonBase(selector=self._cta_button, context=self._we)
