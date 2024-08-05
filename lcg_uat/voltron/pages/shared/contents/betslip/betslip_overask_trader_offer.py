from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.betslip.betslip_stake import BetslipStake
from voltron.utils.waiters import wait_for_result


class StakeOdd(TextBase):
    _value = 'xpath=.//*[@data-crlat="stOddNumber"]'

    @property
    def value_color(self):
        return ComponentBase(selector=self._value, context=self._we).background_color_value


class TraderOfferItem(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="bsStakeTitle"]'
    _color_elem = 'xpath=.//*[@data-crlat="stOddNumber"]'
    _stake_odds = 'xpath=.//*[@data-crlat="stakeOdds"]'

    @property
    def name(self):
        return self._get_webelement_text(self._name, context=self._we)

    @property
    def stake_odds(self):
        return StakeOdd(self._stake_odds, context=self._we)


class StakeEstReturn(TextBase):
    _est_returns = 'xpath=.//*[@data-crlat="oEstRetValue"]'
    _value = 'xpath=.//*[@data-crlat="oEstRetValue"]'

    @property
    def value(self):
        return self._wait_for_not_empty_web_element_text(selector=self._value, timeout=5).strip()


class StakeValue(TextBase):
    _value = 'xpath=.//*[@data-crlat="stakeValue"]'

    @property
    def value_color(self):
        return ComponentBase(selector=self._value, context=self._we).background_color_value


class OddValue(StakeValue):
    _value = 'xpath=.//*[@class="stake-odd-number"]'


class StakeEachWay(TextBase):
    _name = 'xpath=.//*[@class="bs.EWE"]'
    _each_way_tick = 'xpath=.//*[@class="bs-stake-check"]'
    _label = 'xpath=.//*[@data-crlat="oEWText"]'
    _tick = 'xpath=.//*[@data-crlat="oEWText"]'

    @property
    def each_way_tick(self):
        return ComponentBase(selector=self._each_way_tick, context=self._we)

    @property
    def has_tick(self):
        has_ew = self._find_element_by_selector(selector=self._tick, context=self._we, timeout=3)
        return has_ew is not None


class StakeContent(ComponentBase):
    _est_ret = 'xpath=.//*[@data-crlat="oEstRet"]'
    _stake_odds = 'xpath=.//*[@data-crlat="stBodyRow"]'
    _each_way = 'xpath=.//*[@data-crlat="oEachWay"]'
    _stake_message = 'xpath=.//*[@data-crlat="stakeMsg"]'
    _win_only_sign_post = 'xpath=.//*[contains(@class,"bs-stake-each-way")]'

    @property
    def win_only_sign_post(self):
        return TextBase(selector=self._win_only_sign_post, context=self._we, timeout=3).name

    @property
    def odd_value(self):
        return OddValue(selector=self._stake_odds, context=self._we)

    @property
    def est_returns(self):
        return StakeEstReturn(selector=self._est_ret, context=self._we)

    @property
    def stake_value(self):
        return StakeValue(selector=self._stake_odds, context=self._we)

    @property
    def each_way(self):
        return StakeEachWay(selector=self._each_way, context=self._we)

    @property
    def has_each_way(self):
        has_ew = self._find_element_by_selector(selector=self._each_way, context=self._we, timeout=3)
        return has_ew is not None

    @property
    def stake_message(self):
        return TextBase(selector=self._stake_message, context=self._we, timeout=3).name


class OveraskTraderOfferPrices(BetslipStake):
    _item = 'xpath=.//*[@data-crlat="mulBetPart"]'
    _list_item_type = TraderOfferItem
    _overask_stake_odds = 'xpath=.//*[@data-crlat="stBodyRow"]'
    _stake_content = 'xpath=.//*[@data-crlat="stakeContent"]'

    @property
    def stake_content(self):
        return StakeContent(selector=self._stake_content, context=self._we)


class MultipleBetsSplit(ComponentBase):
    _name = 'xpath=.//*[@data-uat="selectionName"] | .//*[@data-crlat="bsStakeTitle"]'
    _stake_odds = 'xpath=.//*[@class="stake-odds"]'
    _remove_btn = 'xpath=.//*[@data-crlat="selectStakeCheckbox"]'
    _est_returns = 'xpath=.//*[@data-crlat="oEstRet"]'
    _stake_value = 'xpath=.//*[@data-crlat="stakeValue"]'
    _undo_icon = 'xpath=.//*[@data-crlat="oUndoBtn"]'
    _leg_remove_marker = 'xpath=.//*[@class="bs-stake-info"]'

    @property
    def undo_icon(self):
        return self._find_element_by_selector(selector=self._undo_icon, context=self._we)

    @property
    def leg_remove_marker(self):
        return self._find_element_by_selector(selector=self._leg_remove_marker, context=self._we)

    @property
    def name(self):
        return self._get_webelement_text(self._name, context=self._we).replace('(', '').replace(')', '')

    @property
    def stake_odds(self):
        return StakeOdd(self._stake_odds, context=self._we)

    @property
    def remove_btn(self):
        return self._find_element_by_selector(self._remove_btn, context=self._we)

    def has_remove_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._remove_btn,
                                                                      timeout=0.5) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Remove Button status to be "{expected_result}"')

    @property
    def est_returns(self):
        return self._find_element_by_selector(self._est_returns, context=self._we)

    @property
    def stake_value(self):
        return StakeValue(selector=self._stake_value, context=self._we)


class OveraskTraderOfferSection(ComponentBase):
    _item = 'xpath=.//div[@data-crlat="stakeContent"] | .//*[@data-crlat="mulBetPart"]'
    _list_item_type = MultipleBetsSplit
    _trader_message = 'xpath=.//*[@data-crlat="oTraderOffer"]'
    _expires_message = 'xpath=.//*[@data-crlat="oExpOffer"]'
    _trader_offer_info_icon = 'xpath=.//*[@class="bs-overask-trader-offer-info-icon"]'

    @property
    def trader_message(self):
        return TextBase(selector=self._trader_message, context=self._we, timeout=10).name

    @property
    def expires_message(self):
        return TextBase(selector=self._expires_message, context=self._we, timeout=10).name

    @property
    def trader_offer_info_icon(self):
        return self._find_element_by_selector(self._trader_offer_info_icon, context=self._we)
