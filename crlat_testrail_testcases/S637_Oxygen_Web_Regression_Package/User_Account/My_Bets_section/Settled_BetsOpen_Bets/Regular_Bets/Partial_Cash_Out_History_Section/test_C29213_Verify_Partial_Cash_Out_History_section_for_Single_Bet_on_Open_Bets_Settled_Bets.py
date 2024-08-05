import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C29213_Verify_Partial_Cash_Out_History_section_for_Single_Bet_on_Open_Bets_Settled_Bets(Common):
    """
    TR_ID: C29213
    NAME: Verify 'Partial Cash Out History' section for Single Bet on Open Bets/Settled Bets
    DESCRIPTION: This test case verifies 'Partial Cash Out History' section of 'Regular' bets.
    DESCRIPTION: AUTOTEST [C41790483]
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has 'Pending' bets with available Partial Cash Out option
    PRECONDITIONS: 3. User has already made Partial Cash Out
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tabverifypartial_cash_out_history_section_presence_for_single_bet(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab
        DESCRIPTION: Verify 'Partial Cash Out History' section presence for Single bet
        EXPECTED: *   'Partial Cash Out History' section is displayed above the 'Total Estimated Returns' field
        EXPECTED: *   Section is collapsed by default
        """
        pass

    def test_002_verify_total_stakevalue(self):
        """
        DESCRIPTION: Verify **Total Stake** value
        EXPECTED: Total Stake value corresponds to the **betTermsChange.stake.value** attribute where reasonCode:"ORIGINAL_VALUES"
        EXPECTED: *   Total Stake is displayed on the section header in format: 'Remaining Stake: <currency symbol> XX.XX'
        EXPECTED: *   Total Stake is displayed next to the 'Total Stake' field in format: '<currency symbol> XX.XX'
        """
        pass

    def test_003_verify_stakevalue(self):
        """
        DESCRIPTION: Verify **Stake** value
        EXPECTED: Stake value corresponds to **stake.value **(from the core of 'accountHistory' response)
        EXPECTED: *   Stake is displayed next to the 'Stake' field in format: '<currency symbol> X.XX'
        """
        pass

    def test_004_verify_partial_cash_out_history_section_content(self):
        """
        DESCRIPTION: Verify 'Partial Cash Out History' section content
        EXPECTED: 'Partial Cash Out History' section contains:
        EXPECTED: *   Table with 'Stake Used', 'Cash Out Amount' and 'Date/Time' values
        EXPECTED: *   'Remaining Stake', 'Total Cashed Out' and 'Total Cashed Out Stake' fields and corresponding values
        """
        pass

    def test_005_verify_correctness_of_table_data(self):
        """
        DESCRIPTION: Verify correctness of table data
        EXPECTED: *   **Stake Used** = number of line in table **betTermsChange [i-1].stake.value - betTermsChange[i].stake.value** (value is shown in format:  '<currency symbol> XX.XX')
        EXPECTED: *   **Cash Out Amount =** amount of partial cash out. Corresponds to ****betTermsChange.**cashoutValue** attribute and is shown in format:  '<currency symbol> XX.XX'
        EXPECTED: *   **Date/Time** - time of partial cash out transaction. Corresponds to **betTermsChange.cashoutDate** value. Is shown in format: YYYY-MM-DD HH:MM:SS
        """
        pass

    def test_006_verify_correctness_of_remaining_stake_total_cashed_out_and_total_cashed_out_stake_values(self):
        """
        DESCRIPTION: Verify correctness of 'Remaining Stake', 'Total Cashed Out' and 'Total Cashed Out Stake' values
        EXPECTED: *   **Remaining Stake** = betTermsChange [i].stake.value
        EXPECTED: *   **Total Cashed Out **= sum of 'Cash Out Amount' fields
        EXPECTED: *   **Total Cashed Out Stake** = sum of 'Stake Used' fields
        EXPECTED: All values are shown in format: '<currency symbol> XX.XX'
        """
        pass

    def test_007_make_partial_cash_out_of_verified_betverify_that_partial_cash_out_history_sectionis_increased_by_one_row(self):
        """
        DESCRIPTION: Make Partial Cash out of verified bet
        DESCRIPTION: Verify that 'Partial Cash Out History' section is increased by one row
        EXPECTED: - Partial Cash Out transaction has been successful
        EXPECTED: - Table within 'Partial Cash Out History' section is increased by one row
        EXPECTED: - Appropriate partial cash out information is shown within the 'Partial Cash Out History' section
        """
        pass

    def test_008_make_a_full_cash_out_of_the_verified_betnavigate_to_the_settled_bets_tabverify_that_appropriate_information_for_partial_cash_out_is_shown_in_partial_cash_out_history_section_same_as_in_step_7(self):
        """
        DESCRIPTION: Make a Full Cash Out of the verified bet
        DESCRIPTION: Navigate to the 'Settled Bets' tab
        DESCRIPTION: Verify that appropriate information for Partial Cash Out is shown in "Partial Cash Out History' section (same as in Step 7)
        EXPECTED: Appropriate information for Partial Cash Out is shown in "Partial Cash Out History' section on 'Settled Bets' tab
        """
        pass
