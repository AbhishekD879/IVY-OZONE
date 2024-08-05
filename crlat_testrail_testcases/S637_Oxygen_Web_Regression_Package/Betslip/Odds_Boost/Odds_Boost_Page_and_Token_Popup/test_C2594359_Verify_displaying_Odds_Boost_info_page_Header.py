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
class Test_C2594359_Verify_displaying_Odds_Boost_info_page_Header(Common):
    """
    TR_ID: C2594359
    NAME: Verify displaying Odds Boost info page Header
    DESCRIPTION: This test case verifies displaying Odds Boost info page Header
    DESCRIPTION: AUTOMATED [C13755539] [C13802093]
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: CMS Define in Odds Boost details page:
    PRECONDITIONS: - Image_1 (svg file)
    PRECONDITIONS: - 'HeaderText_1'  for logged out user
    PRECONDITIONS: - 'HeaderText_2'  for logged in user
    PRECONDITIONS: - 'T&C_1' in Terms and Conditions text field
    PRECONDITIONS: Load application
    PRECONDITIONS: Do NOT login
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: How to create Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: How to create Upcoming Boosts https://confluence.egalacoral.com/display/SPI/How+to+create+Upcoming+Boosts
    PRECONDITIONS: User1:
    PRECONDITIONS: There are 'X1'  AVAILABLE NOW odds boost (where X1 - number of *active* Odds Boost tokens generated for the user)
    PRECONDITIONS: There are 'X2'  UPCOMING odds boost (where X2 - number of *upcoming* Odds Boost tokens generated for the user
    """
    keep_browser_open = True

    def test_001_navigate_to_the_odds_boost_info_page_tap_oddsboost_in_the_urlverify_odds_boost_page_displaying_for_logged_out_user(self):
        """
        DESCRIPTION: Navigate to the Odds boost info page (tap '/oddsboost' in the URL)
        DESCRIPTION: Verify Odds Boost page displaying for logged out user.
        EXPECTED: Odds Boost page is displayed with the following elements:
        EXPECTED: - Image1
        EXPECTED: - 'HeaderText_1'
        EXPECTED: - 'AVAILABLE NOW' value is displayed as 0
        EXPECTED: - 'UPCOMING BOOSTS' value is displayed as 0
        EXPECTED: - 'LOG IN' button is displayed
        EXPECTED: - 'T&C_1' in Terms&Coditions' section
        """
        pass

    def test_002_login_with_user1_from_preconditionsverify_odds_boost_page_displaying_for_logged_in_user(self):
        """
        DESCRIPTION: Login with User1 from preconditions.
        DESCRIPTION: Verify Odds Boost page displaying for logged in user
        EXPECTED: Odds Boost page is displayed with following elements::
        EXPECTED: - Image1
        EXPECTED: - 'HeaderText_2'
        EXPECTED: - 'AVAILABLE NOW' value is displayed as 'X1'
        EXPECTED: - 'UPCOMING BOOSTS' value is displayed as 'X2'
        EXPECTED: -  List of available Odds Boosts for the user ('boosts available now' and 'upcoming boosts' sections)
        EXPECTED: - 'T&C_1' in Terms&Coditions' section
        EXPECTED: *Coral*
        EXPECTED: ![](index.php?/attachments/get/106905296)
        EXPECTED: *Ladbrokes*
        EXPECTED: ![](index.php?/attachments/get/106905305)
        """
        pass

    def test_003_log_out_and_verify_user_is_navigated_to_the_homepage(self):
        """
        DESCRIPTION: Log out and verify user is navigated to the Homepage
        EXPECTED: User is navigated to the Homepage
        """
        pass
