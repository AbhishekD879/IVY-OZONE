from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class PromotionIcons(ComponentBase):
    _fallers_insurance = 'xpath=.//*[@data-crlat="promotionIcon.FI"]'
    _beaten_by_a_length = 'xpath=.//*[@data-crlat="promotionIcon.BBAL"]'
    _extra_place_race = 'xpath=.//*[@data-crlat="promotionIcon.EPR"]'
    _double_your_winnings = 'xpath=.//*[@data-crlat="promotionIcon.DYW"]'
    _your_call = 'xpath=.//*[@data-crlat="promotionIcon.YOUR_CALL"]'
    _money_back = 'xpath=.//*[@data-crlat="promotionIcon.MB"]'
    _price_boost = 'xpath=.//*[@data-crlat="promotionIcon.PB"]'

    @property
    def fallers_insurance(self):
        return ButtonBase(selector=self._fallers_insurance, timeout=0, context=self._we)

    def has_fallers_insurance(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._fallers_insurance, timeout=0) is not None,
            name=f'"Fallers Insurance" icon status to be "{expected_result}"', expected_result=expected_result,
            timeout=timeout)

    @property
    def beaten_by_a_length(self):
        return ButtonBase(selector=self._beaten_by_a_length, timeout=0, context=self._we)

    def has_beaten_by_a_length(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._beaten_by_a_length, timeout=0) is not None,
            name=f'"Beaten By a Length" icon status to be "{expected_result}"', expected_result=expected_result,
            timeout=timeout)

    @property
    def extra_place_race(self):
        return ButtonBase(selector=self._extra_place_race, timeout=0, context=self._we)

    def has_extra_place_race(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._extra_place_race, timeout=0) is not None,
            name=f'"Extra Place Race" icon status to be "{expected_result}"', expected_result=expected_result,
            timeout=timeout)

    @property
    def double_your_winnings(self):
        return ButtonBase(selector=self._double_your_winnings, timeout=0, context=self._we)

    def has_double_your_winnings(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._double_your_winnings, timeout=0) is not None,
            name=f'"Double Your Winnings" icon status to be "{expected_result}"', expected_result=expected_result,
            timeout=timeout)

    @property
    def your_call(self):
        return ButtonBase(selector=self._your_call, timeout=0, context=self._we)

    def has_your_call(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._your_call, timeout=0) is not None,
            name=f'"Your Call" icon status to be "{expected_result}"', expected_result=expected_result,
            timeout=timeout)

    @property
    def money_back(self):
        return ButtonBase(selector=self._money_back, timeout=0, context=self._we)

    def has_money_back(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._money_back, timeout=0) is not None,
            name=f'"Money Back" icon status to be "{expected_result}"', expected_result=expected_result,
            timeout=timeout)

    @property
    def price_boost(self):
        return ButtonBase(selector=self._price_boost, timeout=0, context=self._we)

    def has_price_boost(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._price_boost, timeout=0) is not None,
            name=f'"Price boost" icon status to be "{expected_result}"', expected_result=expected_result,
            timeout=timeout)
