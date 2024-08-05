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
class Test_C64569634_Verify_that_if_CMS_user_does_not_mark_Market_under_any_filter_then_those_Markets_should_be_displayed_under_All_Markets(Common):
    """
    TR_ID: C64569634
    NAME: Verify that if CMS user does not mark Market under any filter then those Markets should be displayed under 'All Markets'
    DESCRIPTION: Verify that if CMS user does not mark Market under any filter then those Markets should be displayed under 'All Markets'
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
        EXPECTED: User should be able to add new markets
        """
        pass

    def test_003_dont_mark_above_created_market_under_any_other_filters(self):
        """
        DESCRIPTION: Don't mark above created market under any other filters
        EXPECTED: The market should be present under All markets section.
        """
        pass
