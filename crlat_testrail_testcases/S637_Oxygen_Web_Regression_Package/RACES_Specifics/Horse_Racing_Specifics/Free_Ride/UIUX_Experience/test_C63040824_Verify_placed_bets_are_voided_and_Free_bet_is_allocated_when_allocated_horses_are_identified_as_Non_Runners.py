import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C63040824_Verify_placed_bets_are_voided_and_Free_bet_is_allocated_when_allocated_horses_are_identified_as_Non_Runners(Common):
    """
    TR_ID: C63040824
    NAME: Verify placed bets are voided and Free bet is allocated when allocated horses are identified as Non Runners
    DESCRIPTION: This test case verifies that  placed bets are voided and Free bet is allocated when allocated horses are identified as Non Runners
    PRECONDITIONS: 1. Campaign should be currently running
    PRECONDITIONS: 2. Pots should be created successfully
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application_with_eligible_customer(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible customer
        EXPECTED: User should be able to login successfully and Free Ride Banner should be displayed
        """
        pass

    def test_002_click_on_launch_free_ride_banner_in_homepage(self):
        """
        DESCRIPTION: Click on 'Launch Free Ride Banner' in Homepage
        EXPECTED: Splash page with CTA button should be displayed
        """
        pass

    def test_003_click_on_cta_button_in_splash_page(self):
        """
        DESCRIPTION: Click on CTA button in Splash Page
        EXPECTED: Free Ride overlay should be displayed
        """
        pass

    def test_004_select_pot1_combinations_by_using_sub_sequent_questions(self):
        """
        DESCRIPTION: Select Pot1 combinations by using sub sequent questions
        EXPECTED: User should select below options for the sub sequent questions
        EXPECTED: 'Top Player' for question1
        EXPECTED: 'Big & Strong' for question2
        EXPECTED: 'Good Chance' for question3
        """
        pass

    def test_005_verify_free_ride_bet_is_placed_automatically(self):
        """
        DESCRIPTION: Verify Free Ride bet is placed automatically
        EXPECTED: Bet should be placed successfully
        """
        pass

    def test_006_make_the_allocated_horse_as_non_runner_in_ob(self):
        """
        DESCRIPTION: Make the allocated horse as Non Runner in OB
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_my_bets__gt_open_bets(self):
        """
        DESCRIPTION: Navigate to My Bets -&gt; Open bets
        EXPECTED: Earlier placed Free Ride bet should be voided
        """
        pass

    def test_008_navigate_to_my_account__gt_free_bet_section(self):
        """
        DESCRIPTION: Navigate to My Account -&gt; Free bet section
        EXPECTED: Free Ride Free bet should be allocated
        """
        pass
