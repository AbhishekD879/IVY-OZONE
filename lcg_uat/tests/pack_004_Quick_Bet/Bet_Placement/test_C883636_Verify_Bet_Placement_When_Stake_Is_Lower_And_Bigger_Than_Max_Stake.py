import pytest
from selenium.webdriver import ActionChains

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.pages.shared import get_driver


@pytest.mark.quick_bet
@pytest.mark.event_details
@pytest.mark.bet_placement
@pytest.mark.mobile_only
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C883636_Verify_Bet_Placement_When_Stake_Is_Bigger_Than_Max_Stake(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C883636
    VOL_ID: C9698275
    NAME: Verify Bet Placement when Stake is bigger than Max Stake
    DESCRIPTION: This test case verifies Bet Placement within Quick Bet when Stake is bigger than Max Stake
    """
    keep_browser_open = True
    max_bet = 5.00
    stake_delta = 1.00

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event and grant freebets for the user
        """
        username = tests.settings.disabled_overask_user
        self.__class__.event_id = self.ob_config.add_autotest_premier_league_football_event(
            max_bet=self.max_bet).event_id
        self.__class__.event_id_2 = self.ob_config.add_autotest_premier_league_football_event(
            max_bet=self.max_bet).event_id

        market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

        self.ob_config.grant_freebet(username=username, freebet_value=self.max_bet)
        self.ob_config.grant_freebet(username=username, freebet_value=self.max_bet - self.stake_delta)

        self.__class__.free_bet_name_max_bet = self.get_freebet_name(value='{:.2f}'.format(self.max_bet))
        self.__class__.free_bet_name_under_max_bet = self.get_freebet_name(value='{:.2f}'.format(self.max_bet - self.stake_delta))

        self.site.login(username=username)

    def test_001_tap_one_sport_selection(self):
        """
        DESCRIPTION: Tap one <Sport> selection
        EXPECTED: Selected price/odds are highlighted in green
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        self.navigate_to_edp(event_id=self.event_id)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

        self.__class__.user_balance = self.site.header.user_balance

    def test_002_enter_bigger_than_max_stake_value(self):
        """
        DESCRIPTION: Enter value which is bigger than maxStake allowed in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        """
        quick_bet = self.site.quick_bet_panel.selection
        bigger_stake = self.max_bet + self.stake_delta
        quick_bet.content.amount_form.input.value = bigger_stake
        amount = float(quick_bet.content.amount_form.input.value)
        self.assertEqual(amount, bigger_stake,
                         msg=f'Entered amount "{amount}" is not equal to expected "{bigger_stake}"')

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: 'Sorry, the maximum stake for the bet is <currency> <amount>' error message is displayed below 'QUICK BET' header
        EXPECTED: Bet is NOT placed
        """
        place_bet_button = self.site.quick_bet_panel.place_bet
        self.assertTrue(place_bet_button.is_enabled(), msg='"Place Bet" button is not enabled')

        place_bet_button.click()

        message = self.site.quick_bet_panel.info_panels.text
        expected_big_stake_message = vec.quickbet.BET_PLACEMENT_ERRORS.stake_high.format(self.max_bet)
        self.assertEqual(message, expected_big_stake_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_big_stake_message}"')

        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed(expected_result=False)
        self.assertFalse(bet_receipt_displayed, msg='Bet Receipt is shown')
        self.verify_user_balance(expected_user_balance=self.user_balance)

    def test_004_verify_amount_value_displayed_on_error_message(self):
        """
        DESCRIPTION: Verify 'amount' value displayed on error message
        EXPECTED: 'amount' value corresponds to data.error.stake.maxAllowed attribute from 31012 response from WS
        """
        max_bet_ws = self.get_web_socket_response_by_id(response_id=31012, delimiter='42')['data']['error']['stake']['maxAllowed']
        self.assertEqual(max_bet_ws, "{:.2f}".format(self.max_bet),
                         msg=f'Value in the WS {max_bet_ws} is not the same as expected {"{:.2f}".format(self.max_bet)}')

    def test_005_verify_warning_message_presence(self):
        """
        DESCRIPTION: Verify warning message presence
        EXPECTED: Warning message does not disappear after tapping out of its area
        """
        ActionChains(get_driver()).move_by_offset(30, 30).click().perform()

        message = self.site.quick_bet_panel.info_panels.text
        expected_big_stake_message = vec.quickbet.BET_PLACEMENT_ERRORS.stake_high.format(self.max_bet)
        self.assertEqual(message, expected_big_stake_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_big_stake_message}"')

    def test_006_remove_value_from_stake_and_select_free_bet_from_pop_up(self):
        """
        DESCRIPTION: Remove value from 'Stake' field and select free bet from pop up
        DESCRIPTION: with the same amount that is equal to 'maxAllowed' value returned from response
        EXPECTED: 'Stake' field is empty
        EXPECTED: Free bet is chosen
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.amount_form.input.value = ''
        self.assertEqual(quick_bet.amount_form.input.value, '',
                         msg=f'Actual amount "{quick_bet.amount_form.input.value}" does not match expected " "')

        quick_bet.use_free_bet_link.click()
        self.select_free_bet(free_bet_name=self.free_bet_name_max_bet)
        self.assertTrue(quick_bet.has_remove_free_bet_link(), msg='Free bet was not selected')

    def test_007_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: Bet is placed successfully
        EXPECTED: Bet Receipt is displayed
        """
        place_bet_button = self.site.quick_bet_panel.place_bet
        self.assertTrue(place_bet_button.is_enabled(), msg='"Place Bet" button is not enabled')

        place_bet_button.click()

        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')

    def test_008_repeat_steps_6_8(self):
        """
        DESCRIPTION: Repeat steps #6-8 but on step 6 enter stake and choose free bet in that way that their
        DESCRIPTION: sum is equal or less than 'maxAllowed' value returned from the response
        """
        self.site.quick_bet_panel.close()
        self.navigate_to_edp(event_id=self.event_id_2)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

        quick_bet = self.site.quick_bet_panel.selection.content

        quick_bet.amount_form.input.value = self.stake_delta
        amount = float(quick_bet.amount_form.input.value)
        self.assertEqual(amount, self.stake_delta,
                         msg=f'Entered amount "{amount}" is not equal to expected "{self.stake_delta}"')

        quick_bet.use_free_bet_link.click()
        self.select_free_bet(free_bet_name=self.free_bet_name_under_max_bet)
        self.assertTrue(quick_bet.has_remove_free_bet_link(), msg='Free bet was not selected')

        self.test_007_tap_place_bet_button()
