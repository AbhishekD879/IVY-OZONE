import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870343_Verify_that_GDPR_banner_is_displayed_on_user_login(Common):
    """
    TR_ID: C44870343
    NAME: Verify that GDPR banner is displayed on user login.
    DESCRIPTION: 
    PRECONDITIONS: 1. The user with the following tag in IMS is available - Market preference is set to NO.
    PRECONDITIONS: 2. User is not logged into the application.
    """
    keep_browser_open = True

    def test_001_login_into_the_application_with_the_user_mentioned_in_pre_conditions_verify(self):
        """
        DESCRIPTION: Login into the application with the user mentioned in pre-conditions. Verify.
        EXPECTED: GDPR banner consisting of privacy policies etc along with option of marketing preferences is displayed.
        """
        pass

    def test_002_click_on_the_various_links_displayed_in_the_gdpr_banner_and_verify(self):
        """
        DESCRIPTION: Click on the various links displayed in the GDPR banner and verify.
        EXPECTED: User navigates to respective account one link (which is provided in CMS).
        """
        pass
