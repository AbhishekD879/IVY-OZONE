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
class Test_C44870415_Mini_Games_Below_Betslip(Common):
    """
    TR_ID: C44870415
    NAME: Mini Games Below Betslip
    DESCRIPTION: Mini Games Below Betslip are displayed below betslip as CMS configuration
    PRECONDITIONS: Mini Games configured in CMS to be displayed on front end bellow Betslip
    PRECONDITIONS: User loads the BETA desktop web page and log in
    """
    keep_browser_open = True

    def test_001_verify_that_mini_games_module_is_displayed_under_betslip_area_as_per_cms_configurationverify_that_user_is_able_to_play_mini_gamesverify_balance_is_updated_automatically_after_playing_few_gamesverify_user_is_shown_insufficient_balance_message_when_balance_is_less_than_stakeverify_that_user_can_add_funds_and_continue_bettingverify_that_bet_is_reflected_on_my_bets_and_bets_history(self):
        """
        DESCRIPTION: Verify that Mini Games module is displayed under Betslip area as per CMS configuration
        DESCRIPTION: Verify that user is able to play Mini Games
        DESCRIPTION: Verify balance is updated automatically after playing few games
        DESCRIPTION: Verify user is shown insufficient balance message when balance is less than stake
        DESCRIPTION: Verify that user can add funds and continue betting
        DESCRIPTION: Verify that bet is reflected on my bets and bets history
        EXPECTED: Mini Games module feature is displayed as per configuration and works as designed
        EXPECTED: Betting flow in Mini Games module is as per expected
        """
        pass

    def test_002_log_outverify_login_popup_is__displayed_when_user_clicks_on_the_play_now_buttonverify_that_after_log_in_user_is_able_to_do_all_actions_mentioned_in_step_1(self):
        """
        DESCRIPTION: Log out
        DESCRIPTION: Verify login popup is  displayed when user clicks on the "Play Now" button
        DESCRIPTION: Verify that after log in user is able to do all actions mentioned in step 1
        EXPECTED: User is able to log out and log in, Mini Games betting flow works fine
        """
        pass
