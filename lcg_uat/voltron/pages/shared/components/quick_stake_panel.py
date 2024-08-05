from voltron.pages.shared.components.keyboard.mobile_keyboard import Keyboard, Key
from voltron.utils.waiters import wait_for_result


class QuickStakeKey(Key):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class QuickStakePanel(Keyboard):
    _item = 'xpath=.//*[@data-crlat="quickStake.key"] | //button[@type="button" and contains(@class,"item md-button") ]'
    _list_item_type = QuickStakeKey
    _freebet_stake = 'xpath=.//*[@data-crlat="useFreeBet"] | .//*[@data-crlat="addFreeBetMobile"]'

    @property
    def free_bet(self):
        return self._find_element_by_selector(selector=self._freebet_stake, context=self._we)

    def has_use_free_bet_link(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._freebet_stake, timeout=0) is not None,
                               name=f'Has Use Free Bet Button displayed status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)
