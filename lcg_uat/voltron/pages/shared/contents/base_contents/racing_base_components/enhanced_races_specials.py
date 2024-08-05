from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import RacingBetButton
from voltron.pages.shared.contents.base_contents.racing_base_components.enhanced_races_event import EnhancedRaces, \
    EnhancedRacesEvent


class RacesSpecialsEvent(EnhancedRacesEvent):
    _name = 'xpath=.//*[@data-crlat="raceCard.outcomeName"]'
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=2)

    @property
    def bet_button(self):
        return RacingBetButton(selector=self._bet_button, context=self._we)


class RacesSpecials(EnhancedRaces):
    _list_item_type = RacesSpecialsEvent
