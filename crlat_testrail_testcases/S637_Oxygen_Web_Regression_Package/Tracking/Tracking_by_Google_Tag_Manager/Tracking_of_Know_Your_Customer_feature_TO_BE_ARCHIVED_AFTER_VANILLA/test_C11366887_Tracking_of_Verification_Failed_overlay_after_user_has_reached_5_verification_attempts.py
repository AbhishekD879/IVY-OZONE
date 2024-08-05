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
class Test_C11366887_Tracking_of_Verification_Failed_overlay_after_user_has_reached_5_verification_attempts(Common):
    """
    TR_ID: C11366887
    NAME: Tracking of Verification Failed overlay after user has reached 5 verification attempts
    DESCRIPTION: Test case verifies tracking of Verification Failed overlay display after user has reached 5 verification attempts
    PRECONDITIONS: KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: **User has IMS Age verification status = Active grace period AND tag** AGP_Success_Upload **with digit >=5 as a value (with or without tag** POA_Required )
    """
    keep_browser_open = True

    def test_001_login_as_a_user_from_pre_conditionsand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Login as a user from pre-conditions,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - Verification Failed overlay (with max attempts reached message) is shown
        EXPECTED: - Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/upload-5-times'
        EXPECTED: })
        """
        pass

    def test_002_tap_on_log_out_buttonand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on Log out button,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - User logged out
        EXPECTED: - Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'log out',
        EXPECTED: 'eventLabel' : 'log out'
        EXPECTED: })
        """
        pass
