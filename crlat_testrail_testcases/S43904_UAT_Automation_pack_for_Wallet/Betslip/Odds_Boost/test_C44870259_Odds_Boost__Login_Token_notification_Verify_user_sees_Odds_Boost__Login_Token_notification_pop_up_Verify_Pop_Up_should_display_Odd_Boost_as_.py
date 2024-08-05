import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870259_Odds_Boost__Login_Token_notification_Verify_user_sees_Odds_Boost__Login_Token_notification_pop_up_Verify_Pop_Up_should_display_Odd_Boost_as_header__Verify_Youve_xx_odds_Boost_available_Verify_all_buttons_on_the_notification_pop_up(Common):
    """
    TR_ID: C44870259
    NAME: "Odds Boost - Login Token notification -Verify user sees Odds Boost - Login Token notification pop up -Verify Pop Up  should display ""Odd Boost ""as header - Verify ""You've (xx) odds Boost available"" -Verify all buttons on the notification pop up
    DESCRIPTION: "Odds Boost - Login Token notification
    DESCRIPTION: -Verify user sees Odds Boost - Login Token notification pop up
    DESCRIPTION: -Verify Pop Up  should display ""Odd Boost ""as header
    DESCRIPTION: - Verify ""You've (xx) odds Boost available""
    DESCRIPTION: -Verify all buttons on the notification pop up (show more, Ok Thanks, Close etc)
    DESCRIPTION: -Verify tapping on ""Okay, Thanks "" button or anywhere outside Pop up, the pop up should be dismissed
    DESCRIPTION: - Verify 'Show More' takes user to Odds Boost - Detail Page
    DESCRIPTION: "
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_verify_user_sees_odds_boost___login_token_notification_pop_upverify_pop_up__should_display_odd_boost_as_header(self):
        """
        DESCRIPTION: Verify user sees Odds Boost - Login Token notification pop up
        DESCRIPTION: Verify Pop Up  should display ""Odd Boost ""as header
        EXPECTED: Login Token notification pop up should be displayed
        EXPECTED: Odds Boost  notification  popup with the buttons like show more, Ok Thanks, Close etc are displayed
        """
        pass

    def test_002_verify_show_more_takes_user_to_odds_boost___detail_page(self):
        """
        DESCRIPTION: Verify 'Show More' takes user to Odds Boost - Detail Page
        EXPECTED: Show more text takes the user to the odds boost detail page
        """
        pass

    def test_003_navigate_to_my_accounts__offers__free_bets__odds_boost(self):
        """
        DESCRIPTION: Navigate to 'My accounts' > Offers & Free bets > Odds boost
        EXPECTED: My account' (User menu) menu is expanded > Offer & Free bets
        EXPECTED: Odds Boost item is available in the menu
        EXPECTED: Summary value 1 of the number of Odds Boost tokens is displaying in Odds Boost item
        """
        pass
