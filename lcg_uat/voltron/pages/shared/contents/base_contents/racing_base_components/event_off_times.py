from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class EventOffTime(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="raceGrid.raceTime"]'
    _tab = 'xpath=.//*[@data-crlat="tab"]'
    _icon = 'xpath=.//*[@data-crlat="raceIcon"]'
    _promotion_icons = 'xpath=.//*[@data-crlat="promotionIcons"]'
    _is_resulted = 'xpath=.//*[@data-crlat="raceGrid.iconRace"] | .//*[@data-crlat="raceIcon"]'  # mobile | desktop
    _is_live = 'xpath=.//*[@class="live"]'
    _is_race_off = 'xpath=.//*[@data-crlat="race-off"]'
    _resulted = 'xpath=.//*[@data-crlat="resulted"]'

    @property
    def event_resulted(self):
        return self._find_element_by_selector(selector=self._resulted, context=self._we)

    @property
    def promotion_icons(self):
        # see comment on BMA-40659
        raise VoltronException('No Promo Icons on Race Event Off time')

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, timeout=2)

    def race_name(self):
        return self._find_element_by_selector(selector=self._name, timeout=0.5, context=self._we)

    def race_off_element(self, timeout=0.5):
        return self._find_element_by_selector(selector=self._is_race_off, timeout=timeout, context=self._we)

    @property
    def is_resulted(self):
        is_resulted = self._find_element_by_selector(selector=self._is_resulted, timeout=0.5, context=self._we) is not None
        return is_resulted

    def is_race_off(self, timeout=0.5):
        return self._find_element_by_selector(selector=self._is_race_off, timeout=timeout, context=self._we) is not None

    @property
    def race_off(self):
        return ComponentBase(selector=self._is_race_off, timeout=2)

    @property
    def result(self):
        return ComponentBase(selector=self._resulted, timeout=2)

    def is_race_on(self, timeout=0.5, expected_result=True):
        return wait_for_result(lambda: 'race-on' in self.get_attribute('class'),
                               expected_result=expected_result,
                               timeout=timeout,
                               name='"race-on" to be shown in @class')

    @property
    def is_live(self):
        return self._find_element_by_selector(selector=self._is_live, timeout=0.5, context=self._we) is not None

    @property
    def icon(self):
        return self._find_element_by_selector(selector=self._icon, timeout=0.5, context=self._we)

    @property
    def is_priced(self):
        return wait_for_result(
            lambda: any(('text-bold' in self.get_attribute('class'), 'text-bold' in self._find_element_by_selector(selector=self._name, timeout=0).get_attribute('class'))),
            name='Event is priced',
            timeout=2)


class EventOffTimesList(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="raceGrid.event"]'
    _list_item_type = EventOffTime
    _selected_item = 'xpath=.//*[@data-crlat="raceGrid.event" and contains(@class, "active")]'

    def select_off_time(self, off_time):
        self.scroll_to_we()
        items_dict = self.items_as_ordered_dict
        if off_time not in items_dict.keys():
            raise VoltronException('Off time "%s" is not available, one of ["%s"] expected'
                                   % (off_time, '", "'.join(items_dict.keys())))
        if off_time == self.selected_item:
            self._logger.warning('*** Bypassing clicking on off time "%s" as it is already active' % off_time)
            return
        items_dict[off_time].click()
        return wait_for_result(lambda: items_dict[off_time] == self.selected_item,
                               name='"%s" to be active' % off_time,
                               bypass_exceptions=(NoSuchElementException, StaleElementReferenceException,
                                                  VoltronException),
                               timeout=1)

    @property
    def selected_item(self):
        return wait_for_result(lambda: self._list_item_type(selector=self._selected_item).name,
                               name='Event off time string',
                               bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                               timeout=3)

    def get_first_available_event(self) -> str:
        """
        This method returns name of first available event, skipping events that are resulted/live
        :return: Event name
        """
        items = self.items_as_ordered_dict
        if not items:
            raise VoltronException(f'Event list is empty for component {self.__class__.__name__}')

        result = ''
        for name, item in items.items():
            if not item.is_live and item.is_race_on():
                result = name
                break
        if not result:
            all_is_resulted = all((item.is_resulted for name, item in items.items()))
            if all_is_resulted:
                # if all events are resulted, disabling verification, as for different races
                # different events will be chosen so cannot calculate first available events
                return self.selected_item
            else:
                result = list(items.keys())[0]
                self._logger.warning(f'Cannot detect first available event, returning "{result}"')
        return result
