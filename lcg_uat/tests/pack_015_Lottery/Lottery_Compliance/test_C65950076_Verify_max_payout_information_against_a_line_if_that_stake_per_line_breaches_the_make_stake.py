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
class Test_C65950076_Verify_max_payout_information_against_a_line_if_that_stake_per_line_breaches_the_make_stake(Common):
    """
    TR_ID: C65950076
    NAME: Verify max payout information against a line if that stake per line breaches the make stake
    DESCRIPTION: This test case is to verify max payout information against a line if that stake per line breaches the make stake
    PRECONDITIONS: Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    """
    keep_browser_open = True

    def test_001_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the Application and login with valid credentials
        EXPECTED: User should launch the Application and login Successfully
        """
        pass

    def test_002_navigate_to_lottos_page_and_select_any_lottery_by_choose_numbers_or_any_lucky_dip(self):
        """
        DESCRIPTION: Navigate to Lottos Page and Select any Lottery by choose Numbers or any Lucky Dip
        EXPECTED: Able to navigate to the Lottos page and could able to select Numbers or lucky dip
        """
        pass

    def test_003_choose_the_numbers_in_choose_numbers_pop_up_and_click_on_add_line(self):
        """
        DESCRIPTION: Choose the numbers in Choose Numbers Pop up and click on add line
        EXPECTED: Able to see the Below Info-
        EXPECTED: Added lines with chossen numbers
        EXPECTED: Avaliable Draws Information
        EXPECTED: How Many weeks INformation
        """
        pass

    def test_004_select_multiple_weeks(self):
        """
        DESCRIPTION: Select multiple weeks
        EXPECTED: able to select multiple weeks
        """
        pass

    def test_005_click_on_add_to_betslip_and_check_the_added_bets_in_betslip_page(self):
        """
        DESCRIPTION: Click on add to Betslip and check the added bets in Betslip Page
        EXPECTED: Able to add the selected lines to Betslip and can see the Bets info in Betslip for the multiple weeks
        """
        pass

    def test_006_enter_the_stake_and_verify_the_potential_returns_for_the_singles_and_multiple_bets(self):
        """
        DESCRIPTION: Enter the Stake and verify the Potential Returns for the Singles and Multiple Bets
        EXPECTED: user can able to enter the stake and can see the Potential returns
        """
        pass

    def test_007_verify_payout_at_estreturns_when_payout_is_within_max_payout(self):
        """
        DESCRIPTION: Verify payout at est.returns when payout is within max payout
        EXPECTED: user could not see the Payout limit exceeded message
        """
        pass

    def test_008_verify_max_payout_information_against_a_line_if_that_stake_per_line_breaches_the_make_stake(self):
        """
        DESCRIPTION: Verify max payout information against a line if that stake per line breaches the make stake
        EXPECTED: user can see the max payout information against a line
        """
        pass
