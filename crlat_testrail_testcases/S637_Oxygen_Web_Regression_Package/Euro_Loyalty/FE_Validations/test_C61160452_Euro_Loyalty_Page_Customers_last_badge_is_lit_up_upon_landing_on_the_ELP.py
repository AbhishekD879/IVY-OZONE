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
class Test_C61160452_Euro_Loyalty_Page_Customers_last_badge_is_lit_up_upon_landing_on_the_ELP(Common):
    """
    TR_ID: C61160452
    NAME: Euro Loyalty Page- Customers' last badge is lit up upon landing on the ELP
    DESCRIPTION: This test case verifies whether a customer's last badge is lit up when navigated to ELP when bets have not been placed for the day yet
    PRECONDITIONS: User falls under a valid VIP Level and a qualifying bet is placed
    """
    keep_browser_open = True

    def test_001_login_with_valid_user_credentials(self):
        """
        DESCRIPTION: Login with valid user credentials
        EXPECTED: User should be able to login into the application
        """
        pass

    def test_002_verify_if_the_user_is_able_to_navigate_to_the_euro_loyalty_page_from_the_sub_header_menua_z_menu(self):
        """
        DESCRIPTION: Verify if the user is able to navigate to the Euro Loyalty page from the Sub header menu/A-Z menu
        EXPECTED: User should be able to navigate to Euro Loyalty page
        """
        pass

    def test_003_verify_if_the_last_achieved_badge_is_lit_up_as_per_the_animation_in_the_story(self):
        """
        DESCRIPTION: Verify if the last achieved badge is lit up as per the animation in the story
        EXPECTED: User should be able see the last won badge lit up upon navigating to the ELP
        """
        pass
