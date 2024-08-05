import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C179953_Verify_Self_Exclusion_Page_and_Form_after_Log_out(Common):
    """
    TR_ID: C179953
    NAME: Verify Self Exclusion Page and Form after Log out
    DESCRIPTION: This test case verifies Self Exclusion Page and Form after Log out
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger an event when the session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Oxygen app in one browser tab and open 'Self Exclusion' page/pop-up
    PRECONDITIONS: *   Login to Oxygen app in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged
    """
    keep_browser_open = True

    def test_001_make_steps_from_preconditions_for_self_exclusion_page(self):
        """
        DESCRIPTION: Make steps from Preconditions for 'Self Exclusion' page
        EXPECTED: 
        """
        pass

    def test_002_verify_self_exclusion_page(self):
        """
        DESCRIPTION: Verify **'Self Exclusion'** page
        EXPECTED: * The user is logged out from the application without performing any actions
        EXPECTED: * User is not able to see the content of **'Self Exclusion'** page
        EXPECTED: * User is navigated to the Homepage
        """
        pass

    def test_003_make_steps_from_preconditions_for_self_exclusion_request_pop_up(self):
        """
        DESCRIPTION: Make steps from Preconditions for 'Self Exclusion Request' pop-up
        EXPECTED: 
        """
        pass

    def test_004_verify_self_exclusion_request_pop_up(self):
        """
        DESCRIPTION: Verify **'Self Exclusion Request'** pop-up
        EXPECTED: * The user is logged out from the application without performing any actions
        EXPECTED: * User is not able to see the content of **'Self Exclusion Request'** pop-up
        EXPECTED: * User is navigated to the Homepage
        """
        pass
