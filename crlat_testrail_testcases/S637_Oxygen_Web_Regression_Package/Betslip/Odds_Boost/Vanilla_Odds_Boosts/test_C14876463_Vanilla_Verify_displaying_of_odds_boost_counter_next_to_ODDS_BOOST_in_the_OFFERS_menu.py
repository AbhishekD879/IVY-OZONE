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
class Test_C14876463_Vanilla_Verify_displaying_of_odds_boost_counter_next_to_ODDS_BOOST_in_the_OFFERS_menu(Common):
    """
    TR_ID: C14876463
    NAME: [Vanilla] Verify displaying of odds boost counter next to 'ODDS BOOST' in the 'OFFERS' menu
    DESCRIPTION: This test case verifies that users are able to see odds boost counter next to 'ODDS BOOST' options
    PRECONDITIONS: User has an Odds Boosts token. Token is NOT expired
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    """
    keep_browser_open = True

    def test_001_login_into_application(self):
        """
        DESCRIPTION: Login into application
        EXPECTED: User is logged in successfully
        EXPECTED: The "Odds Boost" token notification is displayed
        """
        pass

    def test_002_open_main_page_and_click_on_the_avatar_in_the_header(self):
        """
        DESCRIPTION: Open main page and click on the avatar in the header
        EXPECTED: Account MENU is opened with 'OFFERS & FREE BETS' option
        """
        pass

    def test_003_click_on_the_offers__free_bets_options(self):
        """
        DESCRIPTION: Click on the 'OFFERS & FREE BETS' options
        EXPECTED: 'Odds Boost' counter is shown next to 'ODDS BOOST' with the number of available odds boosts
        """
        pass

    def test_004_use_odds_boost_available_for_the_user_and_click_on_the_avatar_in_the_header(self):
        """
        DESCRIPTION: Use Odds Boost available for the user and click on the avatar in the header
        EXPECTED: Account MENU is opened with 'OFFERS & FREE BETS' option
        """
        pass

    def test_005_click_on_the_offers__free_bets_option(self):
        """
        DESCRIPTION: Click on the 'OFFERS & FREE BETS' option
        EXPECTED: 'Odds Boost' counter is shown next to 'ODDS BOOST' with the updated number of available odds boosts
        """
        pass

    def test_006_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        pass
