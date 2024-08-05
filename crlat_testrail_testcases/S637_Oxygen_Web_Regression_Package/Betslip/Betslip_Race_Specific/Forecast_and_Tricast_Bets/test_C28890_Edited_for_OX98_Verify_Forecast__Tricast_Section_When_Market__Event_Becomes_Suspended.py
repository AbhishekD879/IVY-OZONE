import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C28890_Edited_for_OX98_Verify_Forecast__Tricast_Section_When_Market__Event_Becomes_Suspended(Common):
    """
    TR_ID: C28890
    NAME: [Edited for OX98] Verify 'Forecast' / 'Tricast' Section When Market / Event Becomes Suspended
    DESCRIPTION: This test case verifies 'Forecast' / 'Tricast' sections when event/market becomes suspended
    DESCRIPTION: NOTE, User Story **BMA-3607**
    DESCRIPTION: AUTOTEST [C10581700]
    PRECONDITIONS: Login with user
    PRECONDITIONS: Navigate to Horse racing page
    PRECONDITIONS: Open any rase event -> Navigate to Forecast/Tricast tab
    PRECONDITIONS: Add Forecast/Tricast/Reverse Forecast/Combinations Forecast and Tricast bets to Betslip
    PRECONDITIONS: **For earlier releases than OX98: For Forecast/Tricast bet - Add two or more selections from the same market to the Bet Slip**
    """
    keep_browser_open = True

    def test_001_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_002_trigger_the_situationmarketstatuscodes_for_market_from_which_outcomes_are_added(self):
        """
        DESCRIPTION: Trigger the situation:
        DESCRIPTION: **marketStatusCode='S'** for market from which outcomes are added
        EXPECTED: Error message appear
        """
        pass

    def test_003_enter_stake_in_a_stake_field_for_forecasttricastreverse_forecastcombinations_forecast_and_tricast__bets_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in a stake field for Forecast/Tricast/Reverse Forecast/Combinations Forecast and Tricast  bets and tap 'Bet Now' button
        EXPECTED: *   Error message 'The Outcome/Market/Event Has Been Suspended' is shown in above corresponding single
        EXPECTED: *   Error message 'One or more of your selections are unavailable, please remove them to get new multiples' is shown above 'Bet Now' button
        EXPECTED: *   Bet is NOT placed
        EXPECTED: NOTE, the text of error message may vary. It depends on what comes from the server
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_004_refresh_the_page_for_earlier_releases_than_ox98(self):
        """
        DESCRIPTION: Refresh the page (**For earlier releases than OX98**)
        EXPECTED: 'Forecast / Tricast (n)' section disappear from the Bet Slip
        """
        pass

    def test_005_unsuspend_the_suspended_market_and_refresh_the_page_for_earlier_releases_than_ox98(self):
        """
        DESCRIPTION: Unsuspend the suspended market and refresh the page (**For earlier releases than OX98**)
        EXPECTED: 'Forecast / Tricast (n)' section appear
        """
        pass

    def test_006_repeat_steps_2_5_with_suspended_event(self):
        """
        DESCRIPTION: Repeat steps #2-5 with suspended event
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps__2_5_with_started_event(self):
        """
        DESCRIPTION: Repeat steps # 2-5 with started event
        EXPECTED: 
        """
        pass
