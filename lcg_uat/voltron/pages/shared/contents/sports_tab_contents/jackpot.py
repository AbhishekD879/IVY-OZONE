import re
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.odds_cards.jackpot_template import JackpotBetButton
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.utils.waiters import wait_for_result


class JackpotTabContent(TabContent):
    _lucky_dip = 'xpath=.//*[@data-crlat="luckyDipButton"]'
    _clear_selections = 'xpath=.//*[@data-crlat="clearSelectionsButton"]'
    _confirm_button = 'xpath=.//*[@data-crlat="confirmClearOfBetSlipButton"]'
    _place_bet = 'xpath=.//*[@data-crlat="placeBetButton"]'
    _stake_panel = 'xpath=.//*[@data-crlat="stakePanel"]'
    _error_message = 'xpath=.//*[@data-crlat="errorMessage"]'
    _verify_spinner = True

    @property
    def lucky_dip_button(self):
        return ButtonBase(selector=self._lucky_dip, context=self._we)

    @property
    def clear_all_selections_button(self):
        return ButtonBase(selector=self._clear_selections, context=self._we)

    @property
    def confirm_button(self):
        return ButtonBase(selector=self._clear_selections, context=self._we)

    @property
    def place_bet(self):
        return JackpotBetButton(selector=self._place_bet, context=self._we)

    @property
    def jackpot_stake_section(self):
        return StakeSection(selector=self._stake_panel, context=self._we)

    @property
    def error_message(self):
        return self._get_webelement_text(selector=self._error_message, context=self._we)

    def wait_for_error_message(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: self.error_message,
                               name='Jackpot error message to show up/hide',
                               expected_result=expected_result,
                               timeout=timeout)


class StakeSection(ComponentBase):
    _stake_per_line_label = 'xpath=.//*[@data-crlat="stakePerLineLabel"]'
    _stake_per_line = 'xpath=.//*[@data-crlat="stakePerLine"]'
    _stake_per_line_type = SelectBase
    _total_lines = 'xpath=.//*[@data-crlat="totalLines"]'
    _total_stake = 'xpath=.//*[@data-crlat="totalStake"]'
    _total_stake_label = 'xpath=.//*[@data-crlat="totalStakeLabel"]'

    @property
    def stake_per_line_label(self):
        return TextBase(selector=self._stake_per_line_label, context=self._we)

    @property
    def stake_per_line(self):
        return self._stake_per_line_type(selector=self._stake_per_line, context=self._we)

    @property
    def total_lines(self):
        total_lines = self._get_webelement_text(selector=self._total_lines, timeout=2)
        return total_lines if total_lines else '0'

    @property
    def total_stake(self):
        total_stake = self._get_webelement_text(selector=self._total_stake, timeout=2)
        return self.strip_currency_sign(total_stake).replace(',', '') if total_stake else ''

    @property
    def total_stake_currency(self):
        total_stake = self._get_webelement_text(selector=self._total_stake, timeout=2)
        return re.sub(r'\d+.\d+', '', total_stake)

    @property
    def total_stake_label(self):
        return TextBase(selector=self._total_stake_label, context=self._we)
