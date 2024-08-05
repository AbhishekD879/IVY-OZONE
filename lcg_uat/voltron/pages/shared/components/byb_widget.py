from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


class BYBWidgetCardDetails(ComponentBase):
    _card_name = 'xpath=.//*[@data-crlat="card-main-popular"]'
    _card_odd = 'xpath=.//*[@data-crlat="betButton"]'

    @property
    def card_name(self):
        return self._get_webelement_text(selector=self._card_name, context=self._we)

    @property
    def name(self):
        return self.card_name

    @property
    def card_odds(self):
        return BetButton(selector=self._card_odd, context=self._we, timeout=2)

    def has_card_odds(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._card_odd, context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Bet button shown status to be {expected_result}')


class BYBWidgetSlide(ComponentBase):

    _content_section = 'xpath=.//*[@data-crlat="content-section"]'
    _bottom_section = 'xpath=.//*[@data-crlat="bottom-section"]'
    _byb_widget_header = 'xpath=.//*[@data-crlat="bybWidgetHeader"]'
    _byb_header_name = 'xpath= .//*[data-crlat="bybWidget-full-event-name"]'
    _event_first_name = 'xpath=.//*[@data-crlat="event-first-name"]'
    _event_last_name = 'xpath=.//*[@data-crlat="event-last-name"]'
    _item = 'xpath=.//*[@data-crlat="bybWidgetCard.odds"]'
    _list_item_type = BYBWidgetCardDetails
    _left_arrow = 'xpath=.//*[@data-crlat="left-arrow"]'
    _right_arrow = 'xpath=.//*[@data-crlat="right-arrow"]'
    _byb_widget_footer = 'xpath=.//*[@data-crlat="footer"]'
    _byb_icon = 'xpath=.//*[@data-crlat="byb-icon"]'
    _byb_icon_text = 'xpath=.//*[@data-crlat="icon-text"]'
    _byb_footer_page_count = 'xpath=.//*[@data-crlat="pagenatorCounter"]'

    @property
    def byb_card_details(self):
        return self.items_as_ordered_dict

    def has_byb_section(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._content_section, context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'BYB content section shown status to be {expected_result}')

    def has_byb_bottom_section(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._bottom_section, context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'BYB bottom section shown status to be {expected_result}')

    @property
    def byb_widget_header(self):
        return ButtonBase(selector=self._byb_widget_header, timeout=1, context=self._we)

    def has_byb_widget_header(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._byb_widget_header,
                                                   timeout=0) is not None,
            name=f'Byb Widget Header status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
    @property
    def event_first_name(self):
        return self._get_webelement_text(selector=self._event_first_name, timeout=1, context=self._we)

    @property
    def event_last_name(self):
        return self._get_webelement_text(selector=self._event_last_name, timeout=1, context=self._we)

    @property
    def name(self):
        return self.event_first_name + ' v ' + self.event_last_name

    @property
    def left_arrow(self):
        return ButtonBase(selector=self._left_arrow, context=self._we, timeout=1)

    def has_left_arrow(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._left_arrow,
                                                   timeout=0) is not None,
            name=f'Left arrow status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def right_arrow(self):
        return ButtonBase(selector=self._right_arrow, context=self._we, timeout=1)

    def has_right_arrow(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._right_arrow, timeout=1, context=self._we) is not None,
            name=f'right arrow status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_byb_widget_footer(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._byb_widget_footer, timeout=1,
                                                   context=self._we) is not None,
            name=f'BYB Widget Footer status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def byb_icon(self):
        return self._find_element_by_selector(selector=self._byb_icon, timeout=1, context=self._we)

    def has_byb_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._byb_icon, timeout=1,
                                                   context=self._we) is not None,
            name=f'BYB icon text status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def build_your_own_link(self):
        return ButtonBase(selector=self._byb_icon_text, timeout=1, conftest=self._we)

    @property
    def build_your_own_text(self):
        return self._get_webelement_text(selector=self._byb_icon_text, timeout=1, context=self._we)

    def has_byb_icon_text(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._byb_icon_text, timeout=1,
                                                   context=self._we) is not None,
            name=f'BYB icon text status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def byb_footer_page_counter(self):
        return self._get_webelement_text(selector=self._byb_footer_page_count, timeout=1, context=self._we)


class BYBWidget(Accordion):
    _title = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _chevron_arrow = 'xpath=.//*[@class="chevron-svg chevron-up"]'
    _item = 'xpath=.//*[@data-crlat="slide"]'
    _list_item_type = BYBWidgetSlide

    @property
    def chevron_arrow(self):
        return self._find_element_by_selector(selector=self._chevron_arrow, timeout=1, context=self._we)

    def has_chevron_arrow(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._chevron_arrow,
                                                   timeout=0, context=self._we) is not None,
            name=f'Chevron arrow status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def title_text(self):
        return self._get_webelement_text(selector=self._title, timeout=1, context=self._we)

    @property
    def name(self):
        return self.title_text


class BYBContainer(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="trending-acc"]'
    _list_item_type = BYBWidget
    _arrow_next = 'xpath=.//*[@data-crlat="arrow-next"]'
    _arrow_prev = 'xpath=.//*[@data-crlat="arrow-prev"]'

    def arrow_next(self):
        click(self._find_element_by_selector(selector=self._arrow_next, context=self._we, timeout=1))

    def has_arrow_next(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._arrow_next,
                                                   timeout=0) is not None,
            name=f'Next arrow status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


    def arrow_prev(self):
        click(self._find_element_by_selector(selector =self._arrow_prev,context=self._we, timeout=1))

    def has_arrow_prev(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._arrow_prev,
                                                   timeout=0) is not None,
            name=f'Previous arrow status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
