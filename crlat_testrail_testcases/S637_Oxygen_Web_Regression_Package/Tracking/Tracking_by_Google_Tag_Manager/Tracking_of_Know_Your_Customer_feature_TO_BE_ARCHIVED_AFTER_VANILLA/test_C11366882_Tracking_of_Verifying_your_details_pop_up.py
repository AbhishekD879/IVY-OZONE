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
class Test_C11366882_Tracking_of_Verifying_your_details_pop_up(Common):
    """
    TR_ID: C11366882
    NAME: Tracking of Verifying your details pop up
    DESCRIPTION: Test case verifies tracking of "Verifying Your Details" pop up display
    PRECONDITIONS: KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: **User has IMS Age verification status = Unknown**
    """
    keep_browser_open = True

    def test_001_login_as_a_user_from_pre_conditionsand_in_console_type_datalayer_and_press_enter(self):
        """
        DESCRIPTION: Login as a user from pre-conditions,
        DESCRIPTION: and in Console type "dataLayer" and press Enter
        EXPECTED: - Verifying Your Details pop up is shown
        EXPECTED: - Event has been fired to dataLayer with the following details:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/know-your-customer/in-progress' })
        """
        pass
