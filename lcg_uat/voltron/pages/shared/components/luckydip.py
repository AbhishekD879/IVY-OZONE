from collections import OrderedDict
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import QuickBetButtonBase, ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.dialogs.dialog_base import Dialog


class LuckyDipInfoBanner(Dialog):
    _info_banner = 'xpath=.//*[@class="body"]'
    _info_market_title = 'xpath=.//*[@class="marketHeader"]'
    _info_market_description = 'xpath=.//*[@class="marketDescription"]'
    _info_close_button = 'xpath=//*[@data-uat="popUpCloseButton"]'

    @property
    def info_market_title(self):
        return self._get_webelement_text(selector=self._info_market_title, timeout=1)

    @property
    def info_market_description(self):
        return self._get_webelement_text(selector=self._info_market_description, timeout=1)

    @property
    def has_lucky_dip_info_banner(self, expected_result=True, timeout=3):
        self.scroll_to_we()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._info_banner, timeout=1) is not None,
            name=f'{self.__class__.__name__} "Lucky Dip Info Banner" displayed status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def info_close_button(self):
        return self._find_element_by_selector(selector=self._info_close_button, timeout=1)

    @property
    def has_lucky_dip_info_close_button(self, expected_result=True, timeout=3):
        self.scroll_to_we()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._info_close_button, timeout=1) is not None,
            name=f'{self.__class__.__name__} "Lucky Dip Info Close(x)" displayed status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)


class LuckyDipQBSplashContainer(ComponentBase):
    _lucky_dip_animation = 'xpath=.//*[@class="splash-modal-container splashModal"]'
    _lucky_dip_content_info = 'xpath=.//*[@class="luckydip-content-info"]'
    _lucky_dip_content_title = 'xpath=.//*[@class="luckydip-content-title"]'
    _lucky_dip_content_step = 'xpath=.//*[@class="luckydip-content-steps"]/span[{}]/div[2]'
    _close_lucky_dip_popup = 'xpath=.//*[@class="btn-close closePopup"]'
    _lucky_dip_content_tnc_link = 'xpath=.//*[@class="luckydip-content-tnc"]//a'
    _lucky_dip_logo_banner = 'xpath=.//*[@class="splashModal-bContainer_logoBanner-img"]'

    @property
    def lucky_dip_content_terms_and_conditions_link(self):
        return self._find_element_by_selector(selector=self._lucky_dip_content_tnc_link, timeout=1)

    @property
    def get_lucky_dip_content_info(self):
        return self._get_webelement_text(selector=self._lucky_dip_content_info, timeout=1)

    @property
    def get_lucky_dip_content_title(self):
        return self._get_webelement_text(selector=self._lucky_dip_content_title, timeout=1)

    def has_close_icon_on_lucky_dip_popup(self, expected_result=True, timeout=3):
        self.scroll_to_we()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._close_lucky_dip_popup, timeout=1) is not None,
            name=f'{self.__class__.__name__} "close(X) icon" on lucky dip popup displayed status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_lucky_dip_content_terms_and_conditions_link(self, expected_result=True, timeout=3):
        self.scroll_to_we()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._lucky_dip_content_tnc_link, timeout=1) is not None,
            name=f'{self.__class__.__name__} "terms and conditions link" on lucky dip popup displayed status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_lucky_dip_animation(self, expected_result=True, timeout=3):
        self.scroll_to_we()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._lucky_dip_animation, timeout=1) is not None,
            name=f'{self.__class__.__name__} "Lucky Dip Animation" displayed status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_lucky_dip_logo_banner(self, expected_result=True, timeout=3):
        self.scroll_to_we()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._lucky_dip_logo_banner, timeout=1) is not None,
            name=f'{self.__class__.__name__} "luckydip logo banner" displayed status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def get_lucky_dip_content_step(self, step="1"):
        return self._get_webelement_text(selector=self._lucky_dip_content_step.format(step), timeout=1)


class LuckyDipGotItPanel(Dialog):
    _lucky_dip_got_it_button = 'xpath=.//*[@class="button btn-secondary lucky-dip"]'
    _player_name = 'xpath=.//*[@class="playerName"]'
    _player_card_description = 'xpath=//*[@class="playerCardDescriptionPotential"]'
    _potential_returns_description = 'xpath=.//*[@class="returnsDescription"]'
    _lucky_dip_got_it_panel = 'xpath=.//*[@class="container"]'
    _outcome_value = 'xpath=.//*[@class="outcomeValue"]'
    _potential_return = 'xpath=.//*[@class="amount"]'
    _share_button_layout = 'xpath=.//*[@data-crlat="luckyDipshareBtnLayout"]'
    _share_button_text = 'xpath=.//*[@data-crlat="shareText"]'
    _share_icon = 'xpath=.//*[@data-crlat="shareIcon"]'

    @property
    def lucky_dip_QB_splash_container(self):
        return LuckyDipQBSplashContainer(selector=self._dialog_content)

    @property
    def lucky_dip_potential_returns(self):
        return self._get_webelement_text(selector=self._potential_return)

    @property
    def lucky_dip_potential_returns_value(self):
        potential_returns = self._get_webelement_text(selector=self._potential_return)
        return self.strip_currency_sign(potential_returns)

    @property
    def lucky_Dip_got_it_button(self):
        context = QuickBetButtonBase(selector=self._lucky_dip_got_it_button)
        context.is_enabled(timeout=5)
        return context

    @property
    def lucky_dip_player_name(self):
        player_name = self._get_webelement_text(selector=self._player_name)
        return player_name

    @property
    def lucky_dip_player_card_description(self):
        return self._get_webelement_text(selector=self._player_card_description)

    @property
    def lucky_dip_potential_returns_description(self):
        return self._get_webelement_text(selector=self._potential_returns_description)

    @property
    def lucky_Dip_got_it_button_description(self):
        return self._get_webelement_text(selector=self._lucky_dip_got_it_button)

    @property
    def outcome_value(self):
        return self._get_webelement_text(selector=self._outcome_value)

    def has_lucky_dip_got_it_panel(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._lucky_dip_got_it_panel, timeout=2),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Lucky dip got it panel displayed status to be {expected_result}')
    @property
    def lucky_Dip_share_button(self):
        context = QuickBetButtonBase(selector=self._share_button_layout)
        context.is_enabled(timeout=5)
        return context


    def has_lucky_Dip_share_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._share_button_layout, timeout=2),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'lucky dip share button displayed status to be {expected_result}')

    @property
    def lucky_dip_share_name(self):
        share_button_name = self._get_webelement_text(selector=self._share_button_text)
        return share_button_name

    @property
    def get_lucky_dip_share_icon(self):
        return self._find_element_by_selector(selector=self._share_icon, timeout=1)



