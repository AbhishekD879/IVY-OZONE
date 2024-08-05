from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.date_picker import DatePicker
from voltron.pages.shared.components.edit_acca_history import EditAccaHistoryHolder
from voltron.pages.shared.components.primitives.amount_field import AmountField
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.my_bets.cashout import Bet, CashoutEventsList, CashoutTabContent, Cashout, BetLeg
from voltron.pages.shared.contents.my_bets.my_bets import MyBetsBase
from voltron.pages.shared.contents.my_bets.open_bets.open_bets_jackpot_pool import JackpotTotePool
from voltron.pages.shared.contents.my_bets.open_bets.open_bets_lotto import LottoBet
from voltron.pages.shared.contents.my_bets.open_bets.open_bets_multiple_tote_pools import MultipleTotePool
from voltron.pages.shared.contents.my_bets.open_bets.open_bets_one_leg_pool import OneLegTotePool
from voltron.pages.shared.contents.my_bets.open_bets.open_bets_pool_bet_card import TotePoolBetCard
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


class PartialCashOutHistoryHeader(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="title"]'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, timeout=1)


class PartialCashOutHistoryTableItem(ComponentBase):
    _stake_used = 'xpath=.//*[@data-crlat="stakeUsed"]'
    _cash_out_amount = 'xpath=.//*[@data-crlat="cashoutValue"]'
    _data_time = 'xpath=.//*[@data-crlat="cashoutDate"]'

    @property
    def stake_used(self):
        return AmountField(selector=self._stake_used, context=self._we)

    @property
    def cash_out_amount(self):
        return AmountField(selector=self._cash_out_amount, context=self._we)

    @property
    def data_time(self):
        return TextBase(selector=self._data_time, context=self._we)

    @property
    def name(self):
        return 'Cashed Out: %s at %s' % (self.cash_out_amount._text, self.data_time.name)


class PartialCashOutHistoryTable(ComponentBase):
    _stake_used_label = 'xpath=.//*[@data-crlat="labelStakeUsed"]'
    _cash_out_amount_label = 'xpath=.//*[@data-crlat="labelCashOutAmount"]'
    _data_time_label = 'xpath=.//*[@data-crlat="labelDataTime"]'
    _item = 'xpath=.//*[@data-crlat="cashoutType"]'
    _list_item_type = PartialCashOutHistoryTableItem

    @property
    def stake_used_label(self):
        return TextBase(selector=self._stake_used_label, context=self._we)

    @property
    def data_time_label(self):
        return TextBase(selector=self._data_time_label, context=self._we)

    @property
    def cash_out_amount_label(self):
        return TextBase(selector=self._cash_out_amount_label, context=self._we)


class OpenBetsAmountField(AmountField):

    @property
    def amount(self):
        return self.value


class OpenBetsTextBase(TextBase):

    @property
    def value(self):
        return OpenBetsAmountField(selector=self._value, context=self._we)


class PartialCashOutHistoryContent(ComponentBase):
    _remaining_stake = 'xpath=.//*[@data-crlat="remainingStake"]'
    _total_cash_out = 'xpath=.//*[@data-crlat="totalCashOut"]'
    _total_cash_out_stake = 'xpath=.//*[@data-crlat="totalCashOutStake"]'
    _table = 'xpath=.//*[@data-crlat="tablePanel"]'

    @property
    def table(self):
        return PartialCashOutHistoryTable(selector=self._table, context=self._we)

    @property
    def total_cash_out_stake(self):
        return OpenBetsTextBase(selector=self._total_cash_out_stake, context=self._we)

    @property
    def total_cash_out(self):
        return OpenBetsTextBase(selector=self._total_cash_out, context=self._we)

    @property
    def remaining_stake(self):
        return OpenBetsTextBase(selector=self._remaining_stake, context=self._we)


