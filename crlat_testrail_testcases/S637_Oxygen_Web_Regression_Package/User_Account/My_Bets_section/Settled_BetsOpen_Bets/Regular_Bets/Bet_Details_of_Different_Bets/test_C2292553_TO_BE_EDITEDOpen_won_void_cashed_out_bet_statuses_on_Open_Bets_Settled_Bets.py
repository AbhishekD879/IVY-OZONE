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
class Test_C2292553_TO_BE_EDITEDOpen_won_void_cashed_out_bet_statuses_on_Open_Bets_Settled_Bets(Common):
    """
    TR_ID: C2292553
    NAME: [TO BE EDITED]Open/won/void/cashed out bet statuses on Open Bets/Settled Bets
    DESCRIPTION: [TO BE EDITED]:After settling results of 1 event- multiple bets with "void" & "win" results stay in the "Open Bets", only "Lose" is moved to "Settled". And these scenarios should be checked on the betslip/my bets widget on desktop too.
    DESCRIPTION: ![](index.php?/attachments/get/32613008)
    DESCRIPTION: This test case verifies showing the bet statuses
    PRECONDITIONS: 1. Login with User1
    PRECONDITIONS: 2. User1 has placed Single Bets, where
    PRECONDITIONS: - **Bet1** with **'WON'** result
    PRECONDITIONS: - **Bet2** with **'VOID'** result
    PRECONDITIONS: -  **Bet3** with **'LOSE'** result
    PRECONDITIONS: 3. User1 has placed Multiple Bets, where
    PRECONDITIONS: - **Bet4** has 1 selection with **'WON'** result
    PRECONDITIONS: - **Bet5** has 1 selection with **'VOID'** result
    PRECONDITIONS: - **Bet6** has 1 selection with **'LOSE'** result
    """
    keep_browser_open = True

    def test_001_navigate_to_my_betsopen_bets_tabverify_thatsingle_bets_with_result_are_not_shown_it_is_already_settledmultiple_bet_with_lose_result_are_not_shown_it_is_already_settledverify_that_appropriate_statuses_are_shown_for_other_multiple_bets(self):
        """
        DESCRIPTION: Navigate to My Bets>Open Bets tab
        DESCRIPTION: Verify that:
        DESCRIPTION: Single Bets with result are NOT shown (it is already Settled)
        DESCRIPTION: Multiple bet with 'LOSE' result are NOT shown (it is already Settled)
        DESCRIPTION: Verify that appropriate statuses are shown for other multiple bets
        EXPECTED: **For** **99** **Release**:
        EXPECTED: - Single bets: **Bet1, Bet2, Bet3** are NOT shown
        EXPECTED: - Multiple bet:
        EXPECTED: - 'green tick' icon is shown for one of selection in **Bet4** on the left of selection
        EXPECTED: - 'VOID' label is shown for one of selection in **Bet5** on the left of selection
        EXPECTED: - 'LOSE' label is shown for one of selection in **Bet6** on the left of selection
        EXPECTED: **For** **98** **Release**:
        EXPECTED: - Single bets: Bet1, Bet2, Bet3 are NOT shown
        EXPECTED: - Multiple bet:
        EXPECTED: - 'WON" label is shown for one of selection in Bet4
        EXPECTED: - 'VOID' label is shown for one of selection in Bet5
        EXPECTED: - 'LOSE' label is shown for one of selection in Bet6
        """
        pass

    def test_002_make_full_cash_out_for_bet4verify_that_after_successful_full_cash_out_bet4_disappeared_from_open_bets_tab(self):
        """
        DESCRIPTION: Make full cash out for **Bet4**
        DESCRIPTION: Verify that after successful full cash out **Bet4** disappeared from Open Bets tab
        EXPECTED: **Bet4** disappeared from Open Bets tab
        """
        pass

    def test_003_navigate_to_my_betssettled_betsverify_that_all_settled_bets_are_shown_with_appropriate_statuses(self):
        """
        DESCRIPTION: Navigate to My Bets>Settled Bets
        DESCRIPTION: Verify that all settled bets are shown with appropriate statuses
        EXPECTED: **For** **99** **Release**:
        EXPECTED: - **Bet1** is shown with "green tick' icon on the left of selection and 'WON' label in the header
        EXPECTED: - **Bet2** is shown with "VOID' label on the left of selection
        EXPECTED: - **Bet3** is shown with "red cross' icon on the left of selection and 'LOST' label in  the header
        EXPECTED: - **Bet6** is shown with "red cross' icon on the left of the selection and 'LOST' label in the header
        EXPECTED: - **Bet4** is shown with "CASHED OUT' label in the header
        EXPECTED: **For** **98** **Release**:
        EXPECTED: - Bet1 is shown with "WON' label near the selection and in the title
        EXPECTED: - Bet2 is shown with "VOID' label near the selection and in the title
        EXPECTED: - Bet3 is shown with "LOSE' label near the selection and in the title
        EXPECTED: - Bet6 is shown with "LOSE' label near the selection and in the title
        EXPECTED: - Bet4 is shown with "CASHED OUT' label in the title
        """
        pass
