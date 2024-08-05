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
class Test_C2594362_Verify_displaying_odds_boost_button_in_the_betslip_Single_selection_for_logged_in_user(Common):
    """
    TR_ID: C2594362
    NAME: Verify displaying odds boost button in the betslip (Single selection) for logged in user
    DESCRIPTION: This test case verifies that Odds Boost button displaying in the Betslip with Single selection for logged in user
    DESCRIPTION: AUTOTEST [C9690076]
    PRECONDITIONS: Links to designs dashboard: enter 'boost' into the search field:
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5cc18478560e4a2d671900df/dashboard
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5c01259e7c06af027fe0065a/dashboard
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: **Note:** Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Fractional odds format selected for User1
    PRECONDITIONS: Add a single selection with added Stake to the Betslip
    PRECONDITIONS: Login with User1
    """
    keep_browser_open = True

    def test_001_navigate_to_betslipverify_that_odds_boost_button_is_shown_in_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that Odds Boost button is shown in Betslip
        EXPECTED: Betslip is displayed with the following elements:
        EXPECTED: - 'BOOST' button
        EXPECTED: - text 'Odds Boost'
        EXPECTED: - 'Tap to boost your betslip' text
        EXPECTED: - 'i' icon (tooltip)
        EXPECTED: ![](index.php?/attachments/get/31353)
        EXPECTED: ![](index.php?/attachments/get/31354)
        """
        pass

    def test_002_add_stake_and_tap_boost_buttonverify_that_odds_are_boosted_and_odds_boost_button_is_displaying_with_animation(self):
        """
        DESCRIPTION: Add Stake and tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted and odds boost button is displaying with animation
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        EXPECTED: ![](index.php?/attachments/get/31350)
        EXPECTED: ![](index.php?/attachments/get/31351)
        """
        pass

    def test_003_refresh_pageverify_that_odds_boost_remains_boosted(self):
        """
        DESCRIPTION: Refresh page
        DESCRIPTION: Verify that odds boost remains boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        """
        pass

    def test_004_navigate_to_any_other_page_eg_homepagereopen_betslipverify_that_odds_boost_remains_boosted(self):
        """
        DESCRIPTION: Navigate to any other page e.g. Homepage
        DESCRIPTION: Reopen Betslip
        DESCRIPTION: Verify that odds boost remains boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        """
        pass

    def test_005_add_one_more_selection_with_odds_boost_availablenavigate_to_betslipverify_that_odds_boost_remains_boosted_and_new_selection_displaying_boosted(self):
        """
        DESCRIPTION: Add one more selection with Odds Boost available
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost remains boosted and new selection displaying boosted
        EXPECTED: Odds boost 'On' status is remembered:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        """
        pass

    def test_006_tap_boosted_buttonverify_that_odds_boost_are_removed_and_odds_boost_button_is_displaying_with_animation(self):
        """
        DESCRIPTION: Tap 'BOOSTED' button
        DESCRIPTION: Verify that odds boost are removed and odds boost button is displaying with animation
        EXPECTED: - 'BOOSTED' button is changed back to 'BOOST' button with animation
        EXPECTED: - Boosted odds are removed
        EXPECTED: - Returns are updated back
        """
        pass

    def test_007_navigate_to_any_other_page_eg_homepagereopen_betslipverify_that_odds_boost_remains_unboosted(self):
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

    def test_008_change_odd__format_to_decimalverify_that_this_functionality_works_the_same_with_decimal_odds(self):
        """
        DESCRIPTION: Change odd  format to Decimal
        DESCRIPTION: Verify that this functionality works the same with decimal odds
        EXPECTED: - Boosted odds is shown in decimal
        EXPECTED: - Original odds is displayed as crossed out in decimal
        """
        pass
