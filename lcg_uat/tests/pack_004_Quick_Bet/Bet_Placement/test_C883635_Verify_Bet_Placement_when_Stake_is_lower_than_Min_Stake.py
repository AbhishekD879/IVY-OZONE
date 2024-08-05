import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.event_details
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C883635_Verify_Bet_Placement_when_Stake_is_lower_than_Min_Stake(BaseSportTest, BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C883635
    VOL_ID: C16280355
    NAME: Verify Bet Placement when Stake is lower than Min Stake
    DESCRIPTION: This test case verifies Bet Placement when Stake is lower than Min Stake
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: User is logged in and has positive balance
    PRECONDITIONS: 'MinStake' value can be viewed or changed on selection level in OpenBet Ti tool
    """
    keep_browser_open = True
    min_bet = 0.1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login into application
        """
        quick_bet_config = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet_config:
            quick_bet_config = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet_config.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')

        event = self.ob_config.add_autotest_premier_league_football_event(min_bet=self.min_bet)
        self.__class__.event_id, self.__class__.selection_ids = event.event_id, event.selection_ids
        self.__class__.racing_event_id = self.ob_config.add_UK_racing_event(min_bet=self.min_bet,
                                                                            number_of_runners=2).event_id
        market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|',
                                                                                                                '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)
        for selection in self.selection_ids.values():
            self.ob_config.change_selection_state(selection_id=selection, displayed=True, active=True,
                                                  fixed_stake_limits=True)

        self.site.login(username=tests.settings.disabled_overask_user)

    def test_001_tap_one_sport_selection(self):
        """
        DESCRIPTION: Tap one <Sport> selection
        EXPECTED: Selected price/odds are highlighted in green
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        self.navigate_to_edp(event_id=self.event_id)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

        self.__class__.user_balance = self.site.header.user_balance

    def test_002_enter_lower_than_min_stake_value(self):
        """
        DESCRIPTION: Enter value which is lower than minStake allowed in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        """
        quick_bet = self.site.quick_bet_panel.selection
        lower_stake = float(self.min_bet) / 2.0
        quick_bet.content.amount_form.input.value = lower_stake
        amount = float(quick_bet.content.amount_form.input.value)
        self.assertEqual(amount, lower_stake,
                         msg=f'Entered amount "{amount}" is not equal to expected "{lower_stake}"')

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: 'Stake is too low' error message is displayed below 'QUICK BET' header
        EXPECTED: Bet is NOT placed
        """
        place_bet_button = self.site.quick_bet_panel.place_bet
        self.assertTrue(place_bet_button.is_enabled(), msg='"Place Bet" button is not enabled')

        place_bet_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_bet_info_panel(), msg='Info panel is not shown')

        message = self.site.quick_bet_panel.info_panels.text
        expected_msg = vec.quickbet.BET_PLACEMENT_ERRORS.stake_low.format(self.min_bet)
        self.assertEqual(message, expected_msg,
                         msg=f'Actual message "{message}" does not match expected "{expected_msg}"')

        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed(expected_result=False)
        self.assertFalse(bet_receipt_displayed, msg='Bet Receipt is shown')

        self.verify_user_balance(expected_user_balance=self.user_balance)

    def test_004_tap_x_button(self):
        """
        DESCRIPTION: Tap 'X' button
        EXPECTED: Quick bet is closed
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick bet not closed')

    def test_005_add_race_selection_to_quick_bet_and_repeat_steps_3_5(self):
        """
        DESCRIPTION: Add <Race> selection to Quick Bet and repeat steps #3-5
        """
        counter_value = int(self.site.header.bet_slip_counter.counter_value)
        if counter_value > 0:
            self.site.header.bet_slip_counter.click()
            self.clear_betslip()
            self.device.go_back()
        self.navigate_to_edp(event_id=self.racing_event_id, sport_name='horse-racing')
        self.site.wait_content_state_changed()
        self.add_selection_to_quick_bet()

        self.__class__.user_balance = self.site.header.user_balance

        self.test_002_enter_lower_than_min_stake_value()
        self.test_003_tap_place_bet_button()
        self.test_004_tap_x_button()
