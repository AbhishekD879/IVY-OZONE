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
class Test_C15358884_Verify_Vanilla_Unplug_gamecare_certified_functionality(Common):
    """
    TR_ID: C15358884
    NAME: Verify [Vanilla] Unplug gamecare-certified functionality
    DESCRIPTION: 1)remove 'gamecare-certified' route from vanilla app-routing.module
    DESCRIPTION: 2) */gamecare-certified page should not be available in vanilla app
    DESCRIPTION: 3) GameCareCertifiedComponent should be unplugged from bma module
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

    def test_002_navigate_via_link_url_plus_gamecare_certified(self):
        """
        DESCRIPTION: Navigate via link "url" + */gamecare-certified
        EXPECTED: Verify user is redirected to a home page
        """
        pass

    def test_003_click_gamcare_logo_at_the_footerindexphpattachmentsget31291_orindexphpattachmentsget31292(self):
        """
        DESCRIPTION: Click GamCare logo at the footer
        DESCRIPTION: ![](index.php?/attachments/get/31291) or
        DESCRIPTION: ![](index.php?/attachments/get/31292)
        EXPECTED: Verify user is redirected to :
        EXPECTED: https://www.gamcare.org.uk/
        """
        pass
