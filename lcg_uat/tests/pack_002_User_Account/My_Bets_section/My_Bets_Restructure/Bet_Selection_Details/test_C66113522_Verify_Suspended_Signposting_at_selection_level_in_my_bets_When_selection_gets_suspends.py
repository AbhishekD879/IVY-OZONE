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
class Test_C66113522_Verify_Suspended_Signposting_at_selection_level_in_my_bets_When_selection_gets_suspends(Common):
    """
    TR_ID: C66113522
    NAME: Verify 'Suspended' Signposting  at selection level in my bets When selection gets suspends
    DESCRIPTION: This testcase verifies 'Suspended' Signposting  at selection level in my bets When selection gets suspends
    PRECONDITIONS: Sports,Lottos,Pools bets should be available in Open ,cash out settled tab
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials_with_precondition1(self):
        """
        DESCRIPTION: Login to the application with valid credentials with precondition1
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_once_the_selection_gets_suspended_in_open_tab(self):
        """
        DESCRIPTION: Verify once the selection gets suspended in open tab
        EXPECTED: should display SUSPENDED signposting at selection level when bet is suspended
        EXPECTED: Single bets:
        EXPECTED: ![](index.php?/attachments/get/af547d71-d4e7-4c3f-9e83-b06bbe91213e)
        EXPECTED: Acca Bets:
        EXPECTED: ![](index.php?/attachments/get/1f312912-efba-4dc2-b60b-622a10225549)
        """
        pass

    def test_004_click_on_cash_out(self):
        """
        DESCRIPTION: Click on cash out
        EXPECTED: Cash out tab is opened
        """
        pass

    def test_005_verify_once_the_selection_gets_suspended_in_cash_out_tab(self):
        """
        DESCRIPTION: Verify once the selection gets suspended in Cash out tab
        EXPECTED: should display SUSPENDED signposting at selection level when bet is suspended
        """
        pass
