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
class Test_C64293348_Verify_1_2_free_by_adding_quiz_selections_to_the_betslip(Common):
    """
    TR_ID: C64293348
    NAME: Verify 1-2 free by adding quiz selections to the betslip.
    DESCRIPTION: Verify 1-2 free by adding quiz selections to the betslip.
    PRECONDITIONS: * Ladbrokes:-
    PRECONDITIONS: 1-2 free quiz should be available in Front End.
    """
    keep_browser_open = True

    def test_001_navigate_to_1_2_free_quiz_and_play_the_quiz_in_ladbrokes(self):
        """
        DESCRIPTION: Navigate to 1-2 free quiz and play the quiz in Ladbrokes
        EXPECTED: * 1-2 free quiz page is opened & user able to play quiz
        """
        pass

    def test_002_user_submit_predictions(self):
        """
        DESCRIPTION: User 'Submit' predictions
        EXPECTED: * Quiz is submitted then 'You are in' page opened successfully
        """
        pass

    def test_003_swipe_the_carousel_block(self):
        """
        DESCRIPTION: Swipe the carousel block
        EXPECTED: * User able to swipes left/right  of carousel block
        EXPECTED: * Carousel block contains combination of  bets related to particular market with some information based on quiz submitted. For example carousel block 'Treble:
        EXPECTED: Both Teams to Score (BTTS)' with:
        EXPECTED: Title
        EXPECTED: Matches with BTTS Yes/No information
        EXPECTED: Odds information
        EXPECTED: 'Add To Slip' button
        """
        pass

    def test_004_add_all_selections_which_are_available_in_the_carousel_block(self):
        """
        DESCRIPTION: Add all selections which are available in the carousel block
        EXPECTED: * In enhanced betslip scroll bar does not introduced up to 4 selections & Betslip size is going to increase dynamically irrespective of lengthy selection names but won't see multiples here.
        EXPECTED: * If betslip is added with more than 4 selections then Scroll bar introduces here with the previous selections betslip size.
        """
        pass
