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
class Test_C11328078_Tracking_of_Review_Details_pop_up(Common):
    """
    TR_ID: C11328078
    NAME: Tracking of Review Details pop up
    DESCRIPTION: Test case verifies tracking of pop up view, CTA click and closure on Review Details pop up triggered from link on Verification Failed screen
    PRECONDITIONS: KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: **User with IMS Age verification status = Active grace period AND tag** AGP_Success_Upload **with digit < 5 as a value (with or without tag** POA_Required **) sees Verification Failed Screen with Verify Me or Verify My Address button**
    """
    keep_browser_open = True

    def test_001_tap_on_review_my_details_linkand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on Review My Details link,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - Review Details pop up is opened
        EXPECTED: - Event has been fired to dataLayer with the following details:
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "verification v1" (on the screen with Verify ME CTA) or 'proof of address failed' (on the screen with Verify My Address CTA)
        EXPECTED: eventCategory: "know your customer"
        EXPECTED: eventLabel: "edit my details"
        EXPECTED: - Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/edit-my-details'
        EXPECTED: })
        """
        pass

    def test_002_in_the_opened_pop_up_tap_close_buttonand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: In the opened pop up tap Close button,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'edit my details',
        EXPECTED: 'eventLabel' : 'close'
        EXPECTED: })
        EXPECTED: - Pop up closed
        """
        pass

    def test_003_tap_on_review_my_details_link_and_in_opened_pop_up_fill_in_editable_fields_and_tap_update_addressin_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on Review My Details link and in opened pop up fill in editable fields and tap "Update Address",
        DESCRIPTION: in Console type "dataLayer" and press Enter
        EXPECTED: - trackPageview' event has been fired to dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/edit-my-details'
        EXPECTED: })
        EXPECTED: - Update Address event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'edit my details',
        EXPECTED: 'eventLabel' : 'update address'
        EXPECTED: })
        """
        pass
