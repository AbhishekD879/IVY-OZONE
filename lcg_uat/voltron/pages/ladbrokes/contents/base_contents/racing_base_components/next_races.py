from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_tab_content import RacingEventsAccordionsList


class ExtraPlaceModule(RacingEventsAccordionsList):
    _extra_place_module_event_link = 'xpath=.//*[@data-crlat="exLink"]'
    _extra_place_race = 'xpath=.//*[@data-crlat="promotionIcon.EPR"]'
    _arrow_icon = 'xpath=.//*[@data-crlat="nextArrow"]'
    _event_name = 'xpath=.//*[@data-crlat="raceCard.eventName"]'

    @property
    def extra_place_race(self):
        return ButtonBase(selector=self._extra_place_race, context=self._we)

    @property
    def arrow_icon(self):
        return ComponentBase(selector=self._arrow_icon)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._event_name)

    @property
    def value(self):
        value = self._get_webelement_text(we=self._we)
        return value.replace(')', '').split('(')

    @property
    def event_id(self):
        link = LinkBase(selector=self._extra_place_module_event_link, timeout=0, context=self._we)
        return link.get_link().split('/')[-1]


class ExtraPlaceModuleItems(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="raceCard.event"]'
    _list_item_type = ExtraPlaceModule


class LadbrokesNextRaces(ComponentBase):
    _extra_place_module = 'xpath=.//*[@data-crlat="extraPlaceHomeMod"]'

    @property
    def extra_place_module_dict(self):
        return ExtraPlaceModuleItems(selector=self._extra_place_module, context=self._we)

    @property
    def extra_place_module(self):
        return ExtraPlaceModule(selector=self._extra_place_module, context=self._we)

    def has_extra_place_module(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._extra_place_module, timeout=0).is_displayed(),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Extra Place Module status to be {expected_result}')
