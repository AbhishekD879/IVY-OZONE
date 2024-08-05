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
class Test_C2861261_Verify_Password_field_validation(Common):
    """
    TR_ID: C2861261
    NAME: Verify 'Password' field validation
    DESCRIPTION: This test case verifies 'Password' field validation on Account Closure step 2 page
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [8146652](https://ladbrokescoral.testrail.com/index.php?/cases/view/8146652)
    DESCRIPTION: Desktop - [8146653](https://ladbrokescoral.testrail.com/index.php?/cases/view/8146653)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: * Tap/click 'I want to close my Account' link within 'Account Closure' section
    PRECONDITIONS: * Select any option from 'Closure Reason' drop-down and click/tap 'CONTINUE' button
    """
    keep_browser_open = True

    def test_001_enter_the_incorrect_password_in_password_field(self):
        """
        DESCRIPTION: Enter the incorrect password in 'Password' field
        EXPECTED: * Password' field is populated with the value
        EXPECTED: * 'CONTINUE' button becomes enabled
        EXPECTED: * No error message is displayed
        """
        pass

    def test_002_clicktap_continue_button(self):
        """
        DESCRIPTION: Click/tap 'CONTINUE' button
        EXPECTED: 'Wrong password, please retype and try again' error message is displayed below to 'Password' field
        """
        pass

    def test_003_remove_incorrect_password_from_password_field(self):
        """
        DESCRIPTION: Remove incorrect password from 'Password' field
        EXPECTED: * 'CONTINUE' button becomes disabled again
        EXPECTED: * Error message is still displayed
        """
        pass

    def test_004_enter_the_correct_password_the_password_field(self):
        """
        DESCRIPTION: Enter the correct password the 'Password' field
        EXPECTED: * Error message is still displayed
        EXPECTED: * 'CONTINUE' button becomes enabled
        EXPECTED: * Password' field is populated with the value
        """
        pass

    def test_005_clicktap_continue_button(self):
        """
        DESCRIPTION: Click/tap 'CONTINUE' button
        EXPECTED: * Error message is no more displayed
        """
        pass
