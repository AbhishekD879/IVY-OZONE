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
class Test_C2496171_Floating_Bet_slip__ACCA_Odds_Notification_displaying(Common):
    """
    TR_ID: C2496171
    NAME: Floating Bet slip - ACCA Odds Notification displaying
    DESCRIPTION: This test case verifies ACCA Odds Notification displaying when Bet Slip widget is anchored to the top of the page.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Bet Slip widget is located at the top of the last column
    PRECONDITIONS: 3. Bet Slip widget is expanded by default  (CMS configurable: Widgets->Betslip->'Show Expanded' checkbox)
    PRECONDITIONS: 4. 'Bet slip unlocked' icon is displayed in the header of the bet slip
    """
    keep_browser_open = True

    def test_001_add_at_least_two_selections_from_different_events_to_the_betslip_for_triggering_acca_odds_notification_displaying(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip for triggering ACCA Odds Notification displaying
        EXPECTED: ACCA Odds Notification appears above the Betslip
        """
        pass

    def test_002_click_on_bet_slip_unlocked_icon(self):
        """
        DESCRIPTION: Click on 'Bet slip unlocked' icon
        EXPECTED: 'Bet slip unlocked' icon changes to 'Bet slip locked' icon
        """
        pass

    def test_003_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * Bet Slip widget and ACCA Odds Notification are anchored to the top of the page
        EXPECTED: * Bet Slip widget and ACCA Odds Notification remain visible while scrolling
        EXPECTED: * Bet Slip widget and ACCA Odds Notification overlay 'Favorites' and 'Offer' widgets if available
        """
        pass

    def test_004_navigate_to_any_other_page_within_an_application(self):
        """
        DESCRIPTION: Navigate to any other page within an application
        EXPECTED: 'Bet slip locked' icon remains displayed
        """
        pass

    def test_005_click_on_bet_slip_locked_icon(self):
        """
        DESCRIPTION: Click on 'Bet slip locked' icon
        EXPECTED: * 'Bet slip locked' icon changes to 'Bet slip unlocked' icon
        EXPECTED: * Bet Slip widget and ACCA Odds Notification appear at the top of the last column above any other available modules
        """
        pass

    def test_006_clear_the_bet_slip_from_all_added_selections(self):
        """
        DESCRIPTION: Clear the Bet slip from all added selections
        EXPECTED: * Bet slip is cleared
        EXPECTED: * 'You have no selections in the slip' message is displayed
        """
        pass

    def test_007_click_on_bet_slip_unlocked_icon(self):
        """
        DESCRIPTION: Click on 'Bet slip unlocked' icon
        EXPECTED: 'Bet slip unlocked' icon changes to 'Bet slip locked' icon
        """
        pass

    def test_008_scroll_the_page_down_again(self):
        """
        DESCRIPTION: Scroll the page down again
        EXPECTED: * Bet Slip widget is anchored to the top of the page
        EXPECTED: * Bet Slip widget remains visible while scrolling
        EXPECTED: * Bet Slip widget overlays 'Favorites' and 'Offer' widgets if available
        EXPECTED: * Bet Slip widget stops before footer area
        """
        pass

    def test_009_add_at_least_two_selections_from_different_events_to_the_betslip_for_triggering_acca_odds_notification_displaying(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip for triggering ACCA Odds Notification displaying
        EXPECTED: ACCA Odds Notification appears above the Betslip
        """
        pass

    def test_010_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: * Bet Slip widget and ACCA Odds Notification are anchored to the top of the page
        EXPECTED: * Bet Slip widget and ACCA Odds Notification remain visible while scrolling
        EXPECTED: * Bet Slip widget and ACCA Odds Notification overlay 'Favorites' and 'Offer' widgets if available
        """
        pass
