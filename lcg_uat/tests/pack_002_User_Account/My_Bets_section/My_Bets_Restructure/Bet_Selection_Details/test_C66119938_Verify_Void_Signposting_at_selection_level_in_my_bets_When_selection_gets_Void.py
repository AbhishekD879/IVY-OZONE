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
class Test_C66119938_Verify_Void_Signposting_at_selection_level_in_my_bets_When_selection_gets_Void(Common):
    """
    TR_ID: C66119938
    NAME: Verify 'Void' Signposting at selection level in my bets When selection gets Void
    DESCRIPTION: This testcase verifies 'Void' Signposting at selection level in my bets When selection gets Void
    PRECONDITIONS: Sports,Pools bets should be available in Open ,cash out settled tab
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

    def test_003_verify_once_the_selection_gets_void_in_open_tab_for_single_bets(self):
        """
        DESCRIPTION: Verify once the selection gets void in open tab for single bets
        EXPECTED: should display Void signposting at selection level when bet is void
        EXPECTED: Single Bets:
        EXPECTED: ![](index.php?/attachments/get/49d36154-20b6-441f-83b2-8a4dd5a73036)
        """
        pass

    def test_004_verify_void_signposting_for_acca_bets(self):
        """
        DESCRIPTION: Verify void signposting for Acca Bets
        EXPECTED: should display Void signposting at selection level when bet is void
        EXPECTED: ![](index.php?/attachments/get/8547c7e2-73fe-4765-a1bb-9e8ff4b5ce60)
        """
        pass

    def test_005_repeat_step4_and_step5_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat step4 and step5 in cash out tab
        EXPECTED: Result should be same
        """
        pass

    def test_006_repeat_step4_and_step5_in_settled_tab(self):
        """
        DESCRIPTION: Repeat step4 and step5 in Settled tab
        EXPECTED: Result should be same
        """
        pass
