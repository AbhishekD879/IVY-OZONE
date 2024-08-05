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
class Test_C64569633_Verify_that_if_CMS_user_marks_any_market_under_Team_Bets_filter_and_checks_Popular_Markets_checkbox_those_markets_should_be_displayed_under_All_Markets_Team_Bets_Popular_Markets_tab(Common):
    """
    TR_ID: C64569633
    NAME: Verify that if CMS user marks any market under Team Bets filter and checks Popular Markets checkbox those markets should be displayed under All Markets , Team Bets , Popular Markets tab
    DESCRIPTION: Verify that if CMS user marks any market under Team Bets filter and checks Popular Markets checkbox those markets should be displayed under All Markets , Team Bets , Popular Markets tab
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

    def test_003_mark_the_above_created_market_under_team_bets_select_the_team_bets_from_type_dropdown_in_cms(self):
        """
        DESCRIPTION: Mark the above created market under Team Bets [Select the Team Bets from Type dropdown in CMS]
        EXPECTED: In FE, The market should also be present under Team Bets filter AND Under All Markets filter
        """
        pass

    def test_004_now_select_the_popular_markets_checkbox_in_cms(self):
        """
        DESCRIPTION: Now, Select the Popular Markets checkbox in CMS
        EXPECTED: In FE, The market should also be present under Popular Markets filter AND Under All Markets filter and Team Bets Filter
        """
        pass
