import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C15500642_Vanilla_Logged_out_user_Verify_Quick_Bet_for_not_Logged_In(Common):
    """
    TR_ID: C15500642
    NAME: [Vanilla] [Logged out user] Verify Quick Bet for not Logged In
    DESCRIPTION: This test case verifies Quick Bet for not Logged in
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: User should be logged out
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_sport_race_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/ <Race> selection to Quick Bet
        EXPECTED: Quick Bet is displayed at the bottom of the page
        EXPECTED: Added selection and all data are displayed in Quick Bet
        """
        pass

    def test_003_verify_quick_bet_displaying(self):
        """
        DESCRIPTION: Verify Quick Bet displaying
        EXPECTED: Quick Bet consists of:
        EXPECTED: 'Quick Bet' header and 'X' icon
        EXPECTED: Added selection`s details
        EXPECTED: 'Odds' label and field
        EXPECTED: 'Stake' field
        EXPECTED: 'Each Way' label and checkbox (if available)
        EXPECTED: 'Quick Stakes' buttons
        EXPECTED: 'Stake' and 'Est. Returns' labels and corresponding values
        EXPECTED: 'ADD TO BETSLIP' and 'LOGIN & PLACE BET' button
        EXPECTED: ![](index.php?/attachments/get/31343)
        """
        pass
