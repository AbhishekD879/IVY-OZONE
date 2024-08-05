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
class Test_C18753269_Verify_My_Bets_counter_after_Edit_My_acca(Common):
    """
    TR_ID: C18753269
    NAME: Verify My Bets counter after Edit My acca
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after user edits acca on My Bets page
    PRECONDITIONS: - Load Oxygen/Roxanne Application
    PRECONDITIONS: - Make sure user has open(unsettled) bets with edit my acca available ( for multiples)
    PRECONDITIONS: - Make sure My bets counter config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_or_my_bets_tabpage(self):
        """
        DESCRIPTION: Navigate to 'Cash out' or 'My Bets' tab/page
        EXPECTED: 'Cash Out'/'My Bets' tab/page is opened
        """
        pass

    def test_002__select_edit_my_acca_and_delete_one_or_more_selections_confirm_changes(self):
        """
        DESCRIPTION: * Select edit my acca and delete one or more selections
        DESCRIPTION: * Confirm changes
        EXPECTED: Bet is modified
        """
        pass

    def test_003_check_my_bets_counter_on_footer_remains_the_same(self):
        """
        DESCRIPTION: Check my bets counter on Footer remains the same
        EXPECTED: My bets counter didn't change
        """
        pass

    def test_004_repeat_steps_1_3_for_another_bet_with_edit_my_acca_available(self):
        """
        DESCRIPTION: Repeat steps #1-3 for another bet with edit my acca available
        EXPECTED: Results are the same
        """
        pass
