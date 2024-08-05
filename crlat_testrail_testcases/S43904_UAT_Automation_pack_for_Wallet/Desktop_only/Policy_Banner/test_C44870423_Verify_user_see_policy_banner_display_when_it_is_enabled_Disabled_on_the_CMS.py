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
class Test_C44870423_Verify_user_see_policy_banner_display_when_it_is_enabled_Disabled_on_the_CMS(Common):
    """
    TR_ID: C44870423
    NAME: Verify user see policy banner display when it is enabled/Disabled on the CMS
    DESCRIPTION: 
    PRECONDITIONS: Policy banner should be enabled/disabled in the CMS so that it can be displayed/not displayed respectively.
    """
    keep_browser_open = True

    def test_001_log_in_with_valid_credential_and_observe_the_banner_when_the_policy_banner_is_enabled_in_cms(self):
        """
        DESCRIPTION: Log in with valid credential and observe the banner, when the Policy banner is enabled in CMS
        EXPECTED: The Policy banner is displayed in Frontend.
        """
        pass

    def test_002_log_in_with_same_credentials_and_observe_the_banner_when_the_policy_banner_is_disabled_in_cms(self):
        """
        DESCRIPTION: Log in with same credentials and observe the banner when the Policy banner is disabled in CMS
        EXPECTED: The Poicly banner should not be displayed in Frontend.
        """
        pass
