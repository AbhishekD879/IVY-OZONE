from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.racing_base_components.each_way_terms import EachWayTermsEnhanced
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec


class EnhancedRacesEvent(ComponentBase):
    _card_name = 'xpath=.//*[@data-crlat="raceCard.title"]'
    _name = 'xpath=.//*[@data-crlat="raceCard.eventName"]'
    _countdown_container = 'xpath=.//*[@data-crlat="raceCountdown"]'
    _ew_container = 'xpath=.//*[@data-crlat="terms" or @data-crlat="eachWayContainer"]'
    _next_arrow = 'xpath=.//*[@data-crlat="nextArrow"]'

    def has_next_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._next_arrow, timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Icon status to be {expected_result}')

    @property
    def card_name(self):
        return self._find_element_by_selector(selector=self._card_name, timeout=2).get_attribute('innerHTML').strip()

    @property
    def name(self):
        return self._find_element_by_selector(selector=self._name, timeout=2).get_attribute('innerHTML').strip()

    @property
    def event_name(self):
        return f'{self.card_name.upper()} - {self.name}'

    @property
    def has_countdown_timer(self):
        timer = self._find_element_by_selector(selector=self._countdown_container, timeout=1)
        return self.countdown_timer.is_displayed() if timer else False

    @property
    def countdown_timer(self):
        return TextBase(selector=self._countdown_container, context=self._we)

    def has_each_way_terms(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._ew_container, timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Each way terms status to be {expected_result}')

    @property
    def each_way_terms(self):
        return EachWayTermsEnhanced(selector=self._ew_container, context=self._we)


class EnhancedRacesModule(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="raceCard.event"]'
    _list_item_type = EnhancedRacesEvent


class EnhancedRaces(EventGroup):
    _item = 'xpath=.//*[@data-crlat="raceCard.event"]'
    _list_item_type = EnhancedRacesEvent
    _itv_module = 'xpath=.//*[@data-crlat="ITV Races"]'
    _extra_place_module = 'xpath=.//*[@data-crlat="Extra Place Offer"]'

    @property
    def itv_module(self):
        return EnhancedRacesModule(selector=self._itv_module, context=self._we)

    @property
    def extra_place_offer_module(self):
        return EnhancedRacesModule(selector=self._extra_place_module, context=self._we)

    def has_itv_module(self, expected_result=True, timeout=1):
        return self._has_module(selector=self._itv_module, module_name=vec.racing.ITV,
                                timeout=timeout, expected_result=expected_result)

    def has_extra_place_module(self, expected_result=True, timeout=1):
        return self._has_module(selector=self._extra_place_module, module_name=vec.racing.EXTRA_PLACE_TITLE,
                                timeout=timeout, expected_result=expected_result)

    def _has_module(self, selector, module_name, timeout, expected_result=True):
        module_in_dom = wait_for_result(lambda: self._find_element_by_selector(selector=selector, timeout=0),
                                        expected_result=expected_result,
                                        timeout=timeout,
                                        name=f'{module_name} presence status to be {expected_result}')
        if module_in_dom:
            items_we = self._find_elements_by_selector(selector=self._item, context=module_in_dom)
            self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
            return True if len(items_we) >= 1 else False
        else:
            self._logger.error(f'*** Could not find "{module_name}" module')
            return False
