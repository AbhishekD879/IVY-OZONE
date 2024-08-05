from voltron.pages.shared.contents.base_contents.racing_base_components.enhanced_races_event import EnhancedRaces, \
    EnhancedRacesEvent
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase


class RaceGridEvent(ComponentBase):
    _race_time = 'xpath=.//*[@data-crlat="raceGrid.raceTime"]'
    _race_name = 'xpath=.//*[@data-crlat="raceGrid.raceName"]'

    @property
    def race_time(self):
        return self._get_webelement_text(selector=self._race_time, timeout=2)

    @property
    def race_name(self):
        return self._get_webelement_text(selector=self._race_name, timeout=2)

    @property
    def name(self):
        return f'{self.race_time} {self.race_name}'


class OffersAndFeaturedRacesModule(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="raceGrid.event"]'
    _list_item_type = RaceGridEvent
    _itv_icon = 'xpath=.//*[@data-crlat="promotionIcon.ITV"]'
    _extra_place_races_icon = 'xpath=.//*[@data-crlat="promotionIcon.EPR"]'
    _header = 'xpath=.//*[@data-crlat="raceGrid.meeting.name"]'

    def has_itv_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._itv_icon, timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Icon status to be {expected_result}')

    def has_extra_place_races_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._extra_place_races_icon, timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Icon status to be {expected_result}')

    @property
    def header_name(self):
        return TextBase(selector=self._header, context=self._we)


class EnhancedRacesEventLadbrokes(EnhancedRacesEvent):
    _card_name = 'xpath=.//ancestor::*[@data-crlat="race.enhancedRacesCarousel"]//*[@data-crlat="raceGrid.meeting.name"]'

    @property
    def name(self):
        return self._get_webelement_text(we=self._we).replace('\n', ' ')

    @property
    def event_name(self):
        return f'{self.card_name} - {self.name}'


class LadbrokesEnhancedRaces(EnhancedRaces):
    _item = 'xpath=.//*[@data-crlat="raceGrid.event"]'
    _list_item_type = EnhancedRacesEventLadbrokes
    _card_name = 'xpath=.//*[@data-crlat="raceCard.title"]'
    _extra_place_module = 'xpath=.//*[@data-crlat="Extra Place Offers"]'

    @property
    def extra_place_offer_module(self):
        return OffersAndFeaturedRacesModule(selector=self._extra_place_module, context=self._we)

    @property
    def itv_module(self):
        return OffersAndFeaturedRacesModule(selector=self._itv_module, context=self._we)
