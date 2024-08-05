from collections import OrderedDict
from voltron.pages.ladbrokes.contents.virtuals.virtual_sports import LadbrokesVirtualSports
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.utils.waiters import wait_for_result


class VirtualSportItem(LadbrokesVirtualSports):
    _sport_name = 'xpath=.//*[@data-crlat="virtualSportName"]'
    _sport_sign_post = 'xpath=.//*[@data-crlat="virtualSportSignPost"]'
    _link = 'xpath=.//*[@class="top-sports-image"]'

    @property
    def get_href(self):
        element = self._find_element_by_selector(selector=self._link, context=self._we,
                                       timeout=0)
        return element.get_attribute('href')

    @property
    def link(self):
        return LinkBase(selector=self._link, context=self._we,
                                                 timeout=0)

    def has_sign_post(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._sport_sign_post, context=self._we,
                                                   timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def sign_post(self):
        return self._get_webelement_text(selector=self._sport_sign_post, context=self._we, timeout=3)

    @property
    def sport_name(self):
        return self._get_webelement_text(selector=self._sport_name, context=self._we, timeout=3).split('\n')[0]


class VirtualSportWrapperItem(VirtualSportItem):
    _item_name = 'xpath=.//*[@data-crlat="virtualSectionHeaderName"]'
    _item = 'xpath=.//*[@data-crlat="virtualSportWrapper"]'
    _list_item_type = VirtualSportItem
    _previous_arrow = 'xpath=.//*[@class="lc-carousel__prev arrow-chevron"]'
    _next_arrow = 'xpath=.//*[@class="lc-carousel__next arrow-chevron"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._item_name, context=self._we, timeout=3)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            list_item.scroll_to()
            items_ordered_dict.update({list_item.sport_name.upper(): list_item})
        return items_ordered_dict

    @property
    def previous_arrow(self):
        return ButtonBase(selector=self._previous_arrow, context=self._we)

    @property
    def next_arrow(self):
        return ButtonBase(selector=self._next_arrow, context=self._we)


class VirtualNextEventOutcomes(ComponentBase):
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'
    _name = 'xpath=.//*[@data-crlat="oddsNames"]'

    @property
    def bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we, timeout=3).split('\n')[0]


class VirtualNextEventItem(LadbrokesVirtualSports):
    _name = 'xpath=.//*[@class="slide-title"]'
    _bottom_text = 'xpath=.//*[@class="button-text"]'
    _race_time_counter = 'xpath=.//*[@data-crlat="raceCountdown"]'
    _item = 'xpath=.//*[@data-crlat="outcomeEntity"]'
    _list_item_type = VirtualNextEventOutcomes

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we, timeout=3).split('\n')[0]

    @property
    def bottom_link_text(self):
        return self._get_webelement_text(selector=self._bottom_text, context=self._we, timeout=3)

    @property
    def timer(self):
        return self._get_webelement_text(selector=self._race_time_counter, context=self._we, timeout=3)

    def has_timer(self, timeout=3, expected_result=True):
        self.scroll_to()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._race_time_counter,
                                                   timeout=0) is not None,
            name=f'waiting for timer to Present "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def bottom_link(self):
        return ButtonBase(selector=self._bottom_text, context=self._we)


class VirtualNextEvents(VirtualNextEventItem):
    _item_name = 'xpath=.//*[@class="slide-title"]'
    _item = 'xpath=.//*[@class="slide virtual-slide"]'
    _list_item_type = VirtualNextEventItem

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        count =1
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            list_item.scroll_to()
            items_ordered_dict.update({f'{count}.{list_item.name}': list_item})
            count = count+1
        return items_ordered_dict


class VirtualSectionWrapper(LadbrokesVirtualSports):
    _item = 'xpath=.//*[@data-crlat="virtualSectionWrapper"]'
    _name = 'xpath=.//*[@data-crlat="virtualSectionHeaderName" or @data-crlat="virtualNextEventSectionHeaderName"]'
    _sport_type = VirtualSportWrapperItem
    _next_event_type = VirtualNextEvents
    _accordions_list_type = {
        'Top Sports': _sport_type,
        'Other Sports': _sport_type,
        'Feature Zone': _sport_type,
        'Next Events': _next_event_type,
    }

    def _get_accordion_type(self, section):
        self.scroll_to_we(section)
        accordion_name = self._get_webelement_text(selector=self._name, context=section).title().strip()
        if accordion_name in self._accordions_list_type:
            accordion_template = self._accordions_list_type[accordion_name]
        else:
            accordion_template = self._sport_type
        return accordion_name, accordion_template(web_element=section)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_as_ordered_dict = OrderedDict()
        for item_we in items_we:
            accordion_name, accordion_template = self._get_accordion_type(section=item_we)
            if not (accordion_name == ''):
                items_as_ordered_dict.update({accordion_name: accordion_template}) if accordion_template else None
        return items_as_ordered_dict
