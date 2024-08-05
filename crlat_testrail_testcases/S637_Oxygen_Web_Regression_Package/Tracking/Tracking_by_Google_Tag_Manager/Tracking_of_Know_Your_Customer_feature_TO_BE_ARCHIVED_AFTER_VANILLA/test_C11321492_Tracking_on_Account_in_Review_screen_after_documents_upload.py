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
class Test_C11321492_Tracking_on_Account_in_Review_screen_after_documents_upload(Common):
    """
    TR_ID: C11321492
    NAME: Tracking on Account in Review screen after documents upload
    DESCRIPTION: Test case verifies tracking of page view, CTA click and close button on Account in Review page after successful documents upload
    PRECONDITIONS: KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: Note: To capture dataLayer before 3rd party page is opened on step 3 do the following:
    PRECONDITIONS: when page is loaded open Dev Tools > Sources > Event Listener Breakpoints > Load (check "beforeunload" and "unload" options)
    PRECONDITIONS: **User with IMS Age verification status = Active grace period and IMS tag** "AGP_Success_Upload" **with digit<5 as a value successfully uploaded documents to Jumio and sees "Account in Review" overlay with Verify My Address button**
    """
    keep_browser_open = True

    def test_001_in_console_type_datalayer__and_press_enterverify_that_correct_event_was_fired_when_verification_failed_screen_has_been_shown_to_the_user(self):
        """
        DESCRIPTION: In Console type "dataLayer"  and press Enter.
        DESCRIPTION: Verify that correct event was fired when Verification Failed screen has been shown to the user
        EXPECTED: Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/jumio-success'
        EXPECTED: })
        """
        pass

    def test_002_tap_on_the_close_buttonand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on the Close button,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'jumio success',
        EXPECTED: 'eventLabel' : 'close'
        EXPECTED: })
        """
        pass

    def test_003_repeat_pre_conditions_and_having_breakpoint_set_see_pre_conditions_tap_on_verify_my_address_buttonin_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Repeat pre-conditions and having breakpoint set (see pre-conditions) tap on "Verify My Address" button,
        DESCRIPTION: in Console type "dataLayer" and press Enter
        EXPECTED: Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'jumio success',
        EXPECTED: 'eventLabel' : 'verify my address'
        EXPECTED: })
        """
        pass
