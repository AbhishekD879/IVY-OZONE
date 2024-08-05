from time import sleep

import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # overask
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.footer
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.login
@pytest.mark.high
@pytest.mark.overask
@pytest.mark.mobile_only
@vtest
class Test_C18753268_Verify_My_Bets_counter_during_Overask(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C18753268
    VOL_ID: C58665521
    NAME: Verify My Bets counter during Overask
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after Overask was triggered and Bet was placed/ not placed
    PRECONDITIONS: - Load Oxygen/Roxanne Application and login
    PRECONDITIONS: - Overask is enabled for logged in user
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: - OB TI tool:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True
    max_bet = 0.05

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        """
        self.check_my_bets_counter_enabled_in_cms()
        event_params = self.ob_config.add_UK_racing_event(max_bet=self.max_bet, number_of_runners=1)
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.eventID = event_params.event_id
        self.__class__.username = tests.settings.overask_enabled_user

        self.site.login(username=self.username)

        if '+' in self.get_my_bets_counter_value_from_footer():
            self.__class__.initial_counter = int(self.get_my_bets_counter_value_from_footer().strip('+'))
        else:
            self.__class__.initial_counter = int(self.get_my_bets_counter_value_from_footer())

    def test_001__add_selection_to_quick_betbetslip_trigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: * Add selection to Quick bet/Betslip
        DESCRIPTION: * Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 1
        self.place_single_bet()
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')

    def test_002__close_betslip_or_refresh_the_page_check_my_bets_counter(self):
        """
        DESCRIPTION: * Close betslip or refresh the page
        DESCRIPTION: * Check My bets counter
        EXPECTED: My bets counter remains the same
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='Homepage', timeout=10)
        if '+' in self.get_my_bets_counter_value_from_footer():
            counter_value = int(self.get_my_bets_counter_value_from_footer().strip('+'))
        else:
            counter_value = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(counter_value, self.initial_counter,
                         msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter}"')

    def test_003_accept_the_bet_in_ob_ti_tool_and_check_bet_is_placed_on_coralladbrokes(self):
        """
        DESCRIPTION: Accept the bet in OB TI tool and check bet is placed on Coral/Ladbrokes
        EXPECTED: * Bet is placed and bet receipt is displayed
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')

        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)

        self.check_bet_receipt_is_displayed()

    def test_004__close_betslip_check_my_bets_counter(self):
        """
        DESCRIPTION: * Close betslip
        DESCRIPTION: * Check My bets counter
        EXPECTED: My bets counter is increased by one
        """
        self.site.bet_receipt.footer.click_done()
        sleep(1)
        if '+' in self.get_my_bets_counter_value_from_footer():
            counter_value = int(self.get_my_bets_counter_value_from_footer().strip('+'))
            self.assertEqual(counter_value, self.initial_counter,
                             msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter + 1}"')
        else:
            counter_value = int(self.get_my_bets_counter_value_from_footer())
            self.assertEqual(counter_value, self.initial_counter + 1,
                             msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter + 1}"')

    def test_005_repeat_step_1_2_and_decline_the_bet_in_ob_ti_toolcheck_bet_is_not_placed_on_coralladbrokes(self):
        """
        DESCRIPTION: Repeat step #1-2 and Decline the bet in OB TI tool
        DESCRIPTION: check bet is NOT placed on Coral/Ladbrokes
        EXPECTED: * Bet is NOT placed
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')

        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.decline_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)

        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        _, section = list(betreceipt_sections.items())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message

        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual overask warning message: "{overask_warning_message}" is not equal '
                             f'to expected: "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')

    def test_006__close_betslip_check_my_bets_counter(self):
        """
        DESCRIPTION: * Close betslip
        DESCRIPTION: * Check My bets counter
        EXPECTED: My bets counter remains the same
        """
        self.site.bet_receipt.footer.click_done()
        sleep(1)
        if '+' in self.get_my_bets_counter_value_from_footer():
            counter_value = int(self.get_my_bets_counter_value_from_footer().strip('+'))
            self.assertEqual(counter_value, self.initial_counter,
                             msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter}"')
        else:
            counter_value = int(self.get_my_bets_counter_value_from_footer())
            self.assertEqual(counter_value, self.initial_counter + 1,
                             msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter + 1}"')

    def test_007_repeat_step_1_2_and_make_an_offer_in_ob_ti_tool(self):
        """
        DESCRIPTION: Repeat step #1-2 and make an offer in OB TI tool
        EXPECTED: Bet is NOT placed and offer is shown to user
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')

        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.max_bet,
                                       price_type='S')

    def test_008__close_betslip_check_my_bets_counter(self):
        """
        DESCRIPTION: * Close betslip
        DESCRIPTION: * Check My bets counter
        EXPECTED: My bets counter remains the same
        """
        self.site.close_betslip()
        sleep(1)
        if '+' in self.get_my_bets_counter_value_from_footer():
            counter_value = int(self.get_my_bets_counter_value_from_footer().strip('+'))
            self.assertEqual(counter_value, self.initial_counter,
                             msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter}"')
        else:
            counter_value = int(self.get_my_bets_counter_value_from_footer())
            self.assertEqual(counter_value, self.initial_counter + 1,
                             msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter + 1}"')

    def test_009__open_betslip_and_confirm_the_offer_reject_the_offer_check_my_bets_counter(self):
        """
        DESCRIPTION: * Open betslip and confirm the offer/ reject the offer
        DESCRIPTION: * Check My bets counter
        EXPECTED: * My bets counter is increased by one if offer was accepted
        EXPECTED: * My bets counter remains the same if offer was rejected
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)

        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=5),
                         msg='Betslip widget was not closed')
        sleep(1)

        if '+' in self.get_my_bets_counter_value_from_footer():
            counter_value = int(self.get_my_bets_counter_value_from_footer().strip('+'))
            self.assertEqual(counter_value, self.initial_counter,
                             msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter}"')
        else:
            counter_value = int(self.get_my_bets_counter_value_from_footer())
            self.assertEqual(counter_value, self.initial_counter + 1,
                             msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter + 1}"')

        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')

        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')

        self.__class__.suggested_max_bet = 0.03
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.max_bet,
                                       price_type='S')

        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message,
            name='Overask trader message to appear', timeout=10)
        self.assertTrue(overask_trader_message, msg=f'Overask trader message has not appeared')

        self.get_betslip_content().confirm_overask_offer_button.click()

        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        sleep(1)

        if '+' in self.get_my_bets_counter_value_from_footer():
            counter_value = int(self.get_my_bets_counter_value_from_footer().strip('+'))
            self.assertEqual(counter_value, self.initial_counter,
                             msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter}"')
        else:
            counter_value = int(self.get_my_bets_counter_value_from_footer())
            self.assertEqual(counter_value, self.initial_counter + 2,
                             msg=f'My bets counter "{counter_value}" is not the same as expected "{self.initial_counter + 2}"')
