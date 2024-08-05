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
class Test_C65950034_Verify_payout_for_different_stakes_within_max_payout(Common):
    """
    TR_ID: C65950034
    NAME: Verify payout  for different stakes within max payout
    DESCRIPTION: This testcase verifies payout  for different stakes within max payout
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
        EXPECTED: Able to choose numbers and could able to add the line and navigated to Line Summary page
        """
        pass

    def test_004_verify_the_line_summary_page(self):
        """
        DESCRIPTION: Verify the Line Summary Page
        EXPECTED: Able to see the Below Info-
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: Added lines with chossen numbers
        """
        pass

    def test_006_(self):
        """
        DESCRIPTION: 
        EXPECTED: Avaliable Draws Information
        """
        pass

    def test_007_(self):
        """
        DESCRIPTION: 
        EXPECTED: How Many weeks INformation
        """
        pass

    def test_008_click_on_add_to_betslip_and_check_the_added_bets_in_betslip_page(self):
        """
        DESCRIPTION: Click on add to Betslip and check the added bets in Betslip Page
        EXPECTED: Able to add the selected lines to Betslip and can see the Bets info in Betslip
        """
        pass

    def test_009_enter_different_stakes_and_verify_the_payout_message(self):
        """
        DESCRIPTION: Enter different stakes and verify the payout message
        EXPECTED: user can able to enter and alter different stakes and can see the Potential returns
        """
        pass

    def test_010_verify_payout_at_estreturns_when_payout_exceeds_max_payout(self):
        """
        DESCRIPTION: Verify payout at est.returns when payout exceeds max payout
        EXPECTED: user could see the Payout limit exceeded message
        """
        pass

    def test_011_verify_the_max_payout_information_area_to_be_displayed_above_the_total_stake_and_returns_area_near_placebet_button(self):
        """
        DESCRIPTION: Verify the max payout information area to be displayed above the Total Stake and Returns area near placebet button
        EXPECTED: Message is displaying above the Total Stake and Returns area near placebet button
        """
        pass
