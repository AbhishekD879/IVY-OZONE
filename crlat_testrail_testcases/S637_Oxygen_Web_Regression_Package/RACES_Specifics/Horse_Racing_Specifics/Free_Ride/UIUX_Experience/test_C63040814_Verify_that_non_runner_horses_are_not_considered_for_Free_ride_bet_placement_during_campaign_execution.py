import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C63040814_Verify_that_non_runner_horses_are_not_considered_for_Free_ride_bet_placement_during_campaign_execution(Common):
    """
    TR_ID: C63040814
    NAME: Verify that non runner horses are not considered for Free ride bet placement during campaign execution
    DESCRIPTION: This test case verifies that non runner horses are not considered for Free ride bet placement during campaign execution
    PRECONDITIONS: 1: Campaign should be currently running
    PRECONDITIONS: 2: Pots should be created successfully
    PRECONDITIONS: 3: Make one of the horse as Non runner in OB for the current pot selection in CMS
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
        EXPECTED: Bet should be placed successfully and it should not contain Non Runner horses
        """
        pass

    def test_006_repeat_step_1_4_with_different_users(self):
        """
        DESCRIPTION: Repeat step 1-4 with different users
        EXPECTED: Bet should be placed successfully and it should not contain Non Runner horses
        """
        pass

    def test_007_repeat_steps_1_6_for_the_below_potspot_2_top_player_plus_big__strong_plus_nice_pricepot_3top_player_plus_small__nimble_plus_good_chancepot_4_top_player_plus_small__nimble_plus_nice_pricepot_5_dark_horseplus_big__strong_plus_good_chancepot_6_dark_horse_plus_big__strong_plus_nice_pricepot_7_dark_horse_plus_small__nimble_plus_good_chancepot_8_dark_horse_plus_small__nimble_plus_nice_price(self):
        """
        DESCRIPTION: Repeat steps 1-6 for the below pots
        DESCRIPTION: Pot 2: Top Player + Big & Strong + Nice Price
        DESCRIPTION: Pot 3:Top Player + Small & Nimble + Good Chance
        DESCRIPTION: Pot 4: Top Player + Small & Nimble + Nice Price
        DESCRIPTION: Pot 5: Dark Horse+ Big & Strong + Good Chance
        DESCRIPTION: Pot 6: Dark Horse + Big & Strong + Nice Price
        DESCRIPTION: Pot 7: Dark Horse + Small & Nimble + Good Chance
        DESCRIPTION: Pot 8: Dark Horse + Small & Nimble + Nice Price
        EXPECTED: 
        """
        pass
