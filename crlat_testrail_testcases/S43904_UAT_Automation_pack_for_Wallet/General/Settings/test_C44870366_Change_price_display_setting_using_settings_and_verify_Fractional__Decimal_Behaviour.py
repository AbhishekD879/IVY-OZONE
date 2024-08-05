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
class Test_C44870366_Change_price_display_setting_using_settings_and_verify_Fractional__Decimal_Behaviour(Common):
    """
    TR_ID: C44870366
    NAME: Change price display setting using settings and verify Fractional / Decimal Behaviour
    DESCRIPTION: 
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_001_navigate_to_betting_settings_from_the_my_accountright_menu__settings__betting_settings(self):
        """
        DESCRIPTION: Navigate to Betting Settings from the My Account/Right menu > Settings > Betting settings
        EXPECTED: 1. Settings page is displayed.
        EXPECTED: 2. The odds format is set to 'Fractional' by default.
        """
        pass

    def test_002_change_the_odds_format_to_decimal_click_on_back_button_and_verify_the_pages_(self):
        """
        DESCRIPTION: Change the odds format to 'Decimal'. Click on Back button and Verify the pages .
        EXPECTED: The odds format is displayed in decimals on the Homepage.
        """
        pass

    def test_003_navigate_throughout_the_following_pages_in_the_application_and_verify_the_odds_format__1_landing_pages_of_sports2_tabs_like_in_play_competitions_specials_outright_coupons_etc_wherever_applicable_for_different_sports3_event_detail_pages_of_sports4_in_play_tab5_bet_slip6_bet_receipt7_quick_bet_applicable_for_mobile_only8_my_bets(self):
        """
        DESCRIPTION: Navigate throughout the following pages in the application and verify the odds format -
        DESCRIPTION: 1. Landing pages of sports
        DESCRIPTION: 2. Tabs like in-play, competitions, specials, outright, coupons etc (wherever applicable) for different sports.
        DESCRIPTION: 3. Event detail pages of sports
        DESCRIPTION: 4. In-play tab
        DESCRIPTION: 5. Bet slip
        DESCRIPTION: 6. Bet receipt
        DESCRIPTION: 7. Quick bet (applicable for mobile only)
        DESCRIPTION: 8. My bets
        EXPECTED: The odds format is displayed in decimals on all the mentioned pages.
        """
        pass

    def test_004_change_the_odds_format_to_fractional_perform_steps_2_3_for_fractional_format_of_odds(self):
        """
        DESCRIPTION: Change the odds format to 'Fractional'. Perform steps 2-3 for fractional format of odds.
        EXPECTED: The odds format is displayed in fractions on all the pages throughout the application.
        """
        pass
