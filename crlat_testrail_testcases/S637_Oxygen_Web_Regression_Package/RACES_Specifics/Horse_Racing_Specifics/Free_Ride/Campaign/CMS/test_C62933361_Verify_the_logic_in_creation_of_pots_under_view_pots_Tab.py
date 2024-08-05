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
class Test_C62933361_Verify_the_logic_in_creation_of_pots_under_view_pots_Tab(Common):
    """
    TR_ID: C62933361
    NAME: Verify the logic in creation of pots under view pots Tab
    DESCRIPTION: This test case verifies the logic in creation of pots under view pots Tab
    PRECONDITIONS: 1: User should be logged into oxygen CMS with admin access
    PRECONDITIONS: 2: Campaign and pots should be created successfully
    """
    keep_browser_open = True

    def test_001_navigate_to_view_pots_tab(self):
        """
        DESCRIPTION: Navigate to View Pots Tab
        EXPECTED: Below data should be displayed in view Pots Tab
        EXPECTED: * Pots 1-8 should be displayed
        EXPECTED: * Pots Table should consists of pots (1-8), Rating, Weight, Odds information
        """
        pass

    def test_002_collect_the_horse_characteristics_like_rating_weight_and_odds_from_racing_post(self):
        """
        DESCRIPTION: Collect the horse characteristics like rating, weight and odds from racing post
        EXPECTED: Horse information like rating, weight and odds should be collected
        """
        pass

    def test_003_arrange_the_horses_in_a_chronological_order_based_on_rating(self):
        """
        DESCRIPTION: Arrange the horses in a chronological order based on rating
        EXPECTED: Horses should be arranged in a chronological order based on rating (highest to lowest)
        """
        pass

    def test_004_divide_the_above_arranged_horses_into_two_halves(self):
        """
        DESCRIPTION: Divide the above arranged horses into two halves
        EXPECTED: * First half should be treated as 'Top player'
        EXPECTED: * Second half should be treated as 'Dark Horse'
        """
        pass

    def test_005_arrange_the_top_player_horses_into_chronological_order_based_on_the_weight(self):
        """
        DESCRIPTION: Arrange the 'Top player' horses into chronological order based on the weight
        EXPECTED: All the 'Top player' horses should be arranged in chronological order based on weight
        """
        pass

    def test_006_from_the_step5_result_divide_the_top_player_horses_into_two_halves(self):
        """
        DESCRIPTION: From the step5 result, divide the 'Top player' horses into two halves
        EXPECTED: * First half should be treated as 'Top Player + Big & Strong'
        EXPECTED: * Second half should be treated as 'Top Player + Small & Nimble'
        """
        pass

    def test_007_arrange_the_dark_horse_into_chronological_order_based_on_the_weight(self):
        """
        DESCRIPTION: Arrange the 'Dark horse' into chronological order based on the weight
        EXPECTED: All the Dark horses should be arranged in chronological order based on weight
        """
        pass

    def test_008_from_the_step7_result_divide_the_dark_horse_horses_into_two_halves(self):
        """
        DESCRIPTION: From the step7 result, divide the 'Dark Horse' horses into two halves
        EXPECTED: * First half should be treated as 'Dark Horse + Big & Strong'
        EXPECTED: * Second half should be treated as 'Dark Horse + Small & Nimble'
        """
        pass

    def test_009_from_step6_result_arrange_the_top_player_plus_big__strong_horses_in_chronological_order_based_on_odds_lowest_to_highest(self):
        """
        DESCRIPTION: From step6 result Arrange the 'Top Player + Big & Strong' horses in chronological order based on odds (lowest to highest)
        EXPECTED: All the 'Top Player + Big & Strong' horses should be arranged in chronological order based on odds(lowest to highest)
        EXPECTED: Note:
        EXPECTED: * If any horse is having 'SP' then it should be treated as lowest odd
        EXPECTED: * Unnamed favorites and Non-runner horses should not be considered
        """
        pass

    def test_010_from_step9_divide_top_player_plus_big__strong_horses_list_in_to_two_halves(self):
        """
        DESCRIPTION: From step9 divide 'Top Player + Big & Strong' horses list in to two halves
        EXPECTED: * First half should be treated as 'Top Player + Big & Strong + Good chance'
        EXPECTED: * Second half should be treated as 'Top Player + Big & Strong + Nice Price'
        EXPECTED: Note:
        EXPECTED: * Since 'SP' horses are considered as lowest odd, so these will appear in the lowest pot category
        EXPECTED: * Top Player + Big & Strong + Nice Price
        """
        pass

    def test_011_from_step6_result_arrange_the_top_player_plus_small__nimble_horses_in_chronological_order_based_on_odds_lowest_to_highest(self):
        """
        DESCRIPTION: From step6 result Arrange the 'Top Player + Small & Nimble" horses in chronological order based on odds (lowest to highest)
        EXPECTED: All the 'Top Player + Small & Nimble" horses should be arranged in chronological order based on odds(lowest to highest)
        EXPECTED: Note:
        EXPECTED: * If any horse is having 'SP' then it should be treated as lowest odd
        EXPECTED: * Unnamed favorites and Non-Runner horses should not be considered
        """
        pass

    def test_012_from_step11_divide_top_player_plus_small__nimble_horses_list_into_two_halves(self):
        """
        DESCRIPTION: From step11 divide 'Top Player + Small & Nimble" horses list into two halves
        EXPECTED: * First half should be treated as 'Top Player + Small & Nimble + Good chance'
        EXPECTED: * Second half should be treated as 'Top Player + Small & Nimble + Nice Price'
        EXPECTED: Note:
        EXPECTED: * Since 'SP' horses are considered as lowest odd, so these will appear in the lowest pot category
        EXPECTED: * Top Player + Small & Nimble + Nice Price
        """
        pass

    def test_013_from_step8_result_arrange_the_dark_horse_plus_big__strong_horses_in_chronological_order_based_on_odds_lowest_to_highest(self):
        """
        DESCRIPTION: From step8 result Arrange the 'Dark Horse + Big & Strong" horses in chronological order based on odds (lowest to highest)
        EXPECTED: All the 'Dark Horse + Big & Strong' horses should be arranged in chronological order based on odds(lowest to highest)
        EXPECTED: Note:
        EXPECTED: * If any horse is having 'SP' then it should be treated as lowest odd
        EXPECTED: * Unnamed favorites and Non-Runner horses should not be considered
        """
        pass

    def test_014_from_step13_divide_dark_horse_plus_big__strong_horses_list_in_to_two_halves(self):
        """
        DESCRIPTION: From step13 divide 'Dark Horse + Big & Strong' horses list in to two halves
        EXPECTED: First half should be treated as 'Dark horses + Big & Strong + Good chance'
        EXPECTED: Second half should be treated as 'Dark horses + Big & Strong + Nice Price'
        EXPECTED: Note:
        EXPECTED: * Since 'SP' horses are considered as lowest odd, so these will appear in the lowest pot category
        EXPECTED: * Dark horses + Big & Strong + Nice Price
        """
        pass

    def test_015_from_step8_result_arrange_the_dark_horse_plus_small__nimble_horses_in_chronological_order_based_on_odds_lowest_to_highest(self):
        """
        DESCRIPTION: From step8 result Arrange the 'Dark Horse + Small & Nimble" horses in chronological order based on odds (lowest to highest)
        EXPECTED: All the 'Dark Horse + Small & Nimble' horses should be arranged in chronological order based on odds(lowest to highest)
        EXPECTED: note:
        EXPECTED: * If any horse is having 'SP' then it should be treated as lowest odd
        EXPECTED: * Unnamed favorites and Non-Runner horses should not be considered
        """
        pass

    def test_016_from_step15_divide_dark_horse_plus_small__nimble_horses_list_into_two_halves(self):
        """
        DESCRIPTION: from step15 divide 'Dark Horse + Small & Nimble' horses list into two halves
        EXPECTED: First half should be treated as 'Dark Horse + Small & Nimble + Good chance'
        EXPECTED: Second half should be treated as 'Dark Horse + Small & Nimble + Nice Price'
        EXPECTED: Note:
        EXPECTED: * Since 'SP' horses are considered as lowest odd, so these will appear in the lowest pot category
        EXPECTED: * Dark Horse + Small & Nimble + Nice Price
        """
        pass

    def test_017_verify_the_8_created_pots(self):
        """
        DESCRIPTION: Verify the 8 created pots
        EXPECTED: Below 8 pots should be created
        EXPECTED: * Pot 1: Top Player + Big & Strong + Good Chance
        EXPECTED: * Pot 2: Top Player + Big & Strong + Nice Price
        EXPECTED: * Pot 3:Top Player + Small & Nimble + Good Chance
        EXPECTED: * Pot 4: Top Player + Small & Nimble + Nice Price
        EXPECTED: * Pot 5: Dark Horse+ Big & Strong + Good Chance
        EXPECTED: * Pot 6: Dark Horse + Big & Strong + Nice Price
        EXPECTED: * Pot 7: Dark Horse + Small & Nimble + Good Chance
        EXPECTED: * Pot 8: Dark Horse + Small & Nimble + Nice Price
        """
        pass
