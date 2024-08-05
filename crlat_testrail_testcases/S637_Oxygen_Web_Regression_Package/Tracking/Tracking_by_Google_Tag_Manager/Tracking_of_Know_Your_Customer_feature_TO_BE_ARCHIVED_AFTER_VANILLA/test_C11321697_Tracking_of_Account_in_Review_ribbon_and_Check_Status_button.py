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
class Test_C11321697_Tracking_of_Account_in_Review_ribbon_and_Check_Status_button(Common):
    """
    TR_ID: C11321697
    NAME: Tracking of Account in Review ribbon and Check Status button
    DESCRIPTION: Test case verifies tracking of Account in Review ribbon display on Home page and "Check status" button click
    PRECONDITIONS: KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: **User has IMS Age verification status = Active grace period AND Player tag** = AGP_Success_Upload **with digit<5 as a value AND Player tag** "Verification_Review"
    """
    keep_browser_open = True

    def test_001_login_as_a_user_from_pre_conditionsand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Login as a user from pre-conditions,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - Home page contains review ribbon with "Check status" button
        EXPECTED: - Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'account in review banner',
        EXPECTED: 'eventLabel' : 'display'
        EXPECTED: })
        """
        pass

    def test_002_refresh_the_pageand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Refresh the page,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - Home page contains review ribbon with "Check status" button
        EXPECTED: - One more event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'account in review banner',
        EXPECTED: 'eventLabel' : 'display'
        EXPECTED: })
        """
        pass

    def test_003_tap_on_check_status_button_on_review_ribbonand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Tap on "Check status" button on review ribbon,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - Account in Review overlay appears
        EXPECTED: - Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'know your customer',
        EXPECTED: 'eventAction' : 'account in review banner',
        EXPECTED: 'eventLabel' : 'check status'
        EXPECTED: })
        EXPECTED: - Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/account-review-error'
        EXPECTED: })
        """
        pass
