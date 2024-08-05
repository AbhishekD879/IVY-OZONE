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
class Test_C2854697_Verify_displaying_token_count_icon_when_there_is_no_Odds_Boost_token_available(Common):
    """
    TR_ID: C2854697
    NAME: Verify displaying token count icon when there is no Odds Boost token available
    DESCRIPTION: This test case verifies displaying token count icon when there is no Odds Boost tokens available
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: 'Odds Boost' item is enabled in Right menu in CMS
    PRECONDITIONS: 'My account' (User menu) Feature Toggle is enabled in CMS
    PRECONDITIONS: 'Odds Boost' item is enabled in My account (User menu) in CMS
    PRECONDITIONS: Add 1 Odds Boost token to Any bet to the user
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    """
    keep_browser_open = True

    def test_001_navigate_to_the_my_account_user_menu_from_right_menu_for_mobile_and_tablet_onlynavigate_to_my_account_user_menu_from_the_header_of_the_page_for_desktop(self):
        """
        DESCRIPTION: Navigate to the 'My account' (User menu) from Right menu (for mobile and tablet only)
        DESCRIPTION: Navigate to 'My account' (User menu) from the header of the page (for desktop)
        EXPECTED: - 'My account' (User menu) menu is expanded
        EXPECTED: - Odds Boost item is available in the menu
        EXPECTED: - Summary value 1 of the number of Odds Boost tokens is displaying in Odds Boost item
        """
        pass

    def test_002_tap_on_odds_boost_item(self):
        """
        DESCRIPTION: Tap on Odds Boost item
        EXPECTED: User is navigated to the Odds Boost information page
        """
        pass

    def test_003_place_a_bet_with_available_on_information_page_odds_boost_token(self):
        """
        DESCRIPTION: Place a bet with available on information page Odds boost token
        EXPECTED: - Bet is placed
        EXPECTED: - Odds Boost token is used
        """
        pass

    def test_004_navigate_to_the_my_account_user_menu_from_right_menu_for_mobile_and_tablet_onlynavigate_to_my_account_user_menu_from_the_header_of_the_page_for_desktop(self):
        """
        DESCRIPTION: Navigate to the 'My account' (User menu) from Right menu (for mobile and tablet only)
        DESCRIPTION: Navigate to 'My account' (User menu) from the header of the page (for desktop)
        EXPECTED: - 'My account' (User menu) menu is expanded
        EXPECTED: - Odds Boost item is available in the menu
        EXPECTED: - NO icon is displayed in Odds Boost item
        """
        pass
