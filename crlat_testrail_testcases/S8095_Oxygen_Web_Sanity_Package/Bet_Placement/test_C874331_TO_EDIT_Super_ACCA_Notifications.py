import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C874331_TO_EDIT_Super_ACCA_Notifications(Common):
    """
    TR_ID: C874331
    NAME: [TO EDIT] Super ACCA Notifications
    DESCRIPTION: This test case verifies Super ACCA Notification message is displayed for logged in user
    DESCRIPTION: AUTOTESTS [C9690099] [C9690100] [C9690101] [C9690102] [C9697973]
    PRECONDITIONS: There are events with available ACCA Offers.
    PRECONDITIONS: For configuration of ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: To verify ACCA Offer details please check requests: BuildBet -> Bets-> Bet Offer
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Appearing Suggested or Eligible Super ACCA notification depends on set 'Bet Type' value (DBL, TBL, ACC4, etc.) during Settle Lose/Win ACCA offer configuration.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: - Home page is opened
        """
        pass

    def test_002_add_one_selection_to_betslip_from_three_different_events_to_trigger_super_acca_and_open_betslip(self):
        """
        DESCRIPTION: Add one selection to Betslip from three different events (to trigger Super ACCA) and open Betslip
        EXPECTED: - Betslip is opened and contains 'Place your ACCA (3 selections)' section expanded by default
        EXPECTED: - Super ACCA Notification message doesn't appear
        """
        pass

    def test_003_log_in_with_user_account_with_positive_balance_and_open_betslip(self):
        """
        DESCRIPTION: Log in with user account with positive balance and open Betslip
        EXPECTED: - 'Place your ACCA (3 selections)' section expanded by default
        EXPECTED: - Super ACCA Notification message appears under Section on blue background and one selection is required for super ACCA offer
        """
        pass

    def test_004_add_one_more_selection_to_betslip_from_other_event_to_trigger_super_acca_and_open_betslip(self):
        """
        DESCRIPTION: Add one more selection to Betslip from OTHER event (to trigger Super ACCA) and open Betslip
        EXPECTED: - 'Place your ACCA (4 selections)' section expanded by default
        EXPECTED: - Super ACCA Notification message appears under Section on yellow background and message is changed
        """
        pass

    def test_005_add_one_more_selection_to_betslip_from_other_event_to_trigger_super_acca_and_open_betslip(self):
        """
        DESCRIPTION: Add one more selection to Betslip from OTHER event (to trigger Super ACCA) and open Betslip
        EXPECTED: - 'Place your ACCA (5 selections)' section expanded by default
        EXPECTED: - Super ACCA Notification message remainss under Section on yellow background and message is same as before
        """
        pass

    def test_006_remove_any_two_of_selections(self):
        """
        DESCRIPTION: Remove any two of selections
        EXPECTED: - 'Place your ACCA (3 selections)' section expanded by default
        EXPECTED: - Super ACCA Notification message appears under Section on blue background, message is changed and one selection is required for super ACCA offer
        """
        pass
