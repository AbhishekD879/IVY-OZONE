import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C62162603_Verify_Link_Title_Add_Link_Redirection_URLinside_the_Tooltip_Text__CMS(Common):
    """
    TR_ID: C62162603
    NAME: Verify Link Title & Add Link (Redirection URL)inside the Tooltip Text - CMS
    DESCRIPTION: This test Case verifies adding Link Title and redirection URL for Terms and Conditions in Max Pay Out Banner
    PRECONDITIONS: User should have CMS admin access
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as Admin user
        EXPECTED: Login should be successful
        """
        pass

    def test_002_navigate_to_system_config__structure_maxpayout(self):
        """
        DESCRIPTION: Navigate to System Config -Structure-Maxpayout
        EXPECTED: Link Title and URL should be displayed
        """
        pass

    def test_003_add_link_title_and_url(self):
        """
        DESCRIPTION: Add Link Title and URL
        EXPECTED: 
        """
        pass

    def test_004_in_fe_trigger_max_payout_banner_in_quick_bet_or_bet_slipvalidate_the_link_title_and_redirection_url(self):
        """
        DESCRIPTION: In FE trigger Max Payout banner in Quick Bet or Bet Slip
        DESCRIPTION: Validate the Link Title and Redirection URL
        EXPECTED: * Link Title should be displayed as configured in CMS
        EXPECTED: * Click on the Link- User should be redirected to the page as configured in CMS
        """
        pass
