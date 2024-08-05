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
class Test_C64293336_Verify_the_configurations_for_IMGscoreboard_in_CMS(Common):
    """
    TR_ID: C64293336
    NAME: Verify the configurations for IMGscoreboard in CMS
    DESCRIPTION: This tc verifies the functioning of IMG LB toggles in CMS
    PRECONDITIONS: User should have admin access to CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_cms_system_configuration__structure_and_search_for_imgscoreboard_and_imgscoreboardsports(self):
        """
        DESCRIPTION: Navigate to CMS> System Configuration > Structure and search for IMGScoreboard and IMGScoreboardsports
        EXPECTED: 
        """
        pass

    def test_003_validate_the_user_is_able_to_enabledisable_and_save_the_changes_successfully(self):
        """
        DESCRIPTION: Validate the User is able to enable/disable and save the changes successfully
        EXPECTED: CMS toggles are functional
        """
        pass
