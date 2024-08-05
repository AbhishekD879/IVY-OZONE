import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import wait_for_category_in_inplay_ls_structure


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@vtest
class Test_C28410_Verify_Expired_Events_Removing_from_In_Play_pages(BaseSportTest):
    """
    TR_ID: C28410
    NAME: Verify Expired Events Removing from In-Play pages
    DESCRIPTION: This test case verifies which events are removed from displaying within In-Play pages on front-end
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose any Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To configure In-Play module on Sport Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    markets = [('to_qualify',)]

    def inplay_livestream_check(self):
        result = False
        if self.device_type == 'mobile' and self.brand == 'bma':
            expected_market = vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME
        elif self.device_type == 'desktop' and self.brand == 'ladbrokes':
            expected_market = 'Auto Test - Autotest Premier League'
        else:
            expected_market = self.expected_market

        if self.device_type == 'mobile' and self.brand == 'ladbrokes':
            live_stream = self.site.home.get_module_content(
                module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream))
            self.site.wait_splash_to_hide(timeout=15)
            in_play_sections = live_stream.live_now.items_as_ordered_dict
        elif self.device_type == 'mobile' and self.brand == 'bma':
            in_play_sections = self.site.live_stream.live_now.items_as_ordered_dict
        else:
            in_play_sections = self.site.live_stream.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(in_play_sections, msg=f'No in-play sports sections found')
        in_play_section = in_play_sections.get(self.sport_name.upper())
        self.assertTrue(in_play_section, msg=f'"{self.sport_name.upper()}" section not found')
        if not in_play_section.is_expanded():
            in_play_section.expand()
        in_play_leagues = in_play_section.items_as_ordered_dict
        self.assertTrue(in_play_leagues, msg=f'No leagues found for "{self.sport_name}"')
        in_play_league = in_play_leagues.get(expected_market)
        if in_play_league is None:
            return result
        self.assertTrue(in_play_league, msg=f'"{in_play_league}" league not found')
        in_play_events = list(in_play_league.items_as_ordered_dict.keys())
        self.assertTrue(in_play_events, msg=f'No events found for "{in_play_events}"')
        for event in in_play_events:
            if self.__class__.inplay_team_1 in event and self.__class__.inplay_team_2 in event:
                result = True
                break
        return result

    def upcoming_livestream_check(self):
        result = False
        if self.device_type == 'mobile' and self.brand == 'bma':
            expected_market = vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME
        elif self.device_type == 'desktop' and self.brand == 'ladbrokes':
            expected_market = 'Auto Test - Autotest Premier League'
        else:
            expected_market = self.expected_market
        if self.device_type == 'mobile' and self.brand == 'ladbrokes':
            live_stream = self.site.home.get_module_content(
                module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream))
            self.site.wait_splash_to_hide(timeout=15)
            upcoming_sections = live_stream.upcoming.items_as_ordered_dict
        elif self.device_type == 'mobile' and self.brand == 'bma':
            upcoming_sections = self.site.live_stream.upcoming.items_as_ordered_dict
        else:
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
            upcoming_sections = self.site.live_stream.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(upcoming_sections, msg=f'No upcoming sports sections found')
        upcoming_section = upcoming_sections.get(self.sport_name.upper())
        self.assertTrue(upcoming_section, msg=f'"{self.sport_name.upper()}" section not found')
        if not upcoming_section.is_expanded():
            upcoming_section.expand()
        upcoming_leagues = upcoming_section.items_as_ordered_dict
        self.assertTrue(upcoming_leagues, msg=f'No leagues found for "{self.sport_name}"')
        upcoming_league = upcoming_leagues.get(expected_market)
        if upcoming_league is None:
            return result
        self.assertTrue(upcoming_league, msg=f'"{upcoming_league}" league not found')
        upcoming_events = list(upcoming_league.items_as_ordered_dict.keys())
        self.assertTrue(upcoming_events, msg=f'No events found for "{upcoming_events}"')
        for event in upcoming_events:
            if self.__class__.upcoming_team_1 in event and self.__class__.upcoming_team_2 in event:
                result = True
                break
        return result

    def inplay_event_check(self):
        result = False
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.LIVE_NOW_SWITCHER)
        accordion = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict.get(self.expected_market)
        if accordion is None:
            return result
        if not accordion.is_expanded():
            accordion.expand()
        events = list(accordion.items_as_ordered_dict.keys())
        for event in events:
            if self.__class__.inplay_team_1 in event and self.__class__.inplay_team_2 in event:
                result = True
                break
        return result

    def upcoming_event_check(self):
        result = False
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
        if self.device_type == 'mobile':
            section = self.site.inplay.tab_content.upcoming.items_as_ordered_dict.get(self.expected_market)
        else:
            section = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict.get(self.expected_market)
        if section is None:
            return result
        if not section.is_expanded():
            section.expand()
        upcoming_events = list(section.items_as_ordered_dict.keys())
        for event in upcoming_events:
            if self.__class__.upcoming_team_1 in event and self.__class__.upcoming_team_2 in event:
                result = True
                break
        return result

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event and log in
        """
        self.__class__.expected_market = 'AUTO TEST - AUTOTEST PREMIER LEAGUE' if self.device_type == 'desktop' \
            else 'AUTOTEST PREMIER LEAGUE'
        self.__class__.sport_name = 'Football' if self.brand == 'bma' else 'FOOTBALL'
        start_time_upcoming = self.get_date_time_formatted_string(hours=10)
        self.__class__.in_play_event = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                                                 perform_stream=True,
                                                                                                 markets=self.markets)
        self.__class__.inplay_event_id = self.in_play_event.event_id
        self.__class__.inplay_team_1 = self.in_play_event.team1
        self.__class__.inplay_team_2 = self.in_play_event.team2
        self.__class__.upcoming_event = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True,
                                                                                                  perform_stream=True,
                                                                                                  start_time=start_time_upcoming,
                                                                                                  markets=self.markets)
        self.__class__.upcoming_event_id = self.upcoming_event.event_id
        self.__class__.upcoming_team_1 = self.upcoming_event.team1
        self.__class__.upcoming_team_2 = self.upcoming_event.team1

        # checking in-play events on In-play page
        self.navigate_to_page('/in-play/football')
        if self.device_type == 'mobile':
            page_headers = list(self.site.inplay.tab_content.items_as_ordered_dict.keys())
            self.assertIn(vec.inplay.LIVE_NOW_EVENTS_SECTION, page_headers,
                          msg=f'No "{vec.inplay.LIVE_NOW_EVENTS_SECTION}" section is found on In-Play page')
            self.assertIn(vec.inplay.UPCOMING_EVENTS_SECTION, page_headers,
                          msg=f'No "{vec.inplay.UPCOMING_EVENTS_SECTION}" section is found on In-Play page')

        result_inplay = self.inplay_event_check()
        self.assertTrue(result_inplay, msg='Inplay event is not available on Inplay page')
        result_upcoming = self.upcoming_event_check()
        self.assertTrue(result_upcoming, msg='Upcoming event is not available on Inplay page')

    def test_001_trigger_completionexpiration_of_verified_eventnote_eventcompletionexpiration_means_that_event_is_not_present_on_siteserver_anymore_attribute_displayedn_is_set_for_the_event(self):
        """
        DESCRIPTION: Trigger completion/expiration of verified event
        DESCRIPTION: NOTE: Event completion/expiration means that event is not present on SiteServer anymore (attribute 'displayed="N"' is set for the event )
        EXPECTED: Completed/expired event is removed from the front-end automatically
        """
        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=False, active=False)
        sleep(5)
        result_inplay = self.inplay_event_check()
        self.assertFalse(result_inplay, msg='Inplay event is still available on Inplay page')

    def test_002_repeat_step_1_for_upcoming_events(self):
        """
        DESCRIPTION: Repeat step 1 for upcoming events
        EXPECTED: Completed/expired event is removed from the front-end automatically
        """
        self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=False, active=False)
        sleep(5)
        result_upcoming = self.upcoming_event_check()
        self.assertFalse(result_upcoming, msg='Upcoming event is still available on Inplay page')

    def test_003_navigate_to_sports_landing_page__in_play_tab_and_repeat_steps_1_2(self):
        """
        DESCRIPTION: Navigate to Sports Landing page > 'In-Play' tab and repeat steps 1-2
        EXPECTED:
        """
        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=True, active=True)
        self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=True, active=True)
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                              self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(button_name=in_play_tab)

        result_inplay = self.inplay_event_check()
        self.assertTrue(result_inplay, msg='Inplay event is not available on Inplay page')
        result_upcoming = self.upcoming_event_check()
        self.assertTrue(result_upcoming, msg='Upcoming event is not available on Inplay page')

        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=False, active=False)
        sleep(5)
        result_inplay = self.inplay_event_check()
        self.assertFalse(result_inplay, msg='Inplay event is still available on Inplay page')
        self.test_002_repeat_step_1_for_upcoming_events()

    def test_004_navigate_to_live_stream_page_and_repeat_steps_1_2(self):
        """
        DESCRIPTION: Navigate to Live Stream page and repeat steps 1-2
        EXPECTED:
        """
        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=True, active=True)
        self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=True, active=True)
        if self.device_type == 'mobile':
            self.navigate_to_page(name='home/live-stream')
            self.site.wait_content_state(state_name='homepage')
            wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.football.category_id)
        else:
            self.navigate_to_page(name='live-stream')
            self.site.wait_content_state(state_name='LiveStream')
            wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.football.category_id)

        live_stream_inplay_check = self.inplay_livestream_check()
        self.assertTrue(live_stream_inplay_check, msg='In-play event is not present on Live Stream page')

        live_stream_upcoming_check = self.upcoming_livestream_check()
        self.assertTrue(live_stream_upcoming_check, msg='Upcoming event is not present on Live Stream page')

        self.ob_config.change_event_state(event_id=self.inplay_event_id, displayed=False, active=False)
        self.ob_config.change_event_state(event_id=self.upcoming_event_id, displayed=False, active=False)
        self.device.refresh_page()
        live_stream_inplay_check = self.inplay_livestream_check()
        self.assertFalse(live_stream_inplay_check, msg='In-play event is present on Live Stream page')

        live_stream_upcoming_check = self.upcoming_livestream_check()
        self.assertFalse(live_stream_upcoming_check, msg='Upcoming event is present on Live Stream page')

    def test_005_for_mobiletabletnavigate_to_homepage__in_play_tab_and_repeat_steps_1_2(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to Homepage > 'In-Play' tab and repeat steps 1-2
        EXPECTED:
        """
        # Covered in step 4

    def test_006_for_mobiletabletnavigate_to_homepage__live_stream_tab_and_repeat_steps_1_2(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to Homepage > 'Live Stream' tab and repeat steps 1-2
        EXPECTED:
        """
        # Covered in step 4

    def test_007_for_mobiletabletnavigate_to_homepage__featured_tab__in_play__module_and_repeat_step_1(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to Homepage > 'Featured' tab > 'In-play'  module and repeat step 1
        EXPECTED:
        """
        # Covered in step 4

    def test_008_for_mobiletabletnavigate_to_sports_landing_page__matches_tab__in_play_module_and_repeat_step_1(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to Sports Landing page > 'Matches' tab > 'In-play' module and repeat step 1
        EXPECTED:
        """
        # Covered in step 3

    def test_009_for_desktopnavigate_to_in_play__live_stream_section_on_homepageand_repeat_step_1_for_both_in_play_and_live_stream_filter_switchers(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage
        DESCRIPTION: and repeat step 1 for both 'In-Play' and 'Live Stream' filter switchers
        EXPECTED:
        """
        if self.device_type == 'desktop':
            sport_name = 'Football' if self.brand == 'ladbrokes' else self.sport_name.upper()
            self.navigate_to_page(name='/')
            home_module_items = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            self.assertTrue(home_module_items, msg='Can not find any module items')
            home_module_items.get(sport_name).click()
            sections = self.site.contents.tab_content.items_as_ordered_dict
            self.assertTrue(sections, msg='No Sections present')

    def test_010_for_desktopnavigate_to_sports_landing_page__in_play_widget_and_repeat_step_1(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page > 'In-play' widget and repeat step 1
        EXPECTED:
        """
        # Covered in step 3
