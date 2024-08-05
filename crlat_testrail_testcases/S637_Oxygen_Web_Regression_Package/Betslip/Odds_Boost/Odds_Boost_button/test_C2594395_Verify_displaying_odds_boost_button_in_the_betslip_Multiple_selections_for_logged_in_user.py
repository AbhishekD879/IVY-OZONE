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
class Test_C2594395_Verify_displaying_odds_boost_button_in_the_betslip_Multiple_selections_for_logged_in_user(Common):
    """
    TR_ID: C2594395
    NAME: Verify displaying odds boost button in the betslip (Multiple selections) for logged in user
    DESCRIPTION: This test case verifies that Odds Boost button displaying in the Betslip with Multiple selection for logged in user
    DESCRIPTION: AUTOTEST [C9690077]
    PRECONDITIONS: Links to designs dashboard: enter 'boost' into the search field:
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5cc18478560e4a2d671900df/dashboard
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5c01259e7c06af027fe0065a/dashboard
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: **Note:** Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Fractional odds format selected for User1
    PRECONDITIONS: Load application and do NOT login
    PRECONDITIONS: Add Multiple selections with added Stake to the Betslip
    PRECONDITIONS: One of the selections is with unavailable Odds Boost
    """
    keep_browser_open = True

    def test_001_navigate_to_betslipverify_that_odds_boost_button_is_not_shown(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that Odds Boost button is NOT shown
        EXPECTED: 'BOOST' button is not shown
        """
        pass

    def test_002_login_with_user1_and_navigate_to_betslipverify_that_odds_boost_button_is_shown_in_betslip(self):
        """
        DESCRIPTION: Login with User1 and navigate to Betslip
        DESCRIPTION: Verify that Odds Boost button is shown in Betslip
        EXPECTED: Betslip is displayed with the following elements:
        EXPECTED: - 'BOOST' button
        EXPECTED: - 'Tap to boost your betslip' text
        EXPECTED: - 'i' icon (tooltip)
        EXPECTED: ![](index.php?/attachments/get/31365)
        EXPECTED: ![](index.php?/attachments/get/31364)
        """
        pass

    def test_003_enter_stakes_and_tap_a_boost_buttonverify_that_odds_are_boosted_for_odds_with_available_odds_boost_and_odds_boost_button_is_displaying_with_animation(self):
        """
        DESCRIPTION: Enter Stakes and tap a 'BOOST' button
        DESCRIPTION: Verify that odds are boosted for odds with available odds boost and odds boost button is displaying with animation
        EXPECTED: Betslip is displayed with the following elements:
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds (fractional) are shown for singles and for multiples section
        EXPECTED: - Original odds (fractional)is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown for singles and for multiples section section
        EXPECTED: ![](index.php?/attachments/get/31368)
        EXPECTED: ![](index.php?/attachments/get/31367)
        """
        pass

    def test_004_navigate_to_any_other_page_eg_homepagereopen_betslipverify_that_odds_boost_remains_boosted(self):
        """
        DESCRIPTION: Navigate to any other page e.g. Homepage
        DESCRIPTION: Reopen Betslip
        DESCRIPTION: Verify that odds boost remains boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) are shown for singles and for multiples section
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown for singles and for multiples section section
        """
        pass

    def test_005_refresh_pageverify_that_odds_boost_remains_boosted(self):
        """
        DESCRIPTION: Refresh page
        DESCRIPTION: Verify that odds boost remains boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) is shown for singles and for multiples section
        EXPECTED: - Original odds (fractional) are displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds)returns are shown for singles and for multiples section section
        """
        pass

    def test_006_add_one_more_selection_with_odds_boost_availablenavigate_to_betslipverify_that_odds_boost_remains_boosted_and_new_selection_displaying_boosted(self):
        """
        DESCRIPTION: Add one more selection with Odds Boost available
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost remains boosted and new selection displaying boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) is shown for singles and for TREBLE section
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown for singles and for multiples section section
        """
        pass

    def test_007_tap_boosted_buttonverify_that_odds_boost_are_removed_and_odds_boost_button_is_displaying_with_animation(self):
        """
        DESCRIPTION: Tap 'BOOSTED' button
        DESCRIPTION: Verify that odds boost are removed and odds boost button is displaying with animation
        EXPECTED: Betslip is displayed with the following elements:
        EXPECTED: - 'BOOSTED' button is changed back to 'BOOST' button with animation
        EXPECTED: - Boosted odds are removed
        EXPECTED: - Returns are updated back
        """
        pass

    def test_008_navigate_to_any_other_page_eg_homepagereopen_betslipverify_that_odds_boost_remains_unboosted(self):
        """
        DESCRIPTION: Navigate to any other page e.g. Homepage
        DESCRIPTION: Reopen Betslip
        DESCRIPTION: Verify that odds boost remains UNboosted
        EXPECTED: Odds boost 'Off' status is remembered:
        EXPECTED: - 'BOOST' button is shown
        EXPECTED: - Original odds is shown
        EXPECTED: - Original returns are shown
        """
        pass

    def test_009_change_odd_format_to_decimalverify_that_this_functionality_works_the_same_with_decimal_odds(self):
        """
        DESCRIPTION: Change odd format to Decimal
        DESCRIPTION: Verify that this functionality works the same with decimal odds
        EXPECTED: - Boosted odds is shown for singles and for multiples section in decimal
        EXPECTED: - Original odds is displayed as crossed out in decimal
        """
        pass