class Outcome(ComponentBase):
    _outcome_name = 'xpath=.//*[@class="marketName"]'
    _output_price_button = 'xpath=.//*[@id="luckyDipBtn"]'

    @property
    def outcome_name(self):
        return self._get_webelement_text(selector=self._outcome_name)

    @property
    def name(self):
        return self.outcome_name

    @property
    def output_price(self):
        we_text = self._get_webelement_text(selector=self._output_price_button)
        if we_text != '':
            return we_text
        else:
            return VoltronException(message='Output price on btn is not found')

    @property
    def bet_button(self):
        return BetButton(selector=self._output_price_button, context=self._we)


class MarketOutcomesList(ComponentBase):
    _item = 'xpath=.//*[@class="selectionContent"]'
    _list_item_type = Outcome
    _terms = 'xpath=.//*[@class="marketDesc"]'

    @property
    def has_terms(self):
        return self._find_element_by_selector(selector=self._terms, timeout=0) is not None

    @property
    def terms_text(self):
        return self._get_webelement_text(selector=self._terms)


class LuckyDip(LuckyDipGotItPanel, Accordion):
    _luckydip_odds_button = 'xpath=.//*[@id="luckyDipBtn"]'
    _luckydip_info_icon = 'xpath=.//*[@class="infoIcon"]'
    _market_discription = 'xpath=.//*[@class="marketDesc"]'
    _outcomes_list = 'xpath=.//*[@data-crlat="containerContent"] | .//accordion-body'
    _outcomes_list_type = MarketOutcomesList

    @property
    def outcomes(self):
        return self._outcomes_list_type(selector=self._outcomes_list, context=self._we)

    @property
    def odds(self):
        return self._find_element_by_selector(selector=self._luckydip_odds_button, timeout=5)

    @property
    def has_info_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._luckydip_info_icon, timeout=2),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Info icon displayed status to be {expected_result}')

    @property
    def info_icon(self):
        return self._find_element_by_selector(selector=self._luckydip_info_icon, timeout=5)

    @property
    def market_discription(self):
        return self._get_webelement_text(selector=self._market_discription, timeout=5).upper()

    @property
    def lucky_dip_info(self):
        return LuckyDipInfoBanner(selector=self._dialog_content)

    def expand(self):
        if self.is_expanded():
            pass
        else:
            self.section_header.click()
            wait_for_result(lambda: self.is_expanded(timeout=0),
                            name=f'"{self.__class__.__name__}" section to expand',
                            timeout=3)

    def collapse(self):
        if not self.is_expanded():
            pass
        else:
            self.section_header.click()
            wait_for_result(lambda: self.is_expanded(expected_result=False, timeout=0),
                            expected_result=False,
                            name=f'"{self.__class__.__name__}" section to collapse',
                            timeout=3)

class LuckyDipBetShareDialogLayout(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="descHeading"]'
    _desc_data = 'xpath=.//*[@data-crlat="descData"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)

    @property
    def desc_data(self):
        return self._get_webelement_text(selector=self._desc_data, context=self._we)


class BetShareDialog(Dialog):
    _lucky_bet_share_title = 'xpath=.//*[@data-crlat="shareTitle"]'
    _lucky_bet_share_description = 'xpath=.//*[@data-crlat="titleDesc"]'
    _check_box = 'xpath=.//*[@data-crlat="Checkbox"]'
    _item = 'xpath=.//*[@data-crlat="descLayout"]'
    _list_item_type = LuckyDipBetShareDialogLayout
    _preference_description = 'xpath=.//*[@data-crlat="descData"]'
    _cancel_button = 'xpath=.//*[@data-crlat="cancelBtnLayout"]'
    _share_button = 'xpath=.//*[@data-crlat="shareBtnLayout"]'

    @property
    def get_lucky_dip_bet_share_title(self):
        return self._get_webelement_text(selector=self._lucky_bet_share_title, timeout=1)

    @property
    def get_lucky_dip_bet_share_description(self):
        return self._get_webelement_text(selector=self._lucky_bet_share_description)

    @property
    def check_box(self):
        return ButtonBase(selector=self._check_box, context=self._we)

    def has_checkbox(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._check_box, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Checkbox presence status to be "{expected_result}"')

    @property
    def get_lucky_dip_bet_share__preference_description(self):
        return self._get_webelement_text(selector=self._preference_description)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def share_button(self):
        return ButtonBase(selector=self._share_button, context=self._we)

    @property
    def items_as_ordered_dict(self):
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            name = f'{items_we.index(item_we)} {list_item.name}'
            items_ordered_dict.update({name: list_item})
        return items_ordered_dict


