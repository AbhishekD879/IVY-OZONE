import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C12835257_Odds_Boost_token_icon_displaying(Common):
    """
    TR_ID: C12835257
    NAME: Odds Boost token icon displaying
    DESCRIPTION: This test case verifies displaying Odds Boost token value in Right menu and in My account (User menu).
    DESCRIPTION: AUTOTEST MOBILE: [C58216361]
    DESCRIPTION: AUTOTEST DESKTOP: [C58216486]
    PRECONDITIONS: 'Odds Boost' Feature is enabled in CMS
    PRECONDITIONS: 'Odds Boost' item is enabled in Right menu in CMS
    PRECONDITIONS: 'My account' (User menu) Feature Toggle is enabled in CMS
    PRECONDITIONS: 'Odds Boost' item is enabled in My account (User menu) in CMS
    PRECONDITIONS: Add Odds Boost token to Any bet to the user
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Generate Upcoming token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to create Upcoming Boosts https://confluence.egalacoral.com/display/SPI/How+to+create+Upcoming+Boosts
    PRECONDITIONS: Note: Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    """
    keep_browser_open = True

    def test_001_navigate_to_the_my_account_from_right_menu_for_mobile_and_tabletnavigate_to_my_account_from_the_header_of_the_page_for_desktopverify_that_sum_value_of_odds_boost_tokens_is_shown(self):
        """
        DESCRIPTION: Navigate to the 'My account' from Right menu (for mobile and tablet).
        DESCRIPTION: Navigate to 'My account' from the header of the page (for desktop).
        DESCRIPTION: Verify that sum value of Odds Boost tokens is shown.
        EXPECTED: * 'My account' menu is expanded
        EXPECTED: * Odds Boost item is available in the menu
        EXPECTED: * Sum value of Odds Boost tokens is displayed
        """
        pass

    def test_002_add_selection_to_the_betslip_boost_it_and_place_this_boosted_bet(self):
        """
        DESCRIPTION: Add selection to the Betslip, boost it and place this boosted bet.
        EXPECTED: Bet is placed successfully.
        """
        pass

    def test_003_navigate_to_the_my_account_and_verify_that_sum_value_of_odds_boost_tokens_decreased_by_one(self):
        """
        DESCRIPTION: Navigate to the 'My account' and verify that sum value of Odds Boost tokens decreased by one.
        EXPECTED: Sum value of Odds Boost tokens is updated according to available number of Odds Boost tokens (decreased by one).
        """
        pass

    def test_004_place_as_many_boosted_bets_as_there_are_number_of_odds_boost_tokens_available(self):
        """
        DESCRIPTION: Place as many boosted bets, as there are number of Odds Boost tokens available.
        EXPECTED: Bets are placed successfully.
        """
        pass

    def test_005_navigate_to_the_my_account_and_verify_that_sum_value_of_odds_boost_tokens_isnt_shown(self):
        """
        DESCRIPTION: Navigate to the 'My account' and verify that sum value of Odds Boost tokens isn't shown.
        EXPECTED: * Right menu is expanded
        EXPECTED: * Odds Boost item is available in the menu
        EXPECTED: * No icon with Sum value of Odds Boost tokens is displayed
        """
        pass
