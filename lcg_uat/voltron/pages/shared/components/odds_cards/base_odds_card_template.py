from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from collections import OrderedDict

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.utils.waiters import wait_for_result


class BaseOddsCardTemplate(ComponentBase, metaclass=ABCMeta):
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'
    _item = _bet_button
    _list_item_type = BetButton
    _event_day = 'xpath=.//*[@data-crlat="eventDay"]'
    _whole_event_name = 'xpath=.//*[@data-crlat="oddsNames"]'
    # the order in [] is important here, on sport page event time is in .//*[@data-crlat="oddsCardLabel"],
    #  but on in-play additional span is added .//*[@data-crlat="liveClock"] so we should look for liveClock first
    _event_time = 'xpath=.//*[@data-crlat="liveClock" or @data-crlat="oddsCardLabel"]'
    _favourite_icon = 'xpath=.//*[@data-crlat="addFavouritesButton"]//*[local-name() = "svg"]'
    _live_now_label = 'xpath=.//*[@data-crlat="oddsLive" or @data-crlat="liveLabel"]'
    _stream_link = 'xpath=.//*[@data-crlat="watchLive"] | .//span[contains(text(),"Watch")]'
    _stream_icon = 'xpath=.//*[@data-crlat="streamIcon" or @data-crlat="oddsIconStream"]'

    @property
    def event_id(self) -> str:
        return self.get_attribute('data-eventid')

    @property
    def event_date(self) -> str:
        return self._get_webelement_text(self._event_day, timeout=0.5)

    @abstractproperty
    def event_name(self) -> str:
        """
        Method used to return event name for particular Odds Card
        """

    @property
    def name(self):
        return self.event_name

    def is_event_name_truncated(self) -> bool:
        """
        Verifies if in case of long event name it's truncated like this: 'long event nam...'
        """
        return self.is_truncated(selector=self._whole_event_name)

    @property
    def event_time(self) -> str:
        times_we = self._find_elements_by_selector(self._event_time, timeout=2)
        time_we = next((time_we for time_we in times_we if time_we.is_displayed()), None)
        if time_we:
            return self._get_webelement_text(we=time_we)
        else:
            return ''

    @abstractmethod
    def get_available_prices(self) -> OrderedDict:
        """
        """

    @abstractmethod
    def get_active_prices(self) -> OrderedDict:
        """
        Method used to get active prices on current Odds Card
        """

    @abstractmethod
    def get_all_prices(self) -> OrderedDict:
        """
        Method used to get active prices on current Odds Card
        """

    @abstractmethod
    def get_selected_output_prices(self) -> OrderedDict:
        """
        Method used to get active prices on current Odds Card
        """

    @abstractmethod
    def get_markets_count(self) -> int:
        """
        Method used to get number of markets on current Odds Card
        """

    @property
    def favourite_icon(self):
        return ButtonBase(selector=self._favourite_icon, context=self._we)

    def has_favourite_icon(self, expected_result=True, timeout=1) -> bool:
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._favourite_icon, timeout=0) is not None,
            expected_result=expected_result,
            timeout=timeout,
            name=f'Icon presence status to be "{expected_result}"')

    @property
    def is_live_now_event(self) -> bool:
        live_now_label = self._find_element_by_selector(selector=self._live_now_label, timeout=0)
        if live_now_label and 'ng-hide' not in live_now_label.get_attribute('class').strip(' ').split(' '):
            return True
        return False

    def has_stream(self, expected_result=True, timeout=1) -> bool:
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._stream_link, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Stream presence status to be "{expected_result}"')

    @property
    def watch_live_label(self):
        return self._get_webelement_text(self._stream_link, timeout=0.5)

    def has_stream_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._stream_icon, context=self._we) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Stream icon status to be "{expected_result}"')
