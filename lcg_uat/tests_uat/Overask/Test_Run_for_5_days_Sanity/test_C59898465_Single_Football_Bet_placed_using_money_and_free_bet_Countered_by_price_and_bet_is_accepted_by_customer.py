import pytest
import tests
from voltron.environments import constants as vec
from tests.base_test import vtest
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C59898465_Single_Football_Bet_placed_using_money_and_free_bet_Countered_by_price_and_bet_is_accepted_by_customer(BaseBetSlipTest):
    """
    TR_ID: C59898465
    NAME: Single Football Bet placed using money and free bet Countered by price and bet is accepted by customer
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    PRECONDITIONS: Customer should have Freebets in the account
    """
    keep_browser_open = True
    max_bet = 1.2
    suggested_max_bet = 0.94
    prices = {'odds_home': '1/12', 'odds_draw': '1/13', 'odds_away': '1/14'}
    event_names = []
    selection_ids = []
    new_price = '2/10'
    username = tests.settings.betplacement_user

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        self.ob_config.grant_freebet(self.username)
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet)
        self.__class__.team1 = event_params.team1
        self.__class__.eventID, self.__class__.selection_id = event_params.event_id, event_params.selection_ids
        self.selection_ids.append(list(self.selection_id.values())[0])
        self.event_names.append(event_params.ss_response['event']['name'])
        if self.site.wait_logged_out():
            for i in range(2):
                self.ob_config.grant_freebet(self.username)
            self.site.login(self.username)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_single_football_selection_to_betslip_and_place_bet_using_money_and_free_bet(self):
        """
        DESCRIPTION: Add Single Football selection to betslip and place bet using money and free bet
        EXPECTED: Overask flow is triggered
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_bet + 0.1
        selections = self.get_betslip_sections().Singles
        selection = selections.get(self.team1, None)
        self.assertTrue(selection, msg=f'Selection "{self.team1}" not found in the Betslip')
        self.assertTrue(selection.has_use_free_bet_link(), msg='"Use Free Bet" link not found')
        try:
            selection.freebet_tooltip.click()
        except VoltronException as e:
            self._logger.info("*** tooltip not found in the second iteration***", e)
        selection.use_free_bet_link.click()
        self.__class__.freebet_stake = self.select_free_bet()
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_counter_by_price_in_ob_ti_tool(self):
        """
        DESCRIPTION: Counter by Price in OB TI tool
        EXPECTED: Counter offer with the new price highlighted and updated potential returns shown to the customer.
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                 betslip_id=betslip_id, price_1=self.new_price, max_bet=self.bet_amount + float(self.freebet_stake))
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask is not closed')
        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        sections = self.get_betslip_sections().Singles
        odd_value = sections.overask_trader_offer.stake_content.odd_value.value.strip(' x')
        self.assertEqual(odd_value, self.new_price,
                         msg=f'Actual price :{odd_value} is not same as'
                             f'Expected price :{self.new_price}')
        self.assertEqual(sections.overask_trader_offer.stake_content.odd_value.value_color,
                         vec.colors.OVERASK_MODIFIED_PRICE_COLOR, msg=f'Modified price for stake is not highlighted in yellow')
        actual_return = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=actual_return,
                                      odds=self.new_price,
                                      bet_amount=self.bet_amount,
                                      freebet_amount=float(self.freebet_stake))

    def test_003_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: Bet receipt is shown to the customer and it shows that a free bet signposting
        EXPECTED: Balance should be updated correctly
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.has_free_bet_icon())
        sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        single_section = sections.get(vec.betslip.BETSLIP_SINGLES_NAME).items_as_ordered_dict
        self.assertTrue(single_section, msg='No Betslip sections found')
        single = list(single_section.values())[0]
        self.verify_estimated_returns(
            est_returns=float(self.site.bet_receipt.footer.total_estimate_returns),
            odds=single.odds, bet_amount=self.bet_amount, freebet_amount=float(self.freebet_stake))

    def test_004_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History.
        """
        self.navigate_to_page('homepage')
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_name=self.event_names[0])
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_names[0],
                                     bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)

    def test_005_if_the_selection_has_cash_out(self):
        """
        DESCRIPTION: If the selection has cash out
        EXPECTED: Message saying "Free bets has a reduced Cash Out value" should be displayed in My Bets
        """
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                                event_name=self.event_names[0])
        self.assertTrue(bet, msg=f'Bet "{bet_name}" is not displayed')
        self.assertTrue(bet.has_cash_out_error_message,
                        msg='Cash Out error message is not displayed')

    def test_006_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        self.selection_ids.clear()
        self.event_names.clear()
        self.test_000_preconditions()
        self.test_001_add_single_football_selection_to_betslip_and_place_bet_using_money_and_free_bet()
        self.test_002_counter_by_price_in_ob_ti_tool()
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_name=self.event_names[0], bet_in_open_bets=False)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_name=self.event_names[0], bet_in_open_bets=False)
