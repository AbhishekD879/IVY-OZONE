import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C60541131_Verify_Racing_Post_Tip_display__Place_Multiple_SportsGH_and_Virtuals_Bets(Common):
    """
    TR_ID: C60541131
    NAME: Verify Racing Post Tip display - Place Multiple ,Sports,GH and Virtuals Bets
    DESCRIPTION: This test case verifies that Racing Post Tip will not be displayed when User places Multiple Bets (Accumulator , Complex ), Single Bet on any Sports, Grey Hound Racing or Virtual (Racing and Sports) , Multiple Single Bets
    PRECONDITIONS: 1: Racing Post Tip should be enabled in CMS (Main Bet Receipt and Quick Bet Receipt)
    PRECONDITIONS: 2: Tips should be available from Racing Post **upcell API should retrieve Racing Post Tip data from B2B Horses API**
    PRECONDITIONS: **Rules for Tip Display**
    PRECONDITIONS: 1: Racing Post Tip should be displayed only when User places single Horse racing Bet
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_coral(self):
        """
        DESCRIPTION: Login to Ladbrokes/ Coral
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002__add_selection_to_bet_slip_from_any_sport_and_place_single_bet_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add selection to Bet Slip from ANY SPORT and place single Bet
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_003__add_selection_from_grey_hound_racing_and_place_single_bet_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add selection from GREY HOUND Racing and place single bet
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_004__add_selection_from_virtual_sports_and_place_single_bet_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add selection from Virtual Sports and place single bet
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_005__add_selection_from_virtual_horse_racing_and_place_single_bet_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add selection from Virtual Horse Racing and place single bet
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_006__add_selection_from_virtual_grey_hound_racing_and_place_single_bet_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add selection from Virtual Grey Hound Racing and place single bet
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_007__add_2_or_more_selection_from_horse_racing_and_place_accumulator_or_complex_bet_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add 2 or more selection from Horse Racing and place Accumulator or Complex bet
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_008__add_2_or_more_selection_from_horse_racing_and_place_multiple_single_bets_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add 2 or more selection from Horse Racing and place multiple SINGLE bets
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_009__add_1_from_horse_racing_and_another_selection_from_any_sport_place_two_single_bets_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add 1 from Horse Racing and another selection from ANY Sport place two SINGLE bets
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_010__add_1_from_horse_racing_and_another_selection_from_grey_hound_racing_place_two_single_bets_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add 1 from Horse Racing and another selection from Grey Hound Racing place two SINGLE bets
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_011__add_1_from_horse_racing_and_another_selection_from_grey_hound_racing_place_two_single_bets_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add 1 from Horse Racing and another selection from Grey Hound Racing place two SINGLE bets
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_012__add_1_from_horse_racing_and_another_selection_from_virtual_horse_racing_place_two_single_bets_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add 1 from Horse Racing and another selection from Virtual Horse Racing place two SINGLE bets
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_013__add_1_from_horse_racing_and_another_selection_from_virtual_grey_hounds_racing_place_two_single_bets_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add 1 from Horse Racing and another selection from Virtual Grey Hounds Racing place two SINGLE bets
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_014__add_1_from_horse_racing_and_another_selection_from_virtual_sports_place_two_single_bets_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: * Add 1 from Horse Racing and another selection from Virtual Sports place two SINGLE bets
        DESCRIPTION: * Validate the display of Racing Post Tip
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed
        """
        pass

    def test_015_only_mobilerepeat_2__14_and_place_bets_via_quick_bet_and_validate_the_display_of_racing_post_tip_in_quick_bet_receipt(self):
        """
        DESCRIPTION: **ONLY MOBILE**
        DESCRIPTION: Repeat 2- 14 and place bets via Quick Bet and validate the display of Racing Post Tip in Quick Bet receipt
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Racing Post Tip should not be displayed in Quick Bet Receipt
        """
        pass
