from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase, SpinnerButtonBase, IconBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.components.quick_bet import QuickBet
from voltron.pages.shared.components.quick_bet import QuickBetContent
from voltron.pages.shared.components.quick_bet import QuickBetSelection
from voltron.utils.waiters import wait_for_result


class Outcome(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we, timeout=0.2).replace('\n', ' ')


class OutcomesSection(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="yourcallSelection"]'
    _list_item_type = Outcome


class BYBQuickBetContent(QuickBetContent):
    _outcomes_section = 'xpath=.//*[@data-crlat="section.selections"]'
    _outcomes_section_type = OutcomesSection

    @property
    def outcomes_section(self):
        return self._outcomes_section_type(selector=self._outcomes_section, context=self._we)


class BYBQuickBetSelection(QuickBetSelection):
    _freebet_stake = 'xpath=.//*[@data-crlat="fbValue"]'
    _total_stake_label = 'xpath=.//*[@data-crlat="totalStake.label"]'
    _total_stake = 'xpath=.//*[@data-crlat="totalStake"]'
    _total_est_returns_label = 'xpath=.//*[@data-crlat="estimatedResults.label"]'
    _total_est_returns = 'xpath=.//*[@data-crlat="totalEstReturns"]'
    _qb_content_type = BYBQuickBetContent
    _freebet_icon = 'xpath=.//*[@data-crlat="fbIcon"]'

    @property
    def total_est_returns_label(self):
        return self._get_webelement_text(selector=self._total_est_returns_label, timeout=0.2)

    @property
    def total_est_returns(self):
        return self._get_webelement_text(selector=self._total_est_returns, timeout=0.2)

    @property
    def total_est_returns_value(self):
        return self.strip_currency_sign(self.total_est_returns)

    @property
    def total_stake_label(self):
        return self._get_webelement_text(selector=self._total_stake_label, timeout=0.2)

    @property
    def total_stake(self):
        return self._get_webelement_text(selector=self._total_stake, timeout=0.2)

    @property
    def total_stake_value(self):
        return self.strip_currency_sign(self.total_stake)

    @property
    def freebet_stake(self):
        return TextBase(selector=self._freebet_stake, context=self._we)

    @property
    def freebet_icon(self):
        return IconBase(selector=self._freebet_icon, context=self._we)

    @property
    def freebet_stake_value(self):
        return self.strip_currency_sign(self.freebet_stake.text)


class ContestDetails(ComponentBase):
    _name = 'xpath=.//*[contains(@class,"contest-title")]'
    _active_contest = 'xpath=.//*[contains(@class,"contest-title contest-title-font-active")]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)

    @property
    def active_contest(self):
        return self._find_element_by_selector(selector=self._active_contest, context=self._we)

    def has_active_contest(self, expected_result=True, timeout=5):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._active_contest, timeout=1) is not None,
                                 name=f'contest to be "{expected_result}"',
                                 expected_result=expected_result,
                                 timeout=timeout)
        return result


class Contest(ComponentBase):
    _item = 'xpath=.//*[contains(@class, "contest-card")]'
    _list_item_type = ContestDetails
    _prev_arrow = 'xpath=.//*[contains(@class,"action-arrow left row-middle")]'
    _next_arrow = 'xpath=.//*[contains(@class,"action-arrow right row-middle")]'

    @property
    def prev_arrow(self):
        return self._find_element_by_selector(selector=self._prev_arrow, context=self._we)

    @property
    def next_arrow(self):
        return self._find_element_by_selector(selector=self._next_arrow, context=self._we)


class Leaderboard(ComponentBase):
    _contest_header = 'xpath=.//*[@class="primary-header"]'
    _contest = 'xpath=.//*[contains(@class,"swiper-container")]'

    @property
    def contest_header(self):
        return self._find_element_by_selector(selector=self._contest_header, context=self._we)

    @property
    def contest(self):
        return Contest(selector=self._contest, context=self._we)

    def has_contest(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._contest, timeout=0) is not None,
                               name=f'contest visible status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)


class BYBBetslip(QuickBet):
    _quickbet_selection_type = BYBQuickBetSelection
    _back_button = 'xpath=.//*[@data-crlat="addToBetslipButton" or @data-crlat="quickbet.back"]'
    _select_your_leaderboard = 'xpath=.//*[contains(@class,"contest-selection")]'

    @property
    def select_your_leaderboard(self):
        return Leaderboard(selector=self._select_your_leaderboard, context=self._we)

    def has_select_your_leaderboard(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._select_your_leaderboard, timeout=0) is not None,
                               name=f'select your leaderboard status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)


class BYBBetReceiptContent(BYBQuickBetContent):
    _bet_id_label = 'xpath=.//*[@data-crlat="betId.label"]'
    _bet_id_value = 'xpath=.//*[@data-crlat="betId.value"]'
    _odds_label = 'xpath=.//*[@data-crlat="oddsLabel"]'
    _type_name = 'xpath=.//*[@data-crlat="selType"]'
    _odds = 'xpath=.//*[@data-crlat="odds"]'

    @property
    def odds_label(self):
        return self._get_webelement_text(selector=self._odds_label, timeout=1)

    @property
    def bet_id_label(self):
        return self._get_webelement_text(selector=self._bet_id_label, timeout=0.2)

    @property
    def bet_id_value(self):
        return self._get_webelement_text(selector=self._bet_id_value, timeout=0.2)

    @property
    def type_name(self):
        return TextBase(selector=self._type_name, context=self._we)


class BYBBetReceiptSelection(BYBQuickBetSelection):
    _qb_content_type = BYBBetReceiptContent
    _reuse_selection = 'xpath=.//*[@data-crlat="reuseSelectionButton"]'
    _done_button = 'xpath=.//*[@data-crlat="doneButton"]'
    _total_est_returns = 'xpath=.//*[@data-crlat="estimatedResults.value"]'

    @property
    def reuse_selection_button(self):
        return ButtonBase(selector=self._reuse_selection, context=self._we)

    @property
    def done_button(self):
        return SpinnerButtonBase(selector=self._done_button, context=self._we)

    def has_freebet_icon(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._freebet_icon, timeout=0),
                               name='freebet icon to be shown/not shown',
                               expected_result=expected_result,
                               timeout=timeout)


class BYBBetReceipt(BYBBetslip):
    _quickbet_selection = 'xpath=.//*[@data-crlat="quickbetReceipt"]'
    _quickbet_selection_type = BYBBetReceiptSelection
