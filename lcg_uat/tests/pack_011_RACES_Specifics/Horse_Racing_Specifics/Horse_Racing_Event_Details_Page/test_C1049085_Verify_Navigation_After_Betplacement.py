import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_beta2
@pytest.mark.user_journey_single_horse_race
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.bet_placement
@pytest.mark.quick_bet
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.races
@pytest.mark.login
@vtest
class Test_C1049085_Verify_Navigation_After_Betplacement(BaseRacing):
    """
    TR_ID: C1049085
    VOL_ID: C9698409
    NAME: Verify Navigation After Betplacement
    DESCRIPTION: This test case verifies navigation after bet placement when user selects outcome from event details page
    PRECONDITIONS: User should be logged in to place a bet.
    """
    keep_browser_open = True
    bet_amount = 0.1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Preconditions
        DESCRIPTION: TST2: Create racing event in TI
        DESCRIPTION: Prod: Find event in SS
        DESCRIPTION: Log In
        """
        if tests.settings.backend_env != 'prod':
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=3)
            self.__class__.eventID = event_params.event_id
        else:
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         all_available_events=True)
            event = next((event for event in events if
                          event.get('event') and event['event'] and event['event'].get('children')), None)

            self.__class__.eventID = event.get('event').get('id')
        self._logger.info(f'*** Found Horse racing event with id "{self.eventID}"')
        self.site.login()

    def test_001_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        self.__class__.balance = self.site.header.user_balance
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        self.site.wait_content_state_changed(timeout=3)

    def test_002_add_selection_to_the_quick_bet_betslip__enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Add selection to the Quick Bet/BetSlip > Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: * Bet is successfully placed
        EXPECTED: * 'Quick Bet'/Betslip is replaced with 'Bet Receipt' view, displaying bet information
        EXPECTED: * Balance is decreased accordingly
        """
        self.add_selection_to_quick_bet()
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.amount_form.input.clear()
        quick_bet.amount_form.input.value = self.bet_amount
        actual = float(quick_bet.amount_form.input.value)
        expected = float(self.bet_amount)
        self.assertEqual(actual, expected, msg=f'Actual amount "{actual}" does not match expected "{expected}"')
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')

        self.verify_user_balance(self.balance - self.bet_amount)

    def test_003_tap_done_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Tap 'Done' button on Bet Receipt page
        EXPECTED: * Bet Slip Slider closes
        EXPECTED: * User stays on same page
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_content_state(state_name='RacingEventDetails')
