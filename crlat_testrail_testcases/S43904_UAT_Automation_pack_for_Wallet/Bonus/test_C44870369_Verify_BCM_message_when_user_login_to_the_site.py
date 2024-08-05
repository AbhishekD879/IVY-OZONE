import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C44870369_Verify_BCM_message_when_user_login_to_the_site(Common):
    """
    TR_ID: C44870369
    NAME: Verify BCM message when user login to the site.
    DESCRIPTION: 
    PRECONDITIONS: 1. User has BCM/bonus offer.
    PRECONDITIONS: 2. User is not logged in the application.
    """
    keep_browser_open = True

    def test_001_launch_the_application_and_login_with_user_according_to_the_precondition(self):
        """
        DESCRIPTION: Launch the application and login with user according to the precondition.
        EXPECTED: The BCM/bonus message for gaming is displayed as soon as the user logs in the application.
        """
        pass

    def test_002_click_on_ok_in_the_message(self):
        """
        DESCRIPTION: Click on 'OK' in the message.
        EXPECTED: 1. The user is on Home page.
        EXPECTED: 2. The user is not directed to the Gaming page.
        """
        pass
