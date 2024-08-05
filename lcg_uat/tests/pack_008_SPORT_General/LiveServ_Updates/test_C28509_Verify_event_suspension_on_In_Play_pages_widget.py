import pytest
import tests
import voltron.environments.constants as vec
from tenacity import stop_after_attempt, retry, retry_if_exception_type
from time import sleep
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot suspend event
# @pytest.mark.hl    # cannot suspend event
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.in_play
@pytest.mark.liveserv_updates
@pytest.mark.slow
@pytest.mark.timeout(800)
@pytest.mark.desktop
@pytest.mark.high
@vtest
class Test_C28509_Verify_event_suspension_on_In_Play_pages_widget(BaseFeaturedTest):
    """
    TR_ID: C28509
    NAME: Verify event suspension on In-Play pages/widget
    DESCRIPTION: This test case verifies event suspension on <Sport> In-Play page/widget
    PRECONDITIONS: 1) LiveServer is available only for In-Play <Sport> events with the following attributes:
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: 3) To verify suspension check new received value in "status" attribute using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: EVENT/EVMKT/SELCN depend on level of triggering suspension event/market/selection
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to 'In-play' page from Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for desktop)
    PRECONDITIONS: 3. Select 'Watch live' tab
    """
    keep_browser_open = True
    output_price = None
    initial_output_prices = None
    expected_betslip_counter_value = 1
    sport_name = vec.sb.FOOTBALL.upper()
    upcoming_switcher = vec.inplay.UPCOMING_SWITCHER.upper()
    live_now_switcher = vec.inplay.LIVE_NOW_SWITCHER.upper()

    @retry(stop=stop_after_attempt(2), retry=retry_if_exception_type(Exception), reraise=True)
    def check_event_odds_state(
            self, sport_name, section_name, event_name, is_enabled=True, is_displayed=True, upcoming=False):
        sleep(3)
        self.device.refresh_page()
        event = self.get_event_in_watch_live_tab(
            sport_name=sport_name, section_name=section_name, event_name=event_name, upcoming=upcoming)
        odds = event.template.items_as_ordered_dict
        self.assertTrue(odds, msg=f'"{event_name}" event Price/Odds buttons is not displayed')
        for price, button in odds.items():
            self.assertEqual(bool(price), is_displayed,
                             msg=f'\n"{event_name}" event price "{price}" actual display state: '
                                 f'"{bool(price)}" is not as expected: "{is_displayed}"')
            button_state = wait_for_result(lambda: button.is_enabled(expected_result=is_enabled, timeout=5),
                                           expected_result=is_enabled, timeout=10,
                                           name=f'Button enabled state to be: "{is_enabled}"')
            self.assertEqual(button_state, is_enabled,
                             msg=f'\n"{event_name}" event "{price}" Bet Button actual enabled state: '
                                 f'"{button_state}" is not as expected: "{is_enabled}"')

    def get_section_in_watch_live_tab(self, sport_name, section_name, upcoming=False):
        if self.device_type == 'mobile':
            if upcoming:
                sections = self.site.inplay.tab_content.upcoming.items_as_ordered_dict
            else:
                sections = self.site.inplay.tab_content.live_now.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found in "LIVE NOW"')
            self.__class__.sport_section = sections.get(sport_name)
            self.assertTrue(self.sport_section, msg=f'"{sport_name}" is not displayed in "LIVE NOW"')
            self.sport_section.expand()
            self.assertTrue(self.sport_section.is_expanded, msg=f'"{sport_name}" is not expanded')
            league_sections = self.sport_section.items_as_ordered_dict
            self.assertTrue(league_sections, msg=f'No Leagues for "{sport_name}" found')
            league = league_sections.get(section_name)
            if not league and self.sport_section.has_show_more_leagues_button():
                self.sport_section.show_more_leagues_button.click()
                league_sections = self.sport_section.items_as_ordered_dict
                self.assertTrue(league_sections, msg=f'No Leagues for "{sport_name}" found')
                league = league_sections.get(section_name)
        else:
            if upcoming:
                self.site.inplay.tab_content.grouping_buttons.click_button(self.upcoming_switcher)
                actual_btn = self.site.inplay.tab_content.grouping_buttons.current
                self.assertEqual(actual_btn, self.upcoming_switcher, msg=f'"{self.upcoming_switcher}" is not selected')
            else:
                self.site.inplay.tab_content.grouping_buttons.click_button(self.live_now_switcher)
                actual_btn = self.site.inplay.tab_content.grouping_buttons.current
                self.assertEqual(actual_btn, self.live_now_switcher, msg=f'"{self.live_now_switcher}" is not selected')
            sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg=f'No sections found in "{actual_btn}"')
            self.__class__.sport_section = sections.get(sport_name)
            self.assertTrue(self.sport_section, msg=f'"{sport_name}" not found in sport sections')
            self.sport_section.expand()
            self.assertTrue(self.sport_section.is_expanded(), msg=f'"{self.sport_section}" is not expanded')
            league_sections = self.sport_section.items_as_ordered_dict
            self.assertTrue(league_sections, msg=f'No leagues found in "{sport_name}"')
            league = league_sections.get(section_name)
            self.assertTrue(league, msg=f'"{section_name}" not found in leagues')
            league.expand()
            self.assertTrue(league.is_expanded(), msg=f'"{section_name}" is not expanded')
        return league

    def get_event_in_watch_live_tab(self, sport_name, section_name, event_name, upcoming=False):
        section = self.get_section_in_watch_live_tab(
            sport_name=sport_name, section_name=section_name, upcoming=upcoming)
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{section_name}"')
        event = events.get(event_name)
        self.assertTrue(event, msg=f'Event "{event_name}" is not found in "{section_name}"')
        return event

    def test_000_preconditions(self):
        """
        DESCRIPTION: Run preconditions
        """
        # create live now event
        live_now_start_time = self.get_date_time_formatted_string(seconds=10)
        live_now_event_params = self.ob_config.add_autotest_premier_league_football_event(
            is_live=True, perform_stream=True, start_time=live_now_start_time)
        self.__class__.live_now_event_name = live_now_event_params.team1 + ' v ' + live_now_event_params.team2
        self.__class__.live_now_event_id = live_now_event_params.event_id
        # create upcoming event
        upcoming_start_time = self.get_date_time_formatted_string(hours=2)
        upcoming_event_params = self.ob_config.add_autotest_premier_league_football_event(
            is_upcoming=True, perform_stream=True, start_time=upcoming_start_time)
        self.__class__.upcoming_event_name = upcoming_event_params.team1 + ' v ' + upcoming_event_params.team2
        self.__class__.upcoming_event_id = upcoming_event_params.event_id
        # league name
        if self.brand == 'ladbrokes':
            self.__class__.league = f'{tests.settings.football_autotest_competition} - ' \
                                    f'{tests.settings.football_autotest_competition_league}'.title() \
                if self.device_type == 'desktop' else tests.settings.football_autotest_competition_league
        else:
            self.__class__.league = f'{tests.settings.football_autotest_competition} - ' \
                                    f'{tests.settings.football_autotest_competition_league}' \
                if self.device_type == 'desktop' else tests.settings.football_autotest_competition_league.title()
        # open application and navigate to in-play page watch live tab
        self.site.wait_content_state(state_name='Homepage')
        self.navigate_to_page(name='in-play')
        self.site.inplay.inplay_sport_menu.click_item(item_name=vec.sb.WATCH_LIVE_LABEL)

    def test_001_suspend_any_event_within_live_now_section(
            self, event_name=None, event_id=None, upcoming=False):
        """
        DESCRIPTION: Trigger the following situation for any event within 'Live now' section:
        DESCRIPTION: **eventStatusCode="S"**
        EXPECTED: All Price/Odds buttons of this event are displayed immediately as greyed out and become disabled but still displaying prices
        """
        event_name, event_id = (event_name, event_id) \
            if event_name and event_id else (self.live_now_event_name, self.live_now_event_id)
        self.ob_config.change_event_state(event_id=event_id, displayed=True, active=False)
        result = wait_for_result(lambda: self.check_event_is_active(event_id),
                                 expected_result=False, name='Event is suspended', timeout=5)
        self.assertFalse(result, msg='Event is not suspended')
        self.check_event_odds_state(sport_name=self.sport_name, section_name=self.league, event_name=event_name,
                                    is_displayed=True, is_enabled=False, upcoming=upcoming)

    def test_002_activate_the_event(
            self, event_name=None, event_id=None, upcoming=False):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **eventStatusCode="A"**
        EXPECTED: All Price/Odds buttons of this event are no more disabled, they become active immediately
        """
        event_name, event_id = (event_name, event_id) \
            if event_name and event_id else (self.live_now_event_name, self.live_now_event_id)
        self.ob_config.change_event_state(event_id=event_id, displayed=True, active=True)
        result = wait_for_result(lambda: self.check_event_is_active(event_id),
                                 name='Event is active', timeout=5)
        self.assertTrue(result, msg='Event is not active')
        self.check_event_odds_state(sport_name=self.sport_name, section_name=self.league, event_name=event_name,
                                    is_displayed=True, is_enabled=True, upcoming=upcoming)

    def test_003_collapse_sport_type_accordion_suspend_the_event_expand_sport_type_accordion(
            self, event_name=None, event_id=None, upcoming=False):
        """
        DESCRIPTION: * Collapse sport/type accordion
        DESCRIPTION: * Trigger the following situation for this event:
        DESCRIPTION: **eventStatusCode="S"**
        DESCRIPTION: * Expand sport/type accordion
        EXPECTED: If section is collapsed and suspension was triggered, after expanding the section - all Price/Odds buttons of this event are displayed as greyed out and become disabled but still displaying prices
        """
        event_name, event_id = (event_name, event_id) \
            if event_name and event_id else (self.live_now_event_name, self.live_now_event_id)
        self.sport_section.scroll_to()
        self.sport_section.collapse()
        self.ob_config.change_event_state(event_id=event_id, displayed=True, active=False)
        result = wait_for_result(lambda: self.check_event_is_active(event_id),
                                 expected_result=False, name='Event is suspended', timeout=5)
        self.assertFalse(result, msg='Event is not suspended')
        self.sport_section.expand()
        self.check_event_odds_state(sport_name=self.sport_name, section_name=self.league, event_name=event_name,
                                    is_displayed=True, is_enabled=False, upcoming=upcoming)

    def test_004_collapse_sport_type_accordion_activate_the_event_expand_sport_type_accordion(
            self, event_name=None, event_id=None, upcoming=False):
        """
        DESCRIPTION: * Collapse sport/type accordion
        DESCRIPTION: * Trigger the following situation for this event:
        DESCRIPTION: **eventStatusCode="A"**
        DESCRIPTION: * Expand sport/type accordion
        EXPECTED: If section is collapsed and unsuspension was triggered, after expanding the section - all Price/Odds buttons of this event are no more disabled, they become active
        """
        event_name, event_id = (event_name, event_id) \
            if event_name and event_id else (self.live_now_event_name, self.live_now_event_id)
        self.sport_section.scroll_to()
        self.sport_section.collapse()
        self.ob_config.change_event_state(event_id=event_id, displayed=True, active=True)
        result = wait_for_result(lambda: self.check_event_is_active(event_id),
                                 name='Event is active', timeout=5)
        self.assertTrue(result, msg='Event is not active')
        self.sport_section.expand()
        self.site.wait_splash_to_hide(2)
        self.check_event_odds_state(sport_name=self.sport_name, section_name=self.league, event_name=event_name,
                                    is_displayed=True, is_enabled=True, upcoming=upcoming)

    def test_005_navigate_back_to_the_homepage_trigger_suspension_for_sport_live_event(
            self, event_name=None, event_id=None, upcoming=False):
        """
        DESCRIPTION: Navigate back to the Homepage, trigger suspension for <Sport> live event
        EXPECTED: If In-Play Sports page was not opened and suspension was triggered there, after opening In-Play Sports page - all Price/Odds buttons of this event are displayed as greyed out and become disabled there but still displaying prices
        """
        event_name, event_id = (event_name, event_id) \
            if event_name and event_id else (self.live_now_event_name, self.live_now_event_id)
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')
        self.ob_config.change_event_state(event_id=event_id, displayed=True, active=False)
        result = wait_for_result(lambda: self.check_event_is_active(event_id),
                                 expected_result=False, name='Event is suspended', timeout=5)
        self.assertFalse(result, msg='Event is not suspended')
        self.navigate_to_page(name='in-play')
        self.site.inplay.inplay_sport_menu.click_item(item_name=vec.sb.WATCH_LIVE_LABEL)
        self.check_event_odds_state(sport_name=self.sport_name, section_name=self.league, event_name=event_name,
                                    is_displayed=True, is_enabled=False, upcoming=upcoming)

    def test_006_trigger_the_suspension_before_application_is_opened(self):
        """
        DESCRIPTION: Trigger the suspension before application is opened
        EXPECTED: If application was not started/opened and suspension was triggered for live Sports event market 'Match Betting', after opening application and In-Play Sports page - all Price/Odds buttons of this event are displayed as greyed out and become disabled there but still displaying prices
        """
        # need to close the application
        pass

    def test_007_repeat_steps_1_6_for_any_event_within_upcoming_events_section(self, upcoming=True):
        """
        DESCRIPTION: Repeat steps 1-6 for any event within 'Upcoming events' section ('In-play' page > 'Watch live' tab)
        """
        self.test_001_suspend_any_event_within_live_now_section(
            event_name=self.upcoming_event_name, event_id=self.upcoming_event_id, upcoming=upcoming)
        self.test_002_activate_the_event(
            event_name=self.upcoming_event_name, event_id=self.upcoming_event_id, upcoming=upcoming)
        self.test_003_collapse_sport_type_accordion_suspend_the_event_expand_sport_type_accordion(
            event_name=self.upcoming_event_name, event_id=self.upcoming_event_id, upcoming=upcoming)
        self.test_004_collapse_sport_type_accordion_activate_the_event_expand_sport_type_accordion(
            event_name=self.upcoming_event_name, event_id=self.upcoming_event_id, upcoming=upcoming)
        self.test_005_navigate_back_to_the_homepage_trigger_suspension_for_sport_live_event(
            event_name=self.upcoming_event_name, event_id=self.upcoming_event_id, upcoming=upcoming)

    def test_008_repeat_steps_1_7_on_following_sections(self):
        """
        DESCRIPTION: Repeat steps 1-7 on:
        DESCRIPTION: * 'In-play' page > when any sport is selected in Sports Menu Ribbon
        DESCRIPTION: * Home page > 'In-play' tab
        DESCRIPTION: * Home page > featured 'In-play' module
        DESCRIPTION: * Sport Landing page > 'In-play' tab
        DESCRIPTION: * Sport Landing page > featured 'In-play' module on 'Matches' tab
        """
        # better not to automate because of 25 additional steps for live now section and 25 - for upcoming
        # execution time will rise up to approximately 12 minutes
        pass

    def test_009_for_desktop_repeat_steps_1_6_on_sport_landing_page_for_in_play_widget_and_live_stream_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 1-6 on Sport Landing page for 'In-play' widget and 'Live Stream' widget
        """
        # already verified in previous steps
        pass

    def test_010_for_desktop_repeat_steps_1_6_on_home_page_for_in_play__live_stream_section_for_both_switchers(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 1-6 on Home page for 'In-play & Live Stream' section for both switchers
        """
        # already verified in previous steps
        pass
