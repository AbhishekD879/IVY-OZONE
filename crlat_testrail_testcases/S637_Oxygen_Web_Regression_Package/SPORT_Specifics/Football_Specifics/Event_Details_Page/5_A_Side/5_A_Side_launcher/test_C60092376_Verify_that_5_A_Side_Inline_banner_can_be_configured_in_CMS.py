import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C60092376_Verify_that_5_A_Side_Inline_banner_can_be_configured_in_CMS(Common):
    """
    TR_ID: C60092376
    NAME: Verify that 5 A Side Inline banner can be configured in CMS
    DESCRIPTION: This test case verifies that Inline banner for 5 A side can be configured in CMS
    PRECONDITIONS: User should have admin role access to CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_navigate_to_inline_banner_configurations_for_cms(self):
        """
        DESCRIPTION: Navigate to Inline banner configurations for CMS
        EXPECTED: 1: User should be able to edit the Title and Description in CMS that populates within the banner
        EXPECTED: 2: User should be able to save the configurations
        EXPECTED: 3: User should be limited with character length (TBD)
        EXPECTED: 4: User should be able to set the position for the Inline banner
        """
        pass

    def test_003_validate_enabledisable_inline_banner(self):
        """
        DESCRIPTION: Validate enable/disable Inline banner
        EXPECTED: User should be able to enable /diable Inline banner
        """
        pass
