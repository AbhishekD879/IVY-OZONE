import pytest
import tests
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C59898496_Verify_potential_returns_after_single_E_W_bet_is_changed_to_Win_Only_and_counter_offer_is_accepted(BaseBetSlipTest):
    """
    TR_ID: C59898496
    NAME: Verify potential returns after single E/W bet is changed to Win Only and counter offer is accepted
    """
    keep_browser_open = True
    max_bet = 1
    suggested_max_bet = 0.25
    prices = {0: '1/12'}
    selection_ids = []
    event_names = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an HR event
        EXPECTED: HR Event is created
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices, max_bet=self.max_bet)
        self.__class__.eventID = event_params.event_id
        self.event_names.append(event_params.ss_response['event']['name'])
        self.selection_ids.append(list(event_params.selection_ids.values())[0])
        if self.site.wait_logged_out():
            self.__class__.username = tests.settings.betplacement_user
            self.site.login(self.username)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_hr_selection_to_quick_betbetsliptrigger_overask__select_ew_checkbox_and_try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add HR selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( Select E/W checkbox and try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_bet + 0.4
        self.place_single_bet(number_of_stakes=1, each_way=True)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_counter_the_bet_from_ew_to_win_only_in_ob_ti_tool(self):
        """
        DESCRIPTION: Counter the bet from EW to Win Only in OB TI tool
        EXPECTED: Counter offer with the Win Only is displayed and updated potential returns shown to the customer
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.change_bet_to_each_way_or_win(account_id=account_id, bet_id=bet_id, betslip_id=betslip_id,
                                                         bet_amount=self.suggested_max_bet, leg_type='W')
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
        self.__class__.sections = self.get_betslip_sections().Singles
        self.assertEqual(self.sections.overask_trader_offer.stake_content.win_only_sign_post, vec.betslip.WIN_ONLY,
                         msg=f'Actual signposting: {self.sections.overask_trader_offer.stake_content.win_only_sign_post} is not same as '
                             f'Expected signposting: {vec.betslip.WIN_ONLY}')
        est_returns = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=est_returns, bet_amount=self.suggested_max_bet, odds=self.prices.values())

    def test_003_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt
        EXPECTED: Balance should be updated correctly
        """
        actual_stake = self.sections.overask_trader_offer.stake_content.stake_value.value.strip('£')
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.device.refresh_page()
        expected_user_balance = self.user_balance - float(actual_stake)
        self.verify_user_balance(expected_user_balance=expected_user_balance)

    def test_004_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History.
        """
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_name=self.event_names[0])
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_name=self.event_names[0])

    def test_005_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        self.selection_ids.clear()
        self.event_names.clear()
        self.test_000_preconditions()
        self.test_001_add_hr_selection_to_quick_betbetsliptrigger_overask__select_ew_checkbox_and_try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_counter_the_bet_from_ew_to_win_only_in_ob_ti_tool()
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_name=self.event_names[0], bet_in_open_bets=False)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_name=self.event_names[0], bet_in_open_bets=False)
