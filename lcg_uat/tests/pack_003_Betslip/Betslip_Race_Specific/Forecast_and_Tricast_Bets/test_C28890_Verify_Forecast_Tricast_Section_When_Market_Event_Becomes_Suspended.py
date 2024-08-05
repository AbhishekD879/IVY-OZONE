import voltron.environments.constants as vec
import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot modify events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.forecast_tricast
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.ob_smoke
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.login
@vtest
class Test_C28890_Verify_Forecast_Tricast_Section_When_Market_Event_Becomes_Suspended(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C28890
    NAME: Verify 'Forecast' / 'Tricast' Section When Market / Event Becomes Suspended
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def check_betslip_error_messages(self):
        sections = self.get_betslip_sections()
        forecast_tricast_section = sections.Singles
        for stake in list(forecast_tricast_section.items()):
            stake_name, stake = stake
            self.assertFalse(stake.amount_form.input.is_enabled(expected_result=False, timeout=15),
                             msg='Stake input should be disabled')

        betslip = self.get_betslip_content()
        self.assertFalse(betslip.bet_now_button.is_enabled(expected_result=False),
                         msg='Bet Now button is not disabled')
        betnow_section_error = betslip.error
        self.assertEqual(betnow_section_error, vec.betslip.SINGLE_DISABLED,
                         msg=f'Actual error "{betnow_section_error}" != Expected '
                         f'error "{vec.betslip.SINGLE_DISABLED}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login with user
        DESCRIPTION: Navigate to Horse racing page
        DESCRIPTION: Open any race event -> Navigate to Forecast/Tricast tab
        DESCRIPTION: Add Forecast/Tricast bets to Betslip
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=3,
                                                          forecast_available=True,
                                                          tricast_available=True)
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.eventID = event_params.event_id
        self.__class__.marketID = event_params.market_id
        self.site.login(username=tests.settings.betplacement_user)
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.place_forecast_tricast_bet_from_event_details_page(sport_name='horse-racing', tricast=True)

    def test_001_open_betslip_with_selections(self):
        """
        DESCRIPTION: Add two selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        self.site.open_betslip()

    def test_002_trigger_the_situation_market_status_code_s_for_market_from_which_outcomes_are_added(self):
        """
        DESCRIPTION: Trigger the situation:
        DESCRIPTION: **marketStatusCode='S'** for market from which outcomes are added
        EXPECTED: Error message appear
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=False)

    def test_003_verify_error_message_appearance(self):
        """
        DESCRIPTION: Verify error message appearance
        EXPECTED: Error message 'The Outcome/Market/Event Has Been Suspended' is shown in above corresponding single
        EXPECTED: Error message 'One or more of your selections are unavailable, please remove them to get new multiples' is shown above 'Bet Now' button
        EXPECTED: Bet is NOT placed
        EXPECTED: NOTE, the text of error message may vary. It depends on what comes from the server
        """
        self.check_betslip_error_messages()

    def test_004_repeat_steps_with_suspended_event(self):
        """
        DESCRIPTION: Repeat steps #3 - 8 with suspended event
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.ob_config.change_event_state(event_id=self.eventID)
        self.check_betslip_error_messages()

    def test_005_repeat_steps_with_started_event(self):
        """
        DESCRIPTION: Repeat steps # 3 with started event
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.ob_config.change_is_off_flag(event_id=self.eventID, is_off=False)
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=False)
        self.check_betslip_error_messages()
