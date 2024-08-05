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
class Test_C11315115_Tracking_on_Verification_Failed_screen_with_Verify_My_Address_CTA(Common):
    """
    TR_ID: C11315115
    NAME: Tracking on Verification Failed screen with "Verify My Address" CTA
    DESCRIPTION: Test case verifies Google Tracking of page view and CTA click on Verification Failed screen with "Verify My Address" CTA
    PRECONDITIONS: KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: Note: To capture dataLayer before 3rd party page is opened on step 2 do the following:
    PRECONDITIONS: when page is loaded open Dev Tools > Sources > Event Listener Breakpoints > Load (check "beforeunload" and "unload" options)
    PRECONDITIONS: **User with IMS Age verification status = Active grace period AND Player tag** = AGP_Success_Upload **with digit<5 as a value AND tag** "POA_Required" **is logged in and sees Verification Failed screen with button "Verify My Address".**
    """
    keep_browser_open = True

    def test_001_in_console_type_datalayer__and_press_enterverify_that_correct_event_was_fired_when_verification_failed_screen_has_been_shown_to_the_user(self):
        """
        DESCRIPTION: In Console type "dataLayer"  and press Enter.
        DESCRIPTION: Verify that correct event was fired when Verification Failed screen has been shown to the user
        EXPECTED: Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/proof-of-address-failed'
        EXPECTED: })
        """
        pass

    def test_002_having_breakpoint_set_see_in_preconditions_tap_on_the_button_verify_my_address_and_then_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Having breakpoint set (see in preconditions) tap on the button "Verify My Address" and then in Console type "dataLayer" and press Enter
        EXPECTED: Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'proof of address failed',
        EXPECTED: 'eventLabel' : 'verify my address'
        EXPECTED: })
        """
        pass
