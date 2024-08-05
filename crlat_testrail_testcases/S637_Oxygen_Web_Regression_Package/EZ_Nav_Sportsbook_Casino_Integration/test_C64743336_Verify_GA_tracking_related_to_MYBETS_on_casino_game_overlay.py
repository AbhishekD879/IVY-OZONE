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
class Test_C64743336_Verify_GA_tracking_related_to_MYBETS_on_casino_game_overlay(Common):
    """
    TR_ID: C64743336
    NAME: Verify GA tracking related to MYBETS on casino game overlay
    DESCRIPTION: Verify GA tracking related to MYBETS on casino game overlay
    PRECONDITIONS: * Cashout Tab should be enable from CMS
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * User should have open bets & settled bets
    PRECONDITIONS: * Add 'dataslayer' extension to the chrome (https://chrome.google.com/webstore/detail/dataslayer/ikbablmmjldhamhcldjjigniffkkjgpo)
    PRECONDITIONS: Note: Applicable to only Mobile web
    """
    keep_browser_open = True

    def test_001_launch_any_casino_game(self):
        """
        DESCRIPTION: Launch any casino game
        EXPECTED: * User redirects to particular gaming page ex: Roulette page
        EXPECTED: * User able to see 'sports' icon on EZNav panel(header) in gaming page
        """
        pass

    def test_002_open_dev_tools_gt_dataslayer(self):
        """
        DESCRIPTION: Open dev tools-&gt; dataslayer
        EXPECTED: 
        """
        pass

    def test_003_tap_sports_icon_from_eznav_panel(self):
        """
        DESCRIPTION: Tap 'sports' icon from ezNav panel
        EXPECTED: * User navigates to 'MyBets' overlay & displays below tabs:
        EXPECTED: Cashout
        EXPECTED: Openbets
        EXPECTED: Settledbets
        EXPECTED: * User receives below trackable event format in dev tools-&gt; dataslayer extension:
        EXPECTED: Ex: event: Event.NavigationMenus
        EXPECTED: page.navigationMenus: InGameEzNav_MyBets_11
        EXPECTED: user.profile.accountID: 181917579
        EXPECTED: gtm.uniqueEventId: 526
        """
        pass

    def test_004_tap_cashout_tab(self):
        """
        DESCRIPTION: Tap Cashout tab
        EXPECTED: * Bets are loaded
        EXPECTED: * User able to see 'Terms-conditions' quick links
        EXPECTED: * User able to see 'GO TO SPORTS' CTA on the bottom of page
        """
        pass

    def test_005_tap_on_edp_chevron(self):
        """
        DESCRIPTION: Tap on EDP chevron
        EXPECTED: * User receives popup
        EXPECTED: * User receives below trackable event format in dev tools-&gt; dataslayer extension:
        EXPECTED: Ex:
        EXPECTED: event: 'Event.Tracking',
        EXPECTED: component.CategoryEvent: casino ingame,
        EXPECTED: component.LabelEvent: sports betting overlay,
        EXPECTED: component.ActionEvent: click,
        EXPECTED: component.PositionEvent: ingameeznav,
        EXPECTED: component.LocationEvent: sports redirect pop up,
        EXPECTED: component.EventDetails: EDP Click,
        EXPECTED: component.URLclicked: not applicable,
        """
        pass

    def test_006_click_no_thanks_then_tap_any_of_the_terms__conditions_quick_link_which_exists_bottom_of_the_page(self):
        """
        DESCRIPTION: Click 'NO THANKS' then Tap any of the terms & conditions quick link which exists bottom of the page
        EXPECTED: * User receives popup
        EXPECTED: * User receives below trackable event format in dev tools-&gt; dataslayer extension:
        EXPECTED: Ex:
        EXPECTED: event: 'Event.Tracking',
        EXPECTED: component.CategoryEvent: casino ingame,
        EXPECTED: component.LabelEvent: sports betting overlay,
        EXPECTED: component.ActionEvent: click,
        EXPECTED: component.PositionEvent: ingameeznav,
        EXPECTED: component.LocationEvent: sports redirect pop up,
        EXPECTED: component.EventDetails: Terms-conditions CTA,
        EXPECTED: component.URLclicked: not applicable
        """
        pass

    def test_007_click_no_thanks_then_tap_on_go_to_sports_cta_which_exists_at_bottom_of_the_page(self):
        """
        DESCRIPTION: Click 'NO THANKS' then Tap on 'GO TO SPORTS' CTA which exists at bottom of the page
        EXPECTED: * User receives popup
        EXPECTED: * User receives below trackable event format in dev tools-&gt; dataslayer extension:
        EXPECTED: Ex:
        EXPECTED: event: 'Event.Tracking',
        EXPECTED: component.CategoryEvent: casino ingame,
        EXPECTED: component.LabelEvent: sports betting overlay,
        EXPECTED: component.ActionEvent: click,
        EXPECTED: component.PositionEvent: ingameeznav,
        EXPECTED: component.LocationEvent: sports redirect pop up,
        EXPECTED: component.EventDetails: Go To Sports cta,
        EXPECTED: component.URLclicked: not applicable
        """
        pass

    def test_008_tap_yes_lets_go_cta(self):
        """
        DESCRIPTION: Tap 'YES LET'S GO' CTA
        EXPECTED: * User redirects to sportsbook homepage
        EXPECTED: * User receives below trackable event format in dev tools-&gt; dataslayer extension:
        EXPECTED: Ex:
        EXPECTED: event: 'Event.Tracking',
        EXPECTED: component.CategoryEvent: casino ingame,
        EXPECTED: component.LabelEvent: sports betting overlay,
        EXPECTED: component.ActionEvent: click,
        EXPECTED: component.PositionEvent: ingameeznav,
        EXPECTED: component.LocationEvent: sports redirect pop up,
        EXPECTED: component.EventDetails: Go To Sports confirmation Yes CTA,
        EXPECTED: component.URLclicked: not applicable
        """
        pass

    def test_009_come_back_to_casino_game__tap_sports_icon_on_eznav_panel_then_repeat_step_3_4_in_open_bets(self):
        """
        DESCRIPTION: Come back to casino game & tap sports icon on eznav panel then Repeat step-3, 4 in Open bets
        EXPECTED: 
        """
        pass

    def test_010_tap_5_a_side_leaderboard_widget_when_bet_is_void(self):
        """
        DESCRIPTION: Tap 5-A-Side Leaderboard widget when bet is void
        EXPECTED: * User receives popup
        EXPECTED: * User receives below trackable event format in dev tools-&gt; dataslayer extension:
        EXPECTED: Ex:
        EXPECTED: event: 'Event.Tracking',
        EXPECTED: component.CategoryEvent: casino ingame,
        EXPECTED: component.LabelEvent: sports betting overlay,
        EXPECTED: component.ActionEvent: click,
        EXPECTED: component.PositionEvent: ingameeznav,
        EXPECTED: component.LocationEvent: sports redirect pop up,
        EXPECTED: component.EventDetails: 5-A-Side Leaderboard CTA,
        EXPECTED: component.URLclicked: not applicable
        """
        pass

    def test_011_tap_no_thanks__tap_go_to_5a_side_button_when_selected_players_are_not_participated_in_the_game(self):
        """
        DESCRIPTION: Tap 'NO THANKS' & Tap 'Go to 5A-Side' Button when selected players are not participated in the game
        EXPECTED: * User receives popup
        EXPECTED: * User receives below trackable event format in dev tools-&gt; dataslayer extension:
        EXPECTED: Ex:
        EXPECTED: event: 'Event.Tracking',
        EXPECTED: component.CategoryEvent: casino ingame,
        EXPECTED: component.LabelEvent: sports betting overlay,
        EXPECTED: component.ActionEvent: click,
        EXPECTED: component.PositionEvent: ingameeznav,
        EXPECTED: component.LocationEvent: sports redirect pop up,
        EXPECTED: component.EventDetails: Go to 5-A-Side cta,
        EXPECTED: component.URLclicked: not applicable
        """
        pass

    def test_012_tap_no_thanks__repeat_step_5_6_7_in_all_inner_tabs_of_open_bets(self):
        """
        DESCRIPTION: Tap 'NO THANKS' & Repeat step-5, 6, 7 in all inner tabs of open bets
        EXPECTED: 
        """
        pass

    def test_013_come_back_to_casino_game__tap_sports_icon_on_eznav_panel_then_repeat_step_8_9_10_11_in_settled_bets(self):
        """
        DESCRIPTION: Come back to casino game & tap sports icon on eznav panel then Repeat step-8, 9, 10, 11 in Settled bets
        EXPECTED: 
        """
        pass

    def test_014_coralrepeat_step_5_6_7_in_inshop_bets(self):
        """
        DESCRIPTION: Coral:
        DESCRIPTION: Repeat step-5, 6, 7 in INSHOP Bets
        EXPECTED: 
        """
        pass
