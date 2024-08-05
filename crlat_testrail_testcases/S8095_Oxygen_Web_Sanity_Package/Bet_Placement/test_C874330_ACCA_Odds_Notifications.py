import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C874330_ACCA_Odds_Notifications(Common):
    """
    TR_ID: C874330
    NAME: ACCA Odds Notifications
    DESCRIPTION: This test case verifies ACCA Odds Notification displaying after adding selections to the Betslip
    DESCRIPTION: AUTOTESTS [C48981671]
    PRECONDITIONS: This case is not required for tablet, desktop BMA-42942
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_go_to_any_sports_landing_page(self):
        """
        DESCRIPTION: Go to any Sports Landing page
        EXPECTED: Sports Landing page is opened
        """
        pass

    def test_003_add_at_least_two_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip
        EXPECTED: ACCA Odds Notification appears:
        EXPECTED: * at the bottom of the screen but above Footer menu for Mobile
        """
        pass

    def test_004_verify_acca_odds_notification_content(self):
        """
        DESCRIPTION: Verify ACCA Odds Notification content
        EXPECTED: ACCA Odds Notification contains the following information:
        EXPECTED: *  **CORAL** Multiples name (Double, Treble, Accumulator (4), etc.) and Odds are displayed
        EXPECTED: * **LADBROKES** Multiples name (Double, Treble, Accumulator (4), etc.), Shows return to X stake (e.g. £X pays £Y.YY) and Odds are displayed
        EXPECTED: * The odds are displayed in fractional format as default for logged OUT in user
        EXPECTED: * The odds are displayed in appropriate format depending on user preference i.e. decimal/ fractional for logged IN user
        EXPECTED: * An arrow is displayed to the right of the message bar for mobile only
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/113614769)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/113614770)
        """
        pass

    def test_005_verify_that_potential_payout(self):
        """
        DESCRIPTION: Verify that potential payout
        EXPECTED: Payout parameter from the buildBet response is displayed on ACCA Odds Notification message as Odds
        """
        pass

    def test_006_clicktap_on_acca_odds_notification_message(self):
        """
        DESCRIPTION: Click/Tap on ACCA Odds Notification message
        EXPECTED: User is redirected to the Betslip
        EXPECTED: User is focused directly on the relevant input field
        """
        pass

    def test_007_repeat_steps_2_6_for_races_lp_price_type_only(self):
        """
        DESCRIPTION: Repeat steps 2-6 for Races (LP price type only)
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_3_6_on_homepage(self):
        """
        DESCRIPTION: Repeat steps 3-6 on Homepage
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_3_6_on_in_play_page(self):
        """
        DESCRIPTION: Repeat steps 3-6 on In-Play page
        EXPECTED: 
        """
        pass
