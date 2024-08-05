import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2323083_Tracking_of_in_shop_user_success_log_in(Common):
    """
    TR_ID: C2323083
    NAME: Tracking of in-shop user success log in
    DESCRIPTION: This test case verifies google analytics gathering for an in-shop user successfully logging in
    PRECONDITIONS: The following user can be used for testing:
    PRECONDITIONS: Card: 5000000000992086
    PRECONDITIONS: PIN: 1234
    PRECONDITIONS: if you need to generate new in-shop account use attached postman collection (run 'get-token' request, then 'Create In-Shop account' where you need to set 'mobile' parameter with a random phone number in format 7xxxxxxxxx)
    PRECONDITIONS: Open GA: dev tool -> Concsole -> type 'Datalayer' near '>'
    """
    keep_browser_open = True

    def test_001_log_in_to_the_system_as_an_existent_in_shop_user_without_enabling_checkboxes_rememer_username_remember_me(self):
        """
        DESCRIPTION: Log in to the system as an existent in-shop user (without enabling checkboxes 'rememer username' /'remember me')
        EXPECTED: A user is successfully logged in
        """
        pass

    def test_002_in_console_window_type_datalayer_and_press_enter_button(self):
        """
        DESCRIPTION: In Console window type 'dataLayer' and press Enter button
        EXPECTED: Objects are displayed within Console window
        """
        pass

    def test_003_expand_the_last_object(self):
        """
        DESCRIPTION: Expand the last Object
        EXPECTED: Following tags are displayed:
        EXPECTED: - 'event' : ''trackPageview''
        EXPECTED: - 'virtualUrl' : ''/login/success''
        EXPECTED: - 'location' : ''header''
        EXPECTED: - 'loginOption' : ''none''
        EXPECTED: - 'loginType' : ''connect card''
        EXPECTED: });
        """
        pass

    def test_004_log_out_from_application(self):
        """
        DESCRIPTION: Log out from application
        EXPECTED: User successfully logged out
        """
        pass
