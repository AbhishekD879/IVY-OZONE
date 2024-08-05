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
class Test_C11366772_Tracking_of_Verification_success_pop_up(Common):
    """
    TR_ID: C11366772
    NAME: Tracking of Verification success pop up
    DESCRIPTION: Test case verifies tracking of verification success pop up display and tap on "Deposit Now" CTA
    PRECONDITIONS: KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: **User has IMS Age verification status = Active grace period AND Player tag** = AGP_Success_Upload **with digit<5 as a value AND Player tag** "Verification_Review"
    """
    keep_browser_open = True

    def test_001_login_as_a_user_from_pre_conditions(self):
        """
        DESCRIPTION: Login as a user from pre-conditions
        EXPECTED: Review ribbon with Check Status button is shown on Home screen
        """
        pass

    def test_002_on_ims_change_age_verification_status_of_a_user_to_under_review_and_tap_check_status_button_in_the_appin_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: On IMS change Age verification status of a user to "Under Review" and tap Check Status button in the app,
        DESCRIPTION: in Console type "dataLayer" and press Enter
        EXPECTED: - "Account Verification" pop up with "Deposit Now" CTA is shown
        EXPECTED: - Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/account-verification-success' })
        """
        pass

    def test_003_tap_on_deposit_nowin_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on Deposit now,
        DESCRIPTION: in Console type "dataLayer" and press Enter
        EXPECTED: - Deposit page is loaded
        EXPECTED: - Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'account verification success',
        EXPECTED: 'eventLabel' : 'deposit now'
        EXPECTED: })
        """
        pass
