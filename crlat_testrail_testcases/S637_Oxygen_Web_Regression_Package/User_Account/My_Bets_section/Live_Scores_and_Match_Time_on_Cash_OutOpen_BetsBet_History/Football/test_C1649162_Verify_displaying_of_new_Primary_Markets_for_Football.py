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
class Test_C1649162_Verify_displaying_of_new_Primary_Markets_for_Football(Common):
    """
    TR_ID: C1649162
    NAME: Verify displaying of new Primary Markets for Football
    DESCRIPTION: This test case verifies displaying of Football Primary Markets on Home page > Featured, In Play & In Play > All Sports in the following order:
    DESCRIPTION: 1 - Match Betting (market template: |Match Betting|)
    DESCRIPTION: 2 - Match Result (market template: |Match Betting|)
    DESCRIPTION: 3 - Extra-Time Result (market template: |Extra-Time Result|)
    DESCRIPTION: 4 - Penalty Shoot-Out Winner (market template: |Penalty Shoot-Out Winner|)
    DESCRIPTION: 5 - To Qualify (market template: |To Qualify|)
    DESCRIPTION: 6 - To Lift the trophy (market template: |To Qualify|)
    DESCRIPTION: 7 - To finish 3rd (market template: |To Qualify|)
    DESCRIPTION: 8 - To reach the final (market template: |To Qualify|)
    DESCRIPTION: https://docs.google.com/spreadsheets/d/1m8fCgL92tvEk9vZRW02dnWn4cmFiuLqwc7zo6PvMF8o/edit#gid=0
    PRECONDITIONS: - Football event is created in OB TI with all markets from Description (https://confluence.egalacoral.com/display/SPI/OpenBet+Systems)
    PRECONDITIONS: - Football event is configured for Featured tab module in CMS (https://coral-cms-dev1.symphony-solutions.eu/featured-modules/)
    PRECONDITIONS: - In Play events have attribute drilldownTagNames = EVFLAG_BL ('Bet In Play list' check box in ti) where:
    PRECONDITIONS: live now: start time in the past ( but less than 1 day), isOff = Yes (in siteSetver in isLiveNowEvent=true, isStarted = true)
    PRECONDITIONS: - Oxygen app > Home page > Featured tab is opened
    PRECONDITIONS: - User is logged into Oxygen app
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_football_event_from_preconditions_with_match_betting_match_betting_market(self):
        """
        DESCRIPTION: Verify displaying of Football event from Preconditions with 'Match Betting' (|Match Betting|) market
        EXPECTED: * Event with 'Match Betting' (|Match Betting|) market is available
        EXPECTED: * Corresponding selections are displayed under each market header (home/draw/away)
        """
        pass

    def test_002__in_ti_undisplay_and_suspend_match_betting_match_betting_market_of_an_event_from_preconditions_in_app_verify_displaying_the_same_football_event_with_primary_market_match_result_market_template_match_betting_after_page_refresh(self):
        """
        DESCRIPTION: * In TI: Undisplay (and suspend) 'Match Betting' (|Match Betting|) market of an event from Preconditions
        DESCRIPTION: * In app: Verify displaying the same Football event with Primary Market 'Match Result' (market template: |Match Betting|) after page refresh
        EXPECTED: * Event disappears from Football section
        EXPECTED: * Same event with the next active and available Primary Market appears after refresh (e.g. 'Match Result' (market template: |Match Betting|)
        EXPECTED: * Corresponding selections are displayed under each market header (home/draw/away)
        """
        pass

    def test_003_repeat_step_1_undisplaying_the_previous_primary_markets_to_make_the_following_markets_available3___extra_time_result_market_template_extra_time_result4___penalty_shoot_out_winner_market_template_penalty_shoot_out_winner5___to_qualify_market_template_to_qualify6___to_lift_the_trophy_market_template_to_qualify7___to_finish_3rd_market_template_to_qualify8___to_reach_the_final_market_template_to_qualify(self):
        """
        DESCRIPTION: Repeat step 1 undisplaying the previous Primary Markets to make the following markets available:
        DESCRIPTION: 3 - Extra-Time Result (market template: |Extra-Time Result|)
        DESCRIPTION: 4 - Penalty Shoot-Out Winner (market template: |Penalty Shoot-Out Winner|)
        DESCRIPTION: 5 - To Qualify (market template: |To Qualify|)
        DESCRIPTION: 6 - To Lift the trophy (market template: |To Qualify|)
        DESCRIPTION: 7 - To finish 3rd (market template: |To Qualify|)
        DESCRIPTION: 8 - To reach the final (market template: |To Qualify|)
        EXPECTED: * Event with previously undisplayed market disappears from Football section
        EXPECTED: * Same event with the next active and available Primary Market appears after refresh
        EXPECTED: * Corresponding selections are displayed under each market header (home/draw/away); 'draw' column is empty if market consist of 2 selections
        """
        pass

    def test_004__in_ti_display_a_primary_market_eg_to_qualify_market_template_to_qualify_and_extra_time_result_market_template_extra_time_result_in_app_verify_displaying_primary_market_for_the_event(self):
        """
        DESCRIPTION: * In TI: Display a Primary Market e.g. 'To Qualify' (market template: |To Qualify|) and Extra-Time Result (market template: |Extra-Time Result|)
        DESCRIPTION: * In app: Verify displaying Primary Market for the event
        EXPECTED: Primary Market higher in order is available for an event (here: Extra-Time Result (market template: |Extra-Time Result|)
        """
        pass

    def test_005__in_ti_suspend_primary_market_extra_time_result_market_template_extra_time_result_in_app_verify_footbal_event(self):
        """
        DESCRIPTION: * In TI: Suspend Primary Market Extra-Time Result (market template: |Extra-Time Result|)
        DESCRIPTION: * In app: Verify Footbal event
        EXPECTED: * Event is available
        EXPECTED: * All selections are disabled and greyed out
        """
        pass

    def test_006__in_ti_undisplay_all_all_available_markets_in_app_refresh_the_page__verify_football_event_from_preconditions(self):
        """
        DESCRIPTION: * In TI: Undisplay all all available markets
        DESCRIPTION: * In app: Refresh the page & verify Football event from Preconditions
        EXPECTED: Event is available with no market/selections
        """
        pass

    def test_007__in_ti_add_several_in_play_football_events_with_different_primary_markets_eg__match_betting_extra_time_result_penalty_shoot_out_winner__make_live_changes_to_them_simultaneously_eg_price_change_suspension_undisplaydisplay_in_app_verify_added_events(self):
        """
        DESCRIPTION: * In TI: Add several in-play Football events with different Primary Markets (e.g  Match Betting, Extra-Time Result, Penalty Shoot-Out Winner) & make live changes to them simultaneously (e.g. price change, suspension, undisplay/display)
        DESCRIPTION: * In app: Verify added events
        EXPECTED: All events are live updated accordingly
        """
        pass

    def test_008_repeat_steps_1_6_for_home__in_play__in_play_all_sports_pages(self):
        """
        DESCRIPTION: Repeat steps 1-6 for Home > In Play & In Play All Sports pages
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_1_6_for_in_play__football__football__in_play_pages(self):
        """
        DESCRIPTION: Repeat steps 1-6 for In Play > Football & Football > In Play pages
        EXPECTED: 
        """
        pass
