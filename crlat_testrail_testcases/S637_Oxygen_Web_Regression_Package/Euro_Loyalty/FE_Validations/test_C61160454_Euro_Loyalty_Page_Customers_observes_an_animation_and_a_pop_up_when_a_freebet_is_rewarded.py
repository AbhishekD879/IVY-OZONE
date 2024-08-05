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
class Test_C61160454_Euro_Loyalty_Page_Customers_observes_an_animation_and_a_pop_up_when_a_freebet_is_rewarded(Common):
    """
    TR_ID: C61160454
    NAME: Euro Loyalty Page-Customers observes an animation and a pop up when a freebet is rewarded
    DESCRIPTION: This test case verifies whether a customer recieves a pop-up and an animation if a freebet is rewarded
    PRECONDITIONS: User falls under a valid VIP Level and a qualifying bets are placed. The customer's last badge is lit up
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

    def test_003_verify_if_the_user_is_able_to_see_the_animation_and_pop_up_upon_receiving_a_freebet_on_the_elp(self):
        """
        DESCRIPTION: Verify if the user is able to see the animation and pop up upon receiving a freebet on the ELP
        EXPECTED: user is able to see the animation and pop up upon receiving a freebet
        """
        pass
