import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C14714893_In_ProgressVanilla_Verify_displaying_of_free_bet_counter_next_to_SPORTS_FREE_BETS_option_in_the_OFFERS_FREE_BETS_menu(Common):
    """
    TR_ID: C14714893
    NAME: [In Progress][Vanilla] Verify displaying of free bet counter next to 'SPORTS FREE BETS' option in the 'OFFERS & FREE BETS' menu
    DESCRIPTION: This test case verifies that users are able to see free bet counter next to 'SPORTS FREE BETS' option
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: - Instructions how to add free bet tokens for TEST2/STAGE users or existing PROD users with already granted tokens can be found here: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: - FreeBets menu item exists if available in CMS (Right Menu) no matter if FreeBets are available to the user or not
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in with only 1 FreeBet available
    """
    keep_browser_open = True

    def test_001_clicktap_the_my_account_button_on_the_header_with_fb_icon_available(self):
        """
        DESCRIPTION: Click/Tap the 'My Account' button on the Header with 'FB' icon available
        EXPECTED: * 'My Account' menu is opened with 'OFFERS & FREE BETS' option available
        """
        pass

    def test_002_clicktap_on_the_offers__free_bets_option(self):
        """
        DESCRIPTION: Click/Tap on the 'OFFERS & FREE BETS' option
        EXPECTED: 'Free Bet' counter is shown next to 'SPORT FREE BETS' with the number of available free bets (1)
        """
        pass

    def test_003__use_free_bet_available_for_the_user_back_to_the_offers__free_bets_menu(self):
        """
        DESCRIPTION: * Use free bet available for the user.
        DESCRIPTION: * Back to the 'OFFERS & FREE BETS' menu.
        EXPECTED: 'Free Bet' counter is not shown next to 'SPORT FREE BETS'
        """
        pass

    def test_004_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        pass

    def test_005_login_to_the_account_with_multiple_more_than_two_freebets_available_and_click_on_the_avatar_in_the_header(self):
        """
        DESCRIPTION: Login to the account with multiple (more than two) FreeBets available and click on the avatar in the header
        EXPECTED: Account MENU is opened with 'OFFERS & FREE BETS' option
        """
        pass

    def test_006_click_on_the_offers__free_bets_options(self):
        """
        DESCRIPTION: Click on the 'OFFERS & FREE BETS' options
        EXPECTED: Free Bet counter is shown next to 'SPORT FREE BETS' with the number of available free bets
        """
        pass

    def test_007_use_one_of_the_free_bet_and_click_on_the_avatar_in_the_header(self):
        """
        DESCRIPTION: Use one of the free bet and click on the avatar in the header
        EXPECTED: Account MENU is opened with 'OFFERS & FREE BETS' options
        """
        pass

    def test_008_click_on_the_offers__free_bets_option(self):
        """
        DESCRIPTION: Click on the 'OFFERS & FREE BETS' option
        EXPECTED: Free Bet counter is shown next to ’SPORT FREE BETS’ with the updated number of available free bets (n-1)
        """
        pass
