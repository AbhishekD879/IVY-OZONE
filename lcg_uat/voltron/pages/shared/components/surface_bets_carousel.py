from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.odds_cards.surface_bet_template import SurfaceBetTemplate
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class SurfaceBetsCarousel(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="surfaceBetCard"]'
    _list_item_type = SurfaceBetTemplate
    _sb_scroll_prev = 'xpath=.//*[@class="scroll-buttons"]//*[@class="hc-arrow prev-hc-card"]'
    _sb_scroll_next = 'xpath=.//*[@class="scroll-buttons"]//*[@class="hc-arrow next-hc-card"]'
    _sb_button_container = 'xpath=.//*[@class="scroll-buttons"]'
    @property
    def scroll_previous_button(self):
        return ButtonBase(selector=self._sb_scroll_prev, context=self._we)

    @property
    def scroll_next_button(self):
        return  ButtonBase(selector=self._sb_scroll_next, context=self._we)

    def has_next_button(self, expected_result=True, timeout=2):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._sb_scroll_next, timeout=0) is not None,
            name=f'next button shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_prev_button(self, expected_result=True, timeout=2):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._sb_scroll_prev, timeout=0) is not None,
            name=f'prev button shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_scroll_button(self, expected_result=True, timeout=2):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._sb_button_container, context=self._we, timeout=0) is not None,
            name=f'See All link shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)
