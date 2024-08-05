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
class Test_C44870266_Verify_user_can_see_odds_boost_pop_up_for_first_time_login_and_verify_the_Show_more_button_navigation(Common):
    """
    TR_ID: C44870266
    NAME: Verify user can see odds boost pop up for first time login and verify the 'Show more' button navigation.
    DESCRIPTION: 
    PRECONDITIONS: Load application and Login into the application
    """
    keep_browser_open = True

    def test_001_login_into_application_by_user_with_generated_odds_boost_token(self):
        """
        DESCRIPTION: Login into Application by user with generated Odds boost token
        EXPECTED: User is logged in successfully
        EXPECTED: The "Odds Boost" token notification is displayed (as overlay on Mobile, Tablet and as pop-up on Desktop)
        EXPECTED: ContentText1:'You have XX Odds Boost available' (1 is a value specific to the user as fetched on login)
        EXPECTED: On the login journey, this should be last* notification in the queue to appear - after any login messages, onboarding, touch ID etc.
        """
        pass
