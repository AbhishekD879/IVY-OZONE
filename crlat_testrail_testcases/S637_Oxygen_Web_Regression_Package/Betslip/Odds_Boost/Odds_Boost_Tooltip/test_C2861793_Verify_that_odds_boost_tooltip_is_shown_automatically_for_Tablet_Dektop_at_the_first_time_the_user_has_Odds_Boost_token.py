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
class Test_C2861793_Verify_that_odds_boost_tooltip_is_shown_automatically_for_Tablet_Dektop_at_the_first_time_the_user_has_Odds_Boost_token(Common):
    """
    TR_ID: C2861793
    NAME: Verify that odds boost tooltip is shown automatically for Tablet, Dektop at the first time the user has Odds Boost token
    DESCRIPTION: This test case verifies that odds boost tooltip is shown in Betslip for Tablet and Mobile
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Add Odds Boost tokens for USER1 using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: **Note:** Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Load application
    PRECONDITIONS: Clear Local Storage and Login with User1
    """
    keep_browser_open = True

    def test_001_add_selection_to_betslipverify_that_odds_boost_tooltip_popup_is_shown(self):
        """
        DESCRIPTION: Add selection to Betslip
        DESCRIPTION: Verify that odds boost tooltip popup is shown
        EXPECTED: Tooltip popup with hardcoded text is shown: 'Hit Boost to increase the odds of the bets in your betslip! You can boost up to (currency)XXX.XX total stake.'
        EXPECTED: ![](index.php?/attachments/get/7721808)
        EXPECTED: ![](index.php?/attachments/get/7721809)
        """
        pass

    def test_002_navigate_to_local_storageverify_that_oxoddsboostseen_is_added(self):
        """
        DESCRIPTION: Navigate to Local Storage
        DESCRIPTION: Verify that 'OX.oddsBoostSeen' is added
        EXPECTED: The key is shown in Local Storage: OX.oddsBoostSeen = true
        """
        pass

    def test_003_tap_ok_buttonverify_that_tooltip_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that tooltip popup is closed
        EXPECTED: Tooltip popup is closed
        """
        pass

    def test_004_remove_selection_from_betslip_and_add_new_selection_to_betslipverify_that_odds_boost_tooltip_popup_is_not_shown_automatically_in_betslip(self):
        """
        DESCRIPTION: Remove selection from Betslip and ADD new selection to Betslip
        DESCRIPTION: Verify that odds boost tooltip popup is not shown automatically in Betslip
        EXPECTED: - Odds Boost popup is not shown
        EXPECTED: - 'i' icon is shown
        """
        pass

    def test_005_tap_i_iconverify_that_tooltip_popup_is_shown(self):
        """
        DESCRIPTION: Tap 'i' icon
        DESCRIPTION: Verify that tooltip popup is shown
        EXPECTED: Tooltip popup with hardcoded text is shown: 'Hit Boost to increase the odds of the bets in your betslip! You can boost up to (currency)XXX.XX total stake.'
        """
        pass

    def test_006_tap_ok_buttonverify_that_tooltip_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that tooltip popup is closed
        EXPECTED: Tooltip popup is closed
        """
        pass
