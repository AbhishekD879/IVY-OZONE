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
class Test_C61160451_Euro_Loyalty_Page_Customers_observes_a_yellow_line_under_the_first_badge_upon_ELP_launch_for_a_user_with_zero_active_badges(Common):
    """
    TR_ID: C61160451
    NAME: Euro Loyalty Page- Customers observes a yellow line under the first badge upon ELP launch for a user with zero active badges
    DESCRIPTION: This test case verifies whether a customer observes a yellow line under the first badge on ELP with zero active badges
    PRECONDITIONS: User falls under a valid VIP Level and a qualifying bet is not placed so far
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

    def test_003_verify_if_the_first_badge_is_highlighted_with_a_yellow_line_on_the_page_load(self):
        """
        DESCRIPTION: Verify if the first badge is highlighted with a yellow line on the page load
        EXPECTED: User should be able to notice the first badge underlined with a yellow line
        """
        pass
