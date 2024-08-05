import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C64569630_Verify_that_CMS_user_can_add_modify_Market_Titles(Common):
    """
    TR_ID: C64569630
    NAME: Verify that CMS user can add/modify Market Titles
    DESCRIPTION: This Test case verifies that CMS user can add/modify Market Titles
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin User
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_click_on_create_build_you_market(self):
        """
        DESCRIPTION: Click on Create Build You Market
        EXPECTED: * User should be able to add new markets
        """
        pass

    def test_003_click_on_any_market_and_edit(self):
        """
        DESCRIPTION: Click on any Market and Edit
        EXPECTED: * User should be able to edit the existing Market Templates
        """
        pass
