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
class Test_C64256396_Verify_QE_by_adding_quiz_selections_to_the_betslip(Common):
    """
    TR_ID: C64256396
    NAME: Verify QE  by adding quiz selections to the betslip.
    DESCRIPTION: Verify QE  by adding quiz selections to the betslip.
    PRECONDITIONS: * Coral:-
    PRECONDITIONS: Question Engine quiz should be available in Front End.
    """
    keep_browser_open = True

    def test_001_navigate_to_question_engine__play_the_quiz_in_coral(self):
        """
        DESCRIPTION: Navigate to Question Engine & play the quiz in Coral
        EXPECTED: * QE quiz page is opened & user able to play quiz
        """
        pass

    def test_002_user_submit_quiz(self):
        """
        DESCRIPTION: User 'Submit' quiz
        EXPECTED: *The 'Confirm your selections!' pop-up is closed.
        EXPECTED: *The User is navigated to the Latest tab of the Results page.
        EXPECTED: *The Upsell 'card' is displayed with:
        EXPECTED: the 'BET NOW' CTA
        EXPECTED: *signposting as per the attached design
        EXPECTED: *Example:
        EXPECTED: Header: "Premier League Arsenal V Watford".
        EXPECTED: Upsell description : "Arsenal to Win and Both teams to score".
        EXPECTED: Odds & Return calculation : "A£10 bet returns £60".
        EXPECTED: Signposting: n/a.
        EXPECTED: CTA: "BET NOW".
        """
        pass

    def test_003_tap_on_the_bet_now_button(self):
        """
        DESCRIPTION: Tap on the 'BET NOW' button.
        EXPECTED: * User is redirected to the enhanced Betslip page with a possibility to place a bet.
        """
        pass