class PartialCashOutHistory(ComponentBase):
    _header = 'xpath=.//*[@data-crlat="panelHeader"]'
    _content = 'xpath=.//*[@data-crlat="panelBody"]'

    @property
    def header(self):
        return PartialCashOutHistoryHeader(selector=self._header, context=self._we)

    @property
    def content(self):
        return PartialCashOutHistoryContent(selector=self._content, context=self._we)

    def has_content(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._content,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Content shown status to be {expected_result}')


class OpenBet(Bet, BetLeg):
    _partial_cash_out_history = 'xpath=.//*[contains(@data-crlat, "panel.cashOutHistory")]'
    _date = 'xpath=.//*[@data-crlat="displayDate"] | //*[@data-crlat="timerLabel"]'
    _date_without_timer_label = 'xpath=.//*[@data-crlat="displayDate"]'
    _odds_value = 'xpath=.//*[@data-crlat="oddsValue"]'
    _cashout_terms_and_conditions = 'xpath=.//*[contains(text(),"Cash Out Terms & Conditions")]'
    _ema_terms_and_conditions = 'xpath=.//*[contains(text(),"Edit My Acca Terms & Conditions")]'
    _retail_bets_SBT = 'xpath=.//*[contains(text(),"See Retail Bets on Shop Bet Tracker")]'
    _bet_type = 'xpath=.//*[@data-crlat="betType"]'
    _bog_icon_txt = 'xpath=.//*[contains(@class, "bog-label")]'
    _bog_label = 'xpath=.//*[@class="bog-label"]'
    _lucky_dip_icon = 'xpath=.//*[@class="promo-label small-icon"]'

    @property
    def bog_label(self):
        return self._find_element_by_selector(selector=self._bog_label, context=self._we)

    @property
    def bog_icon_txt(self):
        return self._get_webelement_text(selector=self._bog_icon_txt, context=self._we)

    @property
    def bog_icon(self):
        return self._find_element_by_selector(selector=self._bog_icon, context=self._we)

    @property
    def event_elements(self):
        return self._find_elements_by_selector(selector=self._event_name, context=self._we)

    @property
    def selection_elements(self):
        return self._find_elements_by_selector(selector=self._outcome_name, context=self._we)

    @property
    def market_elements(self):
        return self._find_elements_by_selector(selector=self._market_name, context=self._we)

    @property
    def odds_value(self):
        return self._get_webelement_text(selector=self._odds_value, context=self._we)

    @property
    def odds_sign(self):
        return self.before_element(selector=self._odds_value, context=self._we)

    @property
    def selection_name(self):
        return self._get_webelement_text(selector=self._outcome_name, context=self._we).replace('(', '').replace(')', '')

    @property
    def market_name(self):
        return self._get_webelement_text(selector=self._market_name, context=self._we)

    @property
    def date(self):
        return self._get_webelement_text(selector=self._date, context=self._we)

    @property
    def date_without_timer_label(self):
        return self._get_webelement_text(selector=self._date_without_timer_label, context=self._we)

    @property
    def partial_cash_out_history(self):
        return PartialCashOutHistory(selector=self._partial_cash_out_history, context=self._we)

    @property
    def bet_receipt_info(self):
        raise VoltronException('There is no Bet Receipt Info on OX99 design. Please Update autotest')

    @property
    def verify_CashOut_TC(self):
        CashOut_TC = self._find_element_by_selector(selector=self._cashout_terms_and_conditions, timeout=20)
        self.scroll_to_we(CashOut_TC)
        return CashOut_TC

    @property
    def verify_EMA_TC(self):
        EMA_TC = self._find_element_by_selector(selector=self._ema_terms_and_conditions, timeout=20)
        self.scroll_to_we(EMA_TC)
        return EMA_TC

    @property
    def verify_retailbets_on_SBT(self):
        retailbets_on_SBT = self._find_element_by_selector(selector=self._retail_bets_SBT, timeout=20)
        self.scroll_to_we(retailbets_on_SBT)
        return retailbets_on_SBT

    @property
    def bet_types(self):
        bet_headers = self._find_elements_by_selector(selector=self._bet_type, timeout=3)
        bet_headers_text = []
        for headers in bet_headers:
            bet_headers_text.append(headers.text)
        return bet_headers_text

    @property
    def lucky_dip_icon(self):
        return self._get_webelement_text(selector=self._lucky_dip_icon,timeout=3)


class OpenBetsEventsList(CashoutEventsList):
    _cached_list_item_type = None
    _bet_type_pattern = 'xpath=.//*[contains(@data-crlat, "betType.")]'
    _pool_type_pattern = 'xpath=.//*[contains(@data-crlat, "poolType.")]'
    _regular_bet_type = OpenBet
    _lotto_bet_type = LottoBet
    _tote_bet_type = TotePoolBetCard

    _multiple_legs_tote_pool_type = MultipleTotePool
    _jackpot_pool_type = JackpotTotePool
    _one_leg_tote_pool_type = OneLegTotePool

    @property
    def _list_item_type(self):
        if self._cached_list_item_type:
            return self._cached_list_item_type
        bet_type_we = self._find_element_by_selector(selector=self._bet_type_pattern, timeout=0)
        if not bet_type_we:
            self._logger.warning(f'*** Cannot detect BetType on Open Bets page, will use default "{self._regular_bet_type.__name__}"')
            self._cached_list_item_type = self._regular_bet_type
            return self._cached_list_item_type
        bet_type_attribute = bet_type_we.get_attribute('data-crlat')
        bet_types = {
            'betType.regular': self._regular_bet_type,
            'betType.lotto': self._lotto_bet_type,
            'betType.pool': self._tote_bet_type
        }
        if bet_type_attribute not in bet_types:
            self._logger.warning(f'*** Cannot detect BetType on Open Bets page, will use default "{self._regular_bet_type.__name__}"')
            self._cached_list_item_type = self._regular_bet_type
            return self._cached_list_item_type

        detected_bet_type = bet_types[bet_type_attribute]
        self._logger.debug('*** Detected "%s" bet type' % detected_bet_type.__name__)
        self._cached_list_item_type = bet_types[bet_type_attribute]

        if bet_type_attribute == 'betType.pool':
            pool_bet_type_we = self._find_element_by_selector(selector=self._pool_type_pattern, timeout=0)
            if not pool_bet_type_we:
                self._logger.warning(f'*** Cannot detect PoolType on Open Bets page, will use default "{self._tote_bet_type.__name__}"')
                self._cached_list_item_type = self._tote_bet_type
                return self._cached_list_item_type
            pool_type_attribute = pool_bet_type_we.get_attribute('data-crlat')
            pool_types = {
                'poolType.multipleLegs': self._multiple_legs_tote_pool_type,
                'poolType.jackpot': self._jackpot_pool_type,
                'poolType.oneLeg': self._one_leg_tote_pool_type
            }
            if pool_type_attribute not in pool_types:
                self._logger.warning(f'*** Cannot detect PoolType on Open Bets page, will use default "{self._regular_bet_type.__name__}"')
                self._cached_list_item_type = self._regular_bet_type
                return self._cached_list_item_type

            detected_pool_type = pool_types[pool_type_attribute]
            self._logger.debug('*** Detected "%s" pool type' % detected_pool_type.__name__)
            self._cached_list_item_type = detected_pool_type

        return self._cached_list_item_type

    def wait_for_sections(self, timeout=5):
        if not wait_for_result(lambda: len(self.items_as_ordered_dict) > 20,
                               name='"%s" of sections' % (len(self.items_as_ordered_dict)),
                               timeout=timeout):
            self._logger.warning(
                '*** Error waiting for sections, current number of sections is "%s"' % len(self.items_as_ordered_dict))


class OpenBetsTabContent(CashoutTabContent):
    _accordions_list_type = OpenBetsEventsList
    _no_open_bets_text = 'xpath=.//*[@data-crlat="textMsg"]'
    _date_picker = 'xpath=.//*[contains(@class,"datepickers-section")]'

    @property
    def no_open_bets_text(self):
        return self._get_webelement_text(selector=self._no_open_bets_text, timeout=2)

    @property
    def date_picker(self):
        return DatePicker(selector=self._date_picker, context=self._we)


class OpenBets(Cashout, MyBetsBase):
    _url_pattern = r'^http[s]?:\/\/.+\/open-bets'
    _tab_content_type = OpenBetsTabContent
    _tab_content = 'xpath=.//*[@data-crlat="tabContent"]'

    _edit_acca_history_content = 'xpath=.//*[@data-crlat="drawer.content"]'

    @property
    def edit_acca_history(self):
        return EditAccaHistoryHolder(selector=self._edit_acca_history_content, context=self._we, timeout=3)

    def _wait_active(self, timeout=5):
        try:
            self._find_element_by_selector(selector=self._tab_content, context=self._context,
                                           bypass_exceptions=(NoSuchElementException, ), timeout=3)
        except StaleElementReferenceException:
            self._logger.debug('*** Overriding StaleElementReferenceException in %s' % self.__class__.__name__)

    @property
    def tab_content(self):
        return self._tab_content_type(selector=self._tab_content)


class OpenBetsDesktop(Accordion, OpenBets):
    _url_pattern = r'^http[s]?:\/\/.+\/'
    _tab_content = 'xpath=.//*[@data-crlat="slideContent.openBets" or @data-crlat="slideContent.1"]/parent::*'
