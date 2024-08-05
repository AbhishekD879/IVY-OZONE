import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C15385464_Verify_Vanilla_Unplug_self_exclusion_functionality(Common):
    """
    TR_ID: C15385464
    NAME: Verify [Vanilla] Unplug self-exclusion functionality
    DESCRIPTION: 1. remove 'self-exclusion' route from vanilla app-routing.module
    DESCRIPTION: 2. */self-exclusion page should not be available in vanilla app
    DESCRIPTION: 3. SelfExclusionLogoutComponent, SelfExclusionDialogComponent, SelfExclusionComponent should be unplugged from bma module
    DESCRIPTION: all *.less related styles should be removed (check index.less file for related styles)
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: Example of credentials :
    PRECONDITIONS: login:ukmigct-tstEUR02
    PRECONDITIONS: password: 123123
    """
    keep_browser_open = True

    def test_001_login_to_test_environment(self):
        """
        DESCRIPTION: Login to test environment
        EXPECTED: Successful login
        """
        pass

    def test_002_navigate_via_link_url_plus_self_exclusion(self):
        """
        DESCRIPTION: Navigate via link "url" + /self-exclusion
        EXPECTED: Verify user is redirected to a home page
        """
        pass

    def test_003_verify_that_self_exclusion_link_is_no_longer_available_on_home_page(self):
        """
        DESCRIPTION: Verify that self-exclusion link is no longer available on home page
        EXPECTED: Self-exclusion link is no longer available on home page
        """
        pass
