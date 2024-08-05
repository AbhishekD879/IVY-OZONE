from voltron.pages.shared.components.international_tote_carousel import ToteEventsCarousel
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.racing_base_components.greyhound_racing_accordions_list import \
    GreyhoundRacingEventsAccordionsList
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_accordions_list import \
    RacingEventsAccordionsList, InternationalHorseRacingLabel
from voltron.pages.shared.components.build_card import BuildCard
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class RacingTabContent(TabContent):
    _accordions_list_type = RacingEventsAccordionsList
    _build_own_card_type = BuildCard
    _build_own_card = 'xpath=.//*[@data-crlat="buildCardContainer"]'
    _tote_carousel = 'xpath=.//*[@data-crlat="toteEventsCarousel"]'
    _international_label = 'xpath=.//*[@class="inter"] | .//*[@class="split-header"] | .//*[contains(text(), "International")]/ancestor::header'

    @property
    def build_card(self):
        return self._build_own_card_type(selector=self._build_own_card, context=self._we)

    @property
    def tote_events_carousel(self):
        return ToteEventsCarousel(selector=self._tote_carousel, context=self._we)

    @property
    def international_label(self):
        return InternationalHorseRacingLabel(selector=self._international_label, context=self._we)


class GreyhoundRacingTabContent(TabContent):
    _accordions_list_type = GreyhoundRacingEventsAccordionsList
    _item = 'xpath=.//*[@data-crlat="buttonSwitch"]'
    _list_item_type = ButtonBase

    @property
    def current(self):
        # todo: VOL-1616
        # self.items is used below because some switchers have incorrect structure with duplicated selector
        # <a class="switch-btn" data-crlat="buttonSwitch"><span data-crlat="buttonSwitch">90 mins</span></a>
        wait_for_result(lambda: all([item.name for item in self.items]),
                        name=f'{self.__class__.__name__} - {self._list_item_type.__name__} to have text present',
                        timeout=1.5)
        button_name = next((button.name for button in self.items if button.is_selected(timeout=0.5)), '')
        return button_name

    def click_button(self, button_name: str):
        selection_buttons = self.items_as_ordered_dict
        if button_name not in selection_buttons:
            raise VoltronException('Tab name "%s" is not available, one of ["%s"] expected'
                                   % (button_name, '", "'.join(selection_buttons.keys())))
        self.scroll_to_we()
        if selection_buttons[button_name].is_selected():
            self._logger.warning(f'*** Bypassing click on tab as tab "{button_name}" is already active')
            return True
        else:
            selection_buttons[button_name].click()
            return wait_for_result(lambda: self.current == button_name,
                                   name=f'Button: "{button_name}" become active"',
                                   timeout=2)
