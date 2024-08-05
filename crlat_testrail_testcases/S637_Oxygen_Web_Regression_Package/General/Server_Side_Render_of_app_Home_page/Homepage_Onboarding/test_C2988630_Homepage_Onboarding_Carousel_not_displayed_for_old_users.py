import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C2988630_Homepage_Onboarding_Carousel_not_displayed_for_old_users(Common):
    """
    TR_ID: C2988630
    NAME: Homepage Onboarding Carousel not displayed for old users
    DESCRIPTION: This test case verifies that Onboarding carousel overlay is not displayed for old users
    PRECONDITIONS: Multiple (3) onboarding overlay configured in CMS
    PRECONDITIONS: User is not new (Or has cache)
    """
    keep_browser_open = True

    def test_001_navigate_to_oxygen_fe(self):
        """
        DESCRIPTION: Navigate to Oxygen FE
        EXPECTED: Onboarding overlay is not displayed
        """
        pass
