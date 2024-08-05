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
class Test_C2610738_Verify_showing_odds_boost_section_on_bet_receipt_when_the_bet_was_placed_with_odds_boost_Combined_case(Common):
    """
    TR_ID: C2610738
    NAME: Verify showing odds boost section on bet receipt when the bet was placed with odds boost (Combined case)
    DESCRIPTION: This test case verifies that 'This bet has been boosted' text with boost icon is shown on bet receipt in case the bet was placed with odds boost for Multiple selection
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application
    PRECONDITIONS: Login with User1
    """
    keep_browser_open = True

    def test_001_add_selection_with_odds_boost_available_to_quick_betadd_stake_and_tap_boost_buttonverify_that_odds_is_boosted(self):
        """
        DESCRIPTION: Add selection with odds boost available to Quick Bet
        DESCRIPTION: Add Stake and Tap 'BOOST' button
        DESCRIPTION: Verify that odds is boosted
        EXPECTED: - ''BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/total potential returns is shown
        """
        pass

    def test_002_tap_place_bet_buttonverify_that_bet_receipts_is_shown_with_boosted_title(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet receipts is shown with boosted title
        EXPECTED: Receipt is shown with the following elements:
        EXPECTED: - boost icon
        EXPECTED: - hardcoded text: "This bet has been boosted!"
        EXPECTED: - boosted odds
        EXPECTED: - potential returns/total potential returns appropriate to boosted odds
        """
        pass

    def test_003_add_selections_to_betslip__selection_1_selection_2_with_odds_boost_available__selection_3_with_unavailable_odds_boostadd_stake_for_singles_and_multiplesverify_that_odds_boost_button_is_shown(self):
        """
        DESCRIPTION: Add selections to Betslip:
        DESCRIPTION: - Selection_1, Selection_2 with odds boost available
        DESCRIPTION: - Selection_3 with UNavailable odds boost
        DESCRIPTION: Add Stake for SINGLES and MULTIPLES
        DESCRIPTION: Verify that odds boost button is shown
        EXPECTED: 'BOOST' button is shown
        """
        pass

    def test_004_tap_boost_buttonverify_that_odds_for_selections_with_odds_boost_available_is_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds for selections with odds boost available is boosted
        EXPECTED: - ''BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds is shown for singles and for multiples section
        EXPECTED: - 'i' icon is shown for Selection_3
        EXPECTED: - Original odds is displayed as crossed out for Selection_1 and Selection_2
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/total potential returns are shown for singles and for multiples section section
        """
        pass

    def test_005_tap_i_iconverify_that_notification_is_shown(self):
        """
        DESCRIPTION: Tap 'i' icon
        DESCRIPTION: Verify that notification is shown
        EXPECTED: Notification is shown with hint text: "Odds Boost is unavailable for this selection'
        """
        pass

    def test_006_tap_outside_the_notificationverify_that_notification_is_closed(self):
        """
        DESCRIPTION: Tap outside the notification
        DESCRIPTION: Verify that notification is closed
        EXPECTED: Notification is closed
        """
        pass

    def test_007_tap_place_bet_buttonverify_that_bet_receipts_for_singles_and_multiples_bets_are_shown(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet receipts for singles and multiples bets are shown
        EXPECTED: Receipts for singles and multiples bets are shown with the following elements:
        EXPECTED: - boost icon
        EXPECTED: - hardcoded text: "This bet has been boosted!"
        EXPECTED: - boost odds taken by the user are shown for singles and for multiples
        EXPECTED: - boost icon and text "This bet has been boosted!" is NOT shown for single bet (Selection_3)
        EXPECTED: - Not boosted odds is shown for Selection_3
        EXPECTED: - potential returns/total potential returns appropriate to boosted odds and not boosted (selection_3)
        """
        pass
