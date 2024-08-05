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
class Test_C61160453_Euro_Loyalty_Page_Customers_observes_a_yellow_line_under_the_new_badge_to_be_qualified(Common):
    """
    TR_ID: C61160453
    NAME: Euro Loyalty Page- Customers observes a yellow line under the new badge to be qualified
    DESCRIPTION: This test case verifies whether a customer notices a yellow line under the new badge to be qualified
    PRECONDITIONS: User falls under a valid VIP Level and a qualifying bet is placed. The customer's last badge is lit up
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

    def test_003_verify_if_the_new_badge_is_highlighted_with_an_yellow_line_below_with_previous_badge_lit_up(self):
        """
        DESCRIPTION: Verify if the new badge is highlighted with an yellow line below with previous badge lit up
        EXPECTED: User should be able see the last won badge lit up and the new badge is highlighted with a yellow line
        """
        pass
