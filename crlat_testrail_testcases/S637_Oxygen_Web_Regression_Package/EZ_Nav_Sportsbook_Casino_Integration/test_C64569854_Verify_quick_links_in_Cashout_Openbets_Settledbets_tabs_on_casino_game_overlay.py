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
class Test_C64569854_Verify_quick_links_in_Cashout_Openbets_Settledbets_tabs_on_casino_game_overlay(Common):
    """
    TR_ID: C64569854
    NAME: Verify quick links in Cashout/Openbets/Settledbets tabs on casino game overlay.
    DESCRIPTION: Verify quick links in Cashout/Openbets/Settledbets tabs on casino game overlay.
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in.
    PRECONDITIONS: * User has bets in openbets/cashout/settledbets
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
        EXPECTED: * Below quick links are displayed at bottom of page:
        EXPECTED: 1. See Profit/Loss link,
        EXPECTED: 2. See Retail Bets on Shop Bet Tracker;
        EXPECTED: 3. Cash Out Terms & Conditions;
        EXPECTED: 4. Edit My Acca Terms & Conditions
        """
        pass

    def test_004_click_on_any_of_the_quick_link(self):
        """
        DESCRIPTION: Click on any of the quick link
        EXPECTED: * A confirmation popup with CTA should be displayed - stating that: 'Are you sure you want to end your gaming session and visit Sportsbook?'
        EXPECTED: 1. NO THANKS
        EXPECTED: 2. YES, LET'S GO(Yellow background)
        EXPECTED: 3. Do not show me this message again(checkbox)
        """
        pass

    def test_005_tap_on_lets_go_cta(self):
        """
        DESCRIPTION: Tap on 'LET'S GO' CTA
        EXPECTED: * User navigates to its corresponding page
        """
        pass

    def test_006_now_come_back_to_gaming_page_gtmybets_overlay_repeat_step_45_in_all__openbetssettledbets_inner_tabs(self):
        """
        DESCRIPTION: Now come back to Gaming page-&gt;MyBets Overlay Repeat step-4,5 in all  Openbets/Settledbets inner tabs
        EXPECTED: 
        """
        pass

    def test_007_again_come_back_to_gaming_page_gtmybets_overlay_gt_settledbets_tab_then_tap_see_profitloss_link(self):
        """
        DESCRIPTION: Again come back to Gaming page-&gt;MyBets Overlay-&gt; 'Settledbets' tab then tap 'See Profit/Loss' link
        EXPECTED: * Same as step-4
        """
        pass

    def test_008_tap_on_lets_go_cta(self):
        """
        DESCRIPTION: Tap on 'LET'S GO' CTA
        EXPECTED: * User redirects to sportsbook homepage
        """
        pass

    def test_009_repeat_step_78_on_all_inner_tabs_of_settledbets(self):
        """
        DESCRIPTION: Repeat step-7,8 on all inner tabs of Settledbets
        EXPECTED: 
        """
        pass
