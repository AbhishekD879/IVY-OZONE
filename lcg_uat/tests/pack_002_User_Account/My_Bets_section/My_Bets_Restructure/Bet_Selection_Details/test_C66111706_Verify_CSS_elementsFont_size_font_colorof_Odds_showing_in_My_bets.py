import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66111706_Verify_CSS_elementsFont_size_font_colorof_Odds_showing_in_My_bets(Common):
    """
    TR_ID: C66111706
    NAME: Verify CSS elements(Font size, font color)of Odds showing in My bets
    DESCRIPTION: This testcase verifies CSS elements(Font size, color) of Odds showing at selection level in my bets
    PRECONDITIONS: Sports,Lottos,Pools bets should be available in Open ,cash out settled tab
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_odds_displayed_for_the_bets_in_open_tab(self):
        """
        DESCRIPTION: Verify Odds displayed for the bets in Open tab
        EXPECTED: Font size ,font colour should be as per figma
        EXPECTED: ![](index.php?/attachments/get/98b86d48-8cd9-4b65-becf-41d50498a7bf)
        """
        pass

    def test_004_verify_odds_displayed_for_the_bets_in_cash_out_tab(self):
        """
        DESCRIPTION: Verify Odds displayed for the bets in Cash out tab
        EXPECTED: Font size,font color should be as per figma
        """
        pass

    def test_005_verify_odds_displayed_for_the_bets_in_settled_tab(self):
        """
        DESCRIPTION: Verify Odds displayed for the bets in Settled tab
        EXPECTED: Font size,font color should be as per figma
        """
        pass

    def test_006_repeat_step_4_6__by_placing_bets_for_tier1_and_tier2_sports(self):
        """
        DESCRIPTION: Repeat step 4-6  by placing bets for tier1 and tier2 Sports
        EXPECTED: Result should be same
        """
        pass

    def test_007_repeat_step_4_6_by_placing_multiple_bets_and_complex_bets(self):
        """
        DESCRIPTION: Repeat step 4-6 by placing multiple bets and complex bets
        EXPECTED: Result should be same
        """
        pass

    def test_008_repeat_step_4_6_for_lotto_bets(self):
        """
        DESCRIPTION: Repeat step 4-6 for lotto bets
        EXPECTED: Result should be same
        """
        pass

    def test_009_repeat_step_4_6_fot_pools(self):
        """
        DESCRIPTION: Repeat step 4-6 fot pools
        EXPECTED: Result should be same
        """
        pass
