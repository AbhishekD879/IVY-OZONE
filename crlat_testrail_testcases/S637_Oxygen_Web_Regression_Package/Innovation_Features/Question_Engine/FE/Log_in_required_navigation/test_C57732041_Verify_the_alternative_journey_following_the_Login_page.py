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
class Test_C57732041_Verify_the_alternative_journey_following_the_Login_page(Common):
    """
    TR_ID: C57732041
    NAME: Verify the alternative journey following the Login page
    DESCRIPTION: This test case verifies the alternative journey following the Login page.
    PRECONDITIONS: From the Splash page:
    PRECONDITIONS: 1. The CMS has been configured as 'Log in to view' (the 'START' option is selected in the 'Login rule' field).
    PRECONDITIONS: 2. The User is logged out.
    PRECONDITIONS: 3. Tap on the CTA to start the quiz (Log in to Play for free).
    PRECONDITIONS: 4. Enter valid credentials.
    PRECONDITIONS: 5. The existing 'After log in' pop-ups are displayed (Odds Boost/Quick Deposit).
    PRECONDITIONS: From the the 'Submit' pop-up:
    PRECONDITIONS: 1. The CMS has been configured as 'Log in to submit' (the 'SUBMIT' option is selected in the 'Login rule' field).
    PRECONDITIONS: 2. The User is logged out.
    PRECONDITIONS: 3. Answer on the questions in a quiz.
    PRECONDITIONS: 4. Tap on the submit CTA (Log in to submit).
    PRECONDITIONS: 5. Enter valid credentials.
    PRECONDITIONS: 6. The existing 'After log in' pop-ups are displayed (Odds Boost/Quick Deposit).
    """
    keep_browser_open = True

    def test_001_tap_on_the_show_more_cta_button_in_the_odds_boost_pop_up(self):
        """
        DESCRIPTION: Tap on the 'Show More' CTA button in the 'Odds boost' pop-up.
        EXPECTED: The User is redirected to the journey for that pop-up instead of completing the quiz.
        """
        pass

    def test_002_tap_on_the_deposit_now_cta_button_in_the_quick_deposit_pop_up(self):
        """
        DESCRIPTION: Tap on the 'Deposit Now' CTA button in the 'Quick Deposit' pop-up.
        EXPECTED: The User is redirected to the journey for that pop-up instead of completing the quiz.
        """
        pass
