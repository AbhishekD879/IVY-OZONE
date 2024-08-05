import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C64569853_Verify_GO_TO_SPORTS_CTA_on_My_Bets_page_if_there_is_no_bets_in_Cashout_Openebts_Settledbets_tabs(Common):
    """
    TR_ID: C64569853
    NAME: Verify 'GO TO SPORTS' CTA on My Bets page if there is no bets in Cashout/Openebts/Settledbets tabs.
    DESCRIPTION: Verify 'GO TO SPORTS' CTA on My Bets page if there is no bets in Cashout/Openebts/Settledbets tabs.
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in.
    PRECONDITIONS: * User has no bets in openbets/cashout/settledbets
    PRECONDITIONS: Note: Applies to only Mobile Web
    """
    keep_browser_open = True

    def test_001_launch_any_casino_game(self):
        """
        DESCRIPTION: Launch any casino game
        EXPECTED: * User redirects to particular gaming page ex: Roulette page
        EXPECTED: * User able to see 'sports' icon on EZNav panel(header) in gaming page
        """
        pass

    def test_002_tap_sports_icon_from_eznav_panel(self):
        """
        DESCRIPTION: Tap 'sports' icon from ezNav panel
        EXPECTED: * User navigates to 'MyBets' overlay & displays below tabs:
        EXPECTED: Cashout (if available)
        EXPECTED: Openbets
        EXPECTED: Settledbets
        """
        pass

    def test_003_tap_cashout_tab(self):
        """
        DESCRIPTION: Tap 'Cashout' tab
        EXPECTED: * Corresponding info message is shown when there is no bets
        EXPECTED: * 'GO TO SPORTS' CTA with yellow background is displayed.
        """
        pass

    def test_004_next_tap_go_to_sports_cta(self):
        """
        DESCRIPTION: Next tap 'GO TO SPORTS' CTA
        EXPECTED: * A confirmation popup with CTA should be displayed - stating that: 'Are you sure you want to end your gaming session and visit Sportsbook?'
        EXPECTED: 1. NO THANKS
        EXPECTED: 2. YES, LET'S GO(Yellow background)
        EXPECTED: 3. Do not show me this message again(checkbox)
        """
        pass

    def test_005_now_tap_on_no_thanks(self):
        """
        DESCRIPTION: Now tap on 'NO THANKS'
        EXPECTED: * Pop up is closed & user is on same page
        """
        pass

    def test_006_repeat_step_3_4_5_in_all_openbets__settledbets_inner_tabs__except_in_shop(self):
        """
        DESCRIPTION: Repeat step-3, 4, 5 in all Openbets & Settledbets inner tabs  except In-shop
        EXPECTED: 
        """
        pass

    def test_007_now_come_back_to_cashout_tab_again_then_tap_on_go_to_sports_cta_on_the_overlay__tap_on_yes_lets_go(self):
        """
        DESCRIPTION: Now come back to 'Cashout' tab again then tap on 'Go To Sports' CTA on the overlay & Tap on 'YES, LET'S GO'
        EXPECTED: * User redirects to sportsbook homepage
        """
        pass

    def test_008_repeat_step_1_step_2_step_7_in_all_openbets__settledbets_inner_tabs_except_in_shop(self):
        """
        DESCRIPTION: Repeat step-1, step-2, step-7 in all Openbets & Settledbets inner tabs except In-shop
        EXPECTED: 
        """
        pass

    def test_009_repeat_step_1_step_2_step_3_step_4__check_the_do_not_show_me_this_message_again_checkbox_then_tap_no_thanks(self):
        """
        DESCRIPTION: Repeat step-1, step-2, step-3, step-4 & check the 'Do not show me this message again' checkbox then Tap 'NO THANKS'
        EXPECTED: * User checked the checkbox
        EXPECTED: * User will be on same page i.e., My Bets page
        """
        pass

    def test_010_atlast_tap_on_go_to_sports_cta_on_cashoutopenbetssettledbets(self):
        """
        DESCRIPTION: Atlast Tap on 'Go To Sports' CTA on Cashout/Openbets/Settledbets
        EXPECTED: * User won't get popup & directly navigates to sportsbook homepage
        """
        pass
