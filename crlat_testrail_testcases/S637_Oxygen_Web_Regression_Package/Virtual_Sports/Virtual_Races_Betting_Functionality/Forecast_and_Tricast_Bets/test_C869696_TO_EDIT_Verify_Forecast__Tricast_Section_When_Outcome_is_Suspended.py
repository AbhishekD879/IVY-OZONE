import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.virtual_sports
@vtest
class Test_C869696_TO_EDIT_Verify_Forecast__Tricast_Section_When_Outcome_is_Suspended(Common):
    """
    TR_ID: C869696
    NAME: [TO EDIT] Verify 'Forecast' / 'Tricast' Section When Outcome is Suspended
    DESCRIPTION: **TO EDIT:** Betslip was redesigned and everything described in this test case and related to the betslip should be reviewed.
    DESCRIPTION: This test case verifies 'Forecast' / 'Tricast' sections when outcome becomes suspended for
    DESCRIPTION: *   Virtual Motorsports (Class ID 288)
    DESCRIPTION: *   Virtual Cycling (Class ID 290)
    DESCRIPTION: *   Virtul Horse Racing (Class ID 285)
    DESCRIPTION: *   Virtual Greyhound Racing (Class ID 286)
    DESCRIPTION: *   Virtual Grand National (Class ID 26604)
    DESCRIPTION: **JIRA Ticket** :
    DESCRIPTION: BMA-9397 'Extend Forecast and Tricast betting to Virtual Sports'**7**
    PRECONDITIONS: User is logged in
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: Need to update according to the new design in BMA-43681, BMA-42906.
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_the_virtual_racing_event_details_page(self):
        """
        DESCRIPTION: Go to the <Virtual Racing> event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_add_two_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_004_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_005_suspend_one_of_the_outcomes_in_the_backoffice_ti(self):
        """
        DESCRIPTION: Suspend one of the outcomes in the Backoffice TI
        EXPECTED: Error message appears above suspended outcome
        """
        pass

    def test_006_enter_stake_in_a_stake_field_for_forecast__tricast_bet_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in a stake field for forecast / tricast bet and tap 'Bet Now' button
        EXPECTED: *   Error message 'The Outcome/Market/Event Has Been Suspended' is shown in above corresponding single
        EXPECTED: *   Error message 'One or more of your selections are unavailable, please remove them to get new multiples' is shown above 'Bet Now' button
        EXPECTED: *   Bet is NOT placed
        EXPECTED: NOTE, the text of error message may vary. It depends on what comes from the server
        """
        pass

    def test_007_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: 'Forecast / Tricast (n)' section disappear from the Bet Slip
        """
        pass

    def test_008_unsuspend_the_suspended_outcome(self):
        """
        DESCRIPTION: Unsuspend the suspended outcome
        EXPECTED: Error message will disappear near the suspended selection
        EXPECTED: 'Forecast / Tricast (n)' section appear ONLY after the page refresh
        """
        pass

    def test_009_repeat_steps__5___7(self):
        """
        DESCRIPTION: Repeat steps # 5 - 7
        EXPECTED: 
        """
        pass

    def test_010_delete_suspended_outcome_via_x_icon(self):
        """
        DESCRIPTION: Delete suspended outcome via [X] icon
        EXPECTED: Suspended outcome is deleted
        EXPECTED: Bet Slip is auto refreshed
        EXPECTED: 'Forecast / Tricast (n)' section appears immediately
        EXPECTED: 'Forecast / Tricast (n)' will be rebuilt with quantity of active selections
        """
        pass
