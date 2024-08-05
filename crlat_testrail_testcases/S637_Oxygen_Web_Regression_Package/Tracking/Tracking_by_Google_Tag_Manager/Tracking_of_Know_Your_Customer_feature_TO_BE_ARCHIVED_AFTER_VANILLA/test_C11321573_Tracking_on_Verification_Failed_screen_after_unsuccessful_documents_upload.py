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
class Test_C11321573_Tracking_on_Verification_Failed_screen_after_unsuccessful_documents_upload(Common):
    """
    TR_ID: C11321573
    NAME: Tracking on Verification Failed screen after unsuccessful documents upload
    DESCRIPTION: Test case verifies tracking of page view and CTA and log out click on Verification Failed screen after unsuccessful documents upload
    PRECONDITIONS: KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: Note: To capture dataLayer before 3rd party page is opened on step 2 do the following:
    PRECONDITIONS: when page is loaded open Dev Tools > Sources > Event Listener Breakpoints > Load (check "beforeunload" and "unload" options)
    PRECONDITIONS: **User with IMS Age verification status = Active grace period AND tag** AGP_Success_Upload **with digit < 5 as a value (with or without tag** POA_Required **) failed to upload documents to Jumio and is redirected to Verification Failed Screen with Try Again button**
    """
    keep_browser_open = True

    def test_001_in_console_type_datalayer_and_press_enterverify_that_correct_event_was_fired_when_verification_failed_screen_has_been_shown_to_the_user(self):
        """
        DESCRIPTION: In Console type "dataLayer" and press Enter.
        DESCRIPTION: Verify that correct event was fired when Verification Failed screen has been shown to the user
        EXPECTED: Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/jumio-error'
        EXPECTED: })
        """
        pass

    def test_002_having_breakpoint_set_see_pre_conditions_tap_on_try_again_buttonand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Having breakpoint set (see pre-conditions), tap on Try Again button,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'Try again',
        EXPECTED: 'eventLabel' : 'Try again'
        EXPECTED: })
        """
        pass

    def test_003_repeat_pre_conditions_and_tap_on_log_out_buttonand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Repeat pre-conditions and tap on Log out button,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'log out',
        EXPECTED: 'eventLabel' : 'log out'
        EXPECTED: })
        """
        pass
