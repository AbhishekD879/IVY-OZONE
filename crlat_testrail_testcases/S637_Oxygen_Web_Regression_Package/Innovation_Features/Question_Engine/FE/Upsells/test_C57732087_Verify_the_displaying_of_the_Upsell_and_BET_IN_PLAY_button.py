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
class Test_C57732087_Verify_the_displaying_of_the_Upsell_and_BET_IN_PLAY_button(Common):
    """
    TR_ID: C57732087
    NAME: Verify the displaying of the Upsell and 'BET IN PLAY' button
    DESCRIPTION: This test case verifies the displaying of the Upsell and 'BET IN PLAY' button.
    PRECONDITIONS: 1. The dynamic or generic Upsell is configured in the CMS.
    PRECONDITIONS: 2. The current Event has started.
    PRECONDITIONS: 3. The Quiz is configured in the CMS.
    PRECONDITIONS: 4. The User is logged in.
    PRECONDITIONS: 5. The User has not played a Quiz yet.
    """
    keep_browser_open = True

    def test_001_tap_on_the_play_now_for_free_button(self):
        """
        DESCRIPTION: Tap on the 'Play Now For Free' button.
        EXPECTED: The User is redirected to the 1st Question page.
        """
        pass

    def test_002_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: The answer is highlighted with yellow colour.
        EXPECTED: The User is redirected to the next Question page.
        """
        pass

    def test_003_repeat_the_2nd_step_until_the_last_question_page_is_reached(self):
        """
        DESCRIPTION: Repeat the 2nd step until the last Question page is reached.
        EXPECTED: The answer is highlighted with yellow colour.
        EXPECTED: The User is redirected to the last Question page.
        """
        pass

    def test_004_select_any_answer(self):
        """
        DESCRIPTION: Select any answer.
        EXPECTED: The 'Confirm your selections!' pop-up is opened.
        """
        pass

    def test_005_tap_on_the_submit_button(self):
        """
        DESCRIPTION: Tap on the 'Submit' button.
        EXPECTED: 1. The 'Confirm your selections!' pop-up is closed.
        EXPECTED: 2. The User is navigated to the Latest tab of the Results page.
        EXPECTED: 3. The Upsell 'card' is displayed with:
        EXPECTED: - the 'BET IN PLAY' CTA
        EXPECTED: Example:
        EXPECTED: - Header: "Premier League Arsenal V Watford".
        EXPECTED: - Upsell description : "Arsenal to Win and Both teams to score".
        EXPECTED: - Ods & Return calculation : "A£10 bet returns £60" is not displayed.
        EXPECTED: - Signposting: "LIVE".
        EXPECTED: - CTA: "BET IN PLAY".
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a747488351c0b93f3
        """
        pass

    def test_006_tap_on_the_bet_in_play_button(self):
        """
        DESCRIPTION: Tap on the 'Bet in Play' button.
        EXPECTED: The User is redirected to the Event page.
        """
        pass
