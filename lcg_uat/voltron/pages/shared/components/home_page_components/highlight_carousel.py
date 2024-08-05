from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.odds_cards.highlight_carousel_template import HighlightCarouselTemplate
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class HighlightCarousel(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="highlightsCarousel.title"]'
    _item = 'xpath=.//*[@data-crlat="oddsCard.sportTemplate"]'
    _list_item_type = HighlightCarouselTemplate
    _see_all_link = 'xpath=.//*[@data-crlat="moreLink"]'
    _svg_icon_text = 'xpath=.//*[@class="icon"]/*/*'
    _hc_scroll_next = 'xpath=.//*[@class="highlight-carousel-buttons"]/button[@class="hc-arrow next-hc-card"]'
    _hc_scroll_prev = 'xpath=.//*[@class="highlight-carousel-buttons"]/button[@class="hc-arrow prev-hc-card"]'
    _hc_button_container = 'xpath=.//*[@class="highlight-carousel-buttons"]'

    @property
    def svg_icon_text(self):
        return self._find_element_by_selector(selector=self._svg_icon_text).get_attribute('xlink:href')

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)

    @property
    def see_all_link(self):
        return ButtonBase(selector=self._see_all_link, context=self._we)

    @property
    def scroll_previous_button(self):
        return ButtonBase(selector=self._hc_scroll_prev, context=self._we)

    @property
    def scroll_next_button(self):
        return ButtonBase(selector=self._hc_scroll_next, context=self._we)

    def has_scroll_button(self, expected_result=True, timeout=2):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._hc_button_container, timeout=0) is not None,
            name=f'See All link shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_next_button(self, expected_result=True, timeout=2):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._hc_scroll_next, timeout=0) is not None,
            name=f'next button shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_prev_button(self, expected_result=True, timeout=2):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._hc_scroll_prev, timeout=0) is not None,
            name=f'prev button shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_see_all_link(self, expected_result=True, timeout=2):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._see_all_link, timeout=0) is not None,
            name=f'See All link shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)
