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
class Test_C2553400_Tracking_of_Existing_user_Login_pop_up_TO_BE_ARCHIVED_AFTER_VANILLA(Common):
    """
    TR_ID: C2553400
    NAME: Tracking of Existing user Login pop-up  [TO BE ARCHIVED AFTER VANILLA]
    DESCRIPTION: This Test Case verifies tracking in the Google Analytic's data Layer Existing user Login pop-up (after Registration with Duplicate Email Address)
    DESCRIPTION: AUTOTEST [C2911053]
    DESCRIPTION: **Jira ticket**
    DESCRIPTION: BMA-33100 Remove Call/email options from Reg Page when entering an existing email and add tracking [1]
    DESCRIPTION: [1] https://jira.egalacoral.com/browse/BMA-33100
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Existing users with known email address should be registered
    PRECONDITIONS: * test@playtech.com email address is an exception to the rule. There is no validation for its usage for different users
    PRECONDITIONS: * User should fill in all required fields with valid data till the 'Email' field
    """
    keep_browser_open = True

    def test_001_enter_email_address_of_already_existing_user_to_the_email_field_and_clicktap_out_of_the_field(self):
        """
        DESCRIPTION: Enter email address of already existing user to the 'Email' field and click/tap out of the field
        EXPECTED: * Existing user Log In pop-up appears on the screen
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer{
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'virtualUrl' : '/login/existing'
        EXPECTED: };
        """
        pass

    def test_003_click_on_a_cta_within_the_existing_user_login_pop_up(self):
        """
        DESCRIPTION: Click on a CTA within the existing user Login pop-up
        EXPECTED: 
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer{
        EXPECTED: 'eventCategory' : 'login - existing',
        EXPECTED: 'eventAction' : 'cta'
        EXPECTED: 'eventLabel' : '<< CTA >>'
        EXPECTED: };
        """
        pass

    def test_005_verify_eventlabel_parameter_that_present_in_current_object_in_datalayer_(self):
        """
        DESCRIPTION: Verify 'eventLabel' parameter that present in current object in 'dataLayer' :
        EXPECTED: 'eventLabel' = depends on witch item the user clicked on within the 'Existing User' Login pop-up:
        EXPECTED: * 'eventLabel' : 'login'
        EXPECTED: * 'eventLabel' : 'forgot password'
        EXPECTED: * 'eventLabel' : 'forgot username'
        """
        pass
