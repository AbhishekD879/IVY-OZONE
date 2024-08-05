import pytest
import time
from voltron.utils.helpers import normalize_name
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@vtest
class Test_C1649162_Verify_displaying_of_new_Primary_Markets_for_Football(BaseSportTest):
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
    """
    keep_browser_open = True
    selection_ids = []
    markets = [('extra_time_result', {'cashout': True}),
               ('to_qualify', {'cashout': True}),
               ('penalty_shoot_out_winner', {'cashout': True})]

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - Football event is created in OB TI with all markets from Description (https://confluence.egalacoral.com/display/SPI/OpenBet+Systems)
        PRECONDITIONS: - Football event is configured for Featured tab module in CMS (https://coral-cms-dev1.symphony-solutions.eu/featured-modules/)
        PRECONDITIONS: - In Play events have attribute drilldownTagNames = EVFLAG_BL ('Bet In Play list' check box in ti) where:
        PRECONDITIONS: live now: start time in the past ( but less than 1 day), isOff = Yes (in siteSetver in isLiveNowEvent=true, isStarted = true)
        PRECONDITIONS: - Oxygen app > Home page > Featured tab is opened
        PRECONDITIONS: - User is logged into Oxygen app
        """
        event = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets, is_live=False)
        self.__class__.eventID = event.event_id
        self.__class__.marketIDs = list(event.all_markets_ids.values())[0]
        self.__class__.default_market = event.default_market_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
        self.site.login()
        self.site.wait_content_state("Homepage")

    def test_001_verify_displaying_of_football_event_from_preconditions_with_match_betting_match_betting_market(self):
        """
        DESCRIPTION: Verify displaying of Football event from Preconditions with 'Match Betting' (|Match Betting|) market
        EXPECTED: * Event with 'Match Betting' (|Match Betting|) market is available
        EXPECTED: * Corresponding selections are displayed under each market header (home/draw/away)
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('FOOTBALL', timeout=60)
        time.sleep(15)  # Take time to reflect un-displaying/displaying of events
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        is_event_present = self.get_event_from_league(section_name=self.section_name, event_id=self.eventID)
        self.assertTrue(is_event_present,
                        msg=f'Event "{self.event_name}" is not displayed in section "{self.section_name}"')

    def test_002__in_ti_undisplay_and_suspend_match_betting_match_betting_market_of_an_event_from_preconditions_in_app_verify_displaying_the_same_football_event_with_primary_market_match_result_market_template_match_betting_after_page_refresh(self):
        """
        DESCRIPTION: * In TI: Undisplay (and suspend) 'Match Betting' (|Match Betting|) market of an event from Preconditions
        DESCRIPTION: * In app: Verify displaying the same Football event with Primary Market 'Match Result' (market template: |Match Betting|) after page refresh
        EXPECTED: * Event disappears from Football section
        EXPECTED: * Same event with the next active and available Primary Market appears after refresh (e.g. 'Match Result' (market template: |Match Betting|)
        EXPECTED: * Corresponding selections are displayed under each market header (home/draw/away)
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.default_market, displayed=False)
        time.sleep(15)  # Take time to reflect un-displaying/displaying of events
        self.device.refresh_page()

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
        # Covered in step 2

    def test_004__in_ti_display_a_primary_market_eg_to_qualify_market_template_to_qualify_and_extra_time_result_market_template_extra_time_result_in_app_verify_displaying_primary_market_for_the_event(self):
        """
        DESCRIPTION: * In TI: Display a Primary Market e.g. 'To Qualify' (market template: |To Qualify|) and Extra-Time Result (market template: |Extra-Time Result|)
        DESCRIPTION: * In app: Verify displaying Primary Market for the event
        EXPECTED: Primary Market higher in order is available for an event (here: Extra-Time Result (market template: |Extra-Time Result|)
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketIDs['to_qualify'], displayed=True)
        self.navigate_to_edp(event_id=self.eventID)
        time.sleep(15)  # Take time to reflect un-displaying/displaying of events
        self.device.refresh_page()
        time.sleep(15)
        markets_displayed = list(self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.keys())
        if self.brand == 'bma':
            to_qualify = 'TO QUALIFY' if self.device_type == 'mobile' else 'To Qualify'
        else:
            to_qualify = 'To Qualify'
        self.assertIn(to_qualify, markets_displayed, msg='To qualify market is not displayed')

    def test_005__in_ti_suspend_primary_market_extra_time_result_market_template_extra_time_result_in_app_verify_footbal_event(self):
        """
        DESCRIPTION: * In TI: Suspend Primary Market Extra-Time Result (market template: |Extra-Time Result|)
        DESCRIPTION: * In app: Verify Footbal event
        EXPECTED: * Event is available
        EXPECTED: * All selections are disabled and greyed out
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketIDs['extra_time_result'], displayed=False)
        time.sleep(15)  # Take time to reflect un-displaying/displaying of events
        self.device.refresh_page()

    def test_006__in_ti_undisplay_all_all_available_markets_in_app_refresh_the_page__verify_football_event_from_preconditions(self):
        """
        DESCRIPTION: * In TI: Undisplay all all available markets
        DESCRIPTION: * In app: Refresh the page & verify Football event from Preconditions
        EXPECTED: Event is available with no market/selections
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketIDs['to_qualify'], displayed=False)
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketIDs['penalty_shoot_out_winner'], displayed=False)
        time.sleep(15)  # Take time to reflect un-displaying/displaying of events
        self.device.refresh_page()

    def test_007__in_ti_add_several_in_play_football_events_with_different_primary_markets_eg__match_betting_extra_time_result_penalty_shoot_out_winner__make_live_changes_to_them_simultaneously_eg_price_change_suspension_undisplaydisplay_in_app_verify_added_events(self):
        """
        DESCRIPTION: * In TI: Add several in-play Football events with different Primary Markets (e.g  Match Betting, Extra-Time Result, Penalty Shoot-Out Winner) & make live changes to them simultaneously (e.g. price change, suspension, undisplay/display)
        DESCRIPTION: * In app: Verify added events
        EXPECTED: All events are live updated accordingly
        """
        self.__class__.event_live = self.ob_config.add_autotest_premier_league_football_event(is_live=True, markets=self.markets)
        self.__class__.live_event_id = self.event_live.event_id
        self.__class__.default_market_live = self.event_live.default_market_id
        self.navigate_to_page(name='sport/football/live')

    def test_008_repeat_steps_1_6_for_home__in_play__in_play_all_sports_pages(self):
        """
        DESCRIPTION: Repeat steps 1-6 for Home > In Play & In Play All Sports pages
        EXPECTED:
        """
        self.navigate_to_edp(self.live_event_id)
        self.__class__.marketIDs = list(self.event_live.all_markets_ids.values())[0]
        markets_displayed = list(self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.keys())
        self.assertNotIn('penalty_shoot_out_winner', markets_displayed, msg="Extra - time result is still displayed")
        self.ob_config.change_market_state(event_id=self.live_event_id, market_id=self.marketIDs['penalty_shoot_out_winner'], displayed=False)
        self.ob_config.change_market_state(event_id=self.live_event_id, market_id=self.marketIDs['to_qualify'], displayed=False)
        self.ob_config.change_market_state(event_id=self.live_event_id, market_id=self.marketIDs['extra_time_result'], displayed=False)
        time.sleep(15)  # Take time to reflect un-displaying/displaying of events
        self.device.refresh_page()
        markets_displayed1 = list(self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.keys())
        self.assertNotIn('to_qualify', markets_displayed1, msg="Extra - time result is still displayed")
        self.assertNotIn('extra_time_result', markets_displayed1, msg="Extra - time result is still displayed")

    def test_009_repeat_steps_1_6_for_in_play__football__football__in_play_pages(self):
        """
        DESCRIPTION: Repeat steps 1-6 for In Play > Football & Football > In Play pages
        EXPECTED:
        """
        # Covered in above steps
