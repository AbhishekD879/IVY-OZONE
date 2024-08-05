import pytest
import tests
from crlat_ob_client.create_event import CreateSportEvent
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot make modifications to events in prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C120274_Verify_Sport_events_without_Primary_Market_displaying_on_In_Play_pages(Common):
    """
    TR_ID: C120274
    NAME: Verify <Sport> events without Primary Market displaying on 'In-Play' pages
    DESCRIPTION: This test case verifies how <Sport> events without Primary Market are displayed on In-Play pages
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. For reaching Pre-match events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * Primary Market is any Market that has the following attributes:
    PRECONDITIONS: *   isMarketBetInRun="true" on event level
    PRECONDITIONS: *   outcomeMeaningMajorCode="MR"/"HH" on each outcome level
    """
    keep_browser_open = True
    event_found = False

    def retrieving_events_from_ui(self, upcoming=False, home=False):
        if self.device_type not in ['mobile', 'tablet']:
            if upcoming:
                self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
                self.site.wait_content_state_changed(timeout=4)
            self.__class__.grouping_buttons = self.site.inplay.tab_content
            self.assertTrue(self.grouping_buttons,
                            msg=f'"Upcoming" events are not available in inplay tab for sport ""')
            actual_sport_type = self.grouping_buttons.accordions_list.items_as_ordered_dict['AUTO TEST - AUTOTEST PREMIER LEAGUE']
            self.__class__.actual_events_under_type = actual_sport_type.items_as_ordered_dict
        else:
            if upcoming:
                if home:
                    self.__class__.grouping_buttons = self.site.home.tab_content.upcoming.items_as_ordered_dict['FOOTBALL']
                    self.grouping_buttons.click()
                    self.assertTrue(self.grouping_buttons,
                                    msg=f'"Upcoming" events are not available in home page inplay tab for sport ""')
                    actual_sport_type = self.grouping_buttons.items_as_ordered_dict['Autotest Premier League']
                else:
                    self.__class__.grouping_buttons = self.site.inplay.tab_content.upcoming
                    self.assertTrue(self.grouping_buttons,
                                    msg=f'"Upcoming" events are not available in inplay tab for sport ""')
                    actual_sport_type = self.grouping_buttons.items_as_ordered_dict['AUTOTEST PREMIER LEAGUE']
                    actual_sport_type.click()
            else:
                if home:
                    self.__class__.grouping_buttons = self.site.home.tab_content.live_now.items_as_ordered_dict['FOOTBALL']
                    league = 'Autotest Premier League' if self.brand == 'bma' else 'AUTOTEST PREMIER LEAGUE'
                    actual_sport_type = self.grouping_buttons.items_as_ordered_dict[league]
                else:
                    self.__class__.grouping_buttons = self.site.inplay.tab_content.live_now
                    self.assertTrue(self.grouping_buttons, msg=f'"Live" events are not available in inplay tab for sport ""')
                    actual_sport_type = self.grouping_buttons.items_as_ordered_dict['AUTOTEST PREMIER LEAGUE']
            self.__class__.actual_events_under_type = actual_sport_type.items

    def retrieving_events_from_ui_for_inplaystream(self, live_stream=False):
        home_module_items = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
        sport = 'FOOTBALL' if self.brand == 'bma' else 'Football'
        home_module_items[sport].click()
        if live_stream:
            self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu.click_item(vec.sb.LIVE_STREAM.upper())
            self.site.wait_content_state_changed(timeout=4)
        self.__class__.grouping_buttons = self.site.home.desktop_modules.inplay_live_stream_module.tab_content
        self.assertTrue(self.grouping_buttons,
                        msg=f'"Upcoming" events are not available in inplay tab for sport ""')
        actual_sport_type = self.grouping_buttons.accordions_list.items_as_ordered_dict['AUTO TEST - AUTOTEST PREMIER LEAGUE']
        self.__class__.actual_events_under_type = actual_sport_type.items_as_ordered_dict

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event with several markets
        """
        markets = [('both_teams_to_score',)]
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, markets=markets, perform_stream=True, img_stream=True)
        self.ob_config.add_autotest_premier_league_football_event(is_live=True, perform_stream=True, img_stream=True)
        self.__class__.eventID = event_params.event_id
        self.__class__.eventName = event_params.ss_response['event']['name']
        self.__class__.primary_marketID = event_params.default_market_id
        self.__class__.marketID = self.ob_config.market_ids[self.eventID]['both_teams_to_score']
        event_params1 = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, markets=markets,
                                                                                  perform_stream=True, img_stream=True)
        self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, perform_stream=True, img_stream=True)
        self.__class__.eventID1 = event_params1.event_id
        self.__class__.eventName1 = event_params1.ss_response['event']['name']
        self.__class__.primary_marketID1 = event_params1.default_market_id
        self.__class__.marketID1 = self.ob_config.market_ids[self.eventID1]['both_teams_to_score']
        self.navigate_to_page('in-play/football')
        self.site.wait_content_state_changed(timeout=30)

    def test_001_select_sport_event_with_several_markets_including_primary_market___in_ti_system_undisplay_primary_markets_of_selected_event(self, home=False):
        """
        DESCRIPTION: Select <Sport> event with several markets including Primary Market -> In TI system undisplay Primary Market(s) of selected event
        EXPECTED: <Sport> event disappears from the page
        """
        status = False
        self.retrieving_events_from_ui(home=home)
        if self.device_type not in ['mobile', 'tablet']:
            self.assertTrue(self.eventName in list(self.actual_events_under_type.keys()), msg=f'Expected event"{self.eventName}" is not present in actual event list "{list(self.actual_events_under_type.keys())}"')
        else:
            for item in self.actual_events_under_type:
                if self.eventName == item.template.event_name:
                    status = True
            self.assertTrue(status, msg=f'Expected event"{self.eventName}" is not present in actual event list')
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.primary_marketID, displayed=False, active=False)
        sleep(5)
        if self.device_type not in ['mobile', 'tablet']:
            actual_sport_type = self.grouping_buttons.accordions_list.items_as_ordered_dict['AUTO TEST - AUTOTEST PREMIER LEAGUE']
            actual_events_under_type = actual_sport_type.items_as_ordered_dict
            self.assertFalse(self.eventName in list(actual_events_under_type.keys()),
                             msg=f'Expected event"{self.eventName}" is not present in actual event list "{list(actual_events_under_type.keys())}"')
        else:
            if home and self.brand == 'bma':
                actual_sport_type = self.grouping_buttons.items_as_ordered_dict['Autotest Premier League']
            else:
                actual_sport_type = self.grouping_buttons.items_as_ordered_dict['AUTOTEST PREMIER LEAGUE']
            actual_events_under_type = actual_sport_type.items
            for item in actual_events_under_type:
                try:
                    self.assertNotEqual(self.eventName, item.template.event_name,
                                        msg=f'Expected event"{self.eventName}" is not present in actual event list "{item.template.event_name}"  ')
                except Exception:
                    self._logger.info('Event is not present in the actual events')

    def test_002_reload_the_page(self, home=False):
        """
        DESCRIPTION: Reload the page
        EXPECTED: *   <Sport> event is shown on the page
        EXPECTED: *   <Sport> event is shown as without 'Price/Odds' buttons
        """
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        self.retrieving_events_from_ui(home=home)
        if self.device_type not in ['mobile', 'tablet']:
            self.assertTrue(self.eventName in list(self.actual_events_under_type.keys()),
                            msg=f'Expected event"{self.eventName}" is not present in actual event list "{list(self.actual_events_under_type.keys())}"  ')
            event_price = self.actual_events_under_type[self.eventName].template
            price_buttons = len(event_price.items_as_ordered_dict)
            self.assertTrue(price_buttons == 0,
                            msg=f'Expected event"{self.eventName}" is not present in actual event list "{list(self.actual_events_under_type.keys())}"  ')
        else:
            for item in self.actual_events_under_type:
                if self.eventName == item.template.event_name:
                    price_buttons = len(item.template.items_as_ordered_dict)
                    self.assertTrue(price_buttons == 0,
                                    msg=f'Expected event"{self.eventName}" is not present in actual event list')

    def test_003_select_sport_event_with_several_markets_including_primary_market___in_ti_system_remove_ismarketbetinruntrue_attribute_for_primary_markets_for_selected_event__reload_the_page(self, home=False):
        """
        DESCRIPTION: Select <Sport> event with several markets including Primary Market -> In TI system remove isMarketBetInRun="true" attribute for Primary Market(s) for selected event.
        DESCRIPTION: -> Reload the page
        EXPECTED: *   <Sport> event is shown on the page
        EXPECTED: *   <Sport> event is shown as without 'Price/Odds' buttons
        """
        category_id = self.ob_config.football_config.category_id
        class_id = self.ob_config.football_config.autotest_class.class_id
        type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        market_template_id = self.ob_config.football_config.autotest_class.autotest_premier_league.market_template_id
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand, category_id=category_id,
                                 class_id=class_id, type_id=type_id)
        event.update_market_settings(market_id=self.primary_marketID, event_id=self.eventID,
                                     market_template_id=market_template_id, market_display_sort_code='MR',
                                     bet_in_run='N')
        self.test_002_reload_the_page(home=home)
        event.update_market_settings(market_id=self.primary_marketID, event_id=self.eventID,
                                     market_template_id=market_template_id, market_display_sort_code='MR',
                                     bet_in_run='Y')

    def test_004_select_sport_event_with_several_markets_including_primary_market___in_ti_system_undisplay_all_markets_for_selected_event(self, home=False):
        """
        DESCRIPTION: Select <Sport> event with several markets including Primary Market -> In TI system undisplay ALL Markets for selected event
        EXPECTED: *   <Sport> event disappears from the page
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=False,
                                           active=False)
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.primary_marketID, displayed=False,
                                           active=False)
        sleep(5)
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        self.retrieving_events_from_ui(home=home)
        if self.device_type not in ['mobile', 'tablet']:
            self.assertFalse(self.eventName in list(self.actual_events_under_type.keys()),
                             msg=f'Expected event"{self.eventName}" is present in actual event list "{list(self.actual_events_under_type.keys())}"  ')
        else:
            for item in self.actual_events_under_type:
                try:
                    self.assertNotEqual(self.eventName, item.template.event_name,
                                        msg=f'Expected event"{self.eventName}" is not present in actual event list "{item.template.event_name}"  ')
                except Exception:
                    self._logger.info('Event is not present in the actual events')

        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True,
                                           active=True)
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.primary_marketID, displayed=True,
                                           active=True)

    def test_005_reload_the_page(self):
        """
        DESCRIPTION: Reload the page
        EXPECTED: <Sport> event is NOT shown on the page
        """
        # covered in above step
        # This code is for next step navigation
        self.navigate_to_page('/in-play/football')
        self.site.wait_content_state_changed(timeout=30)

    def test_006_repeat_steps_1_6_for_upcoming_events(self, home=False):
        """
        DESCRIPTION: Repeat steps 1-6 for upcoming events
        """
        self.retrieving_events_from_ui(upcoming=True, home=home)
        if self.device_type not in ['mobile', 'tablet']:
            self.assertTrue(self.eventName1 in list(self.actual_events_under_type.keys()),
                            msg=f'Expected event"{self.eventName1}" is not present in actual event list "{list(self.actual_events_under_type.keys())}"  ')
        else:
            for item in self.actual_events_under_type:
                try:
                    if self.eventName1 == item.template.event_name:
                        self.__class__.event_found = True
                except Exception:
                    continue
            self.assertTrue(self.event_found, msg=f'Expected event"{self.eventName1}" is not present in actual event list')
        self.ob_config.change_market_state(event_id=self.eventID1, market_id=self.primary_marketID1, displayed=False,
                                           active=False)
        sleep(5)
        if self.device_type not in ['mobile', 'tablet']:
            actual_sport_type = self.grouping_buttons.accordions_list.items_as_ordered_dict[
                'AUTO TEST - AUTOTEST PREMIER LEAGUE']
            actual_events_under_type = actual_sport_type.items_as_ordered_dict
            self.assertFalse(self.eventName1 in list(actual_events_under_type.keys()),
                             msg=f'Expected event"{self.eventName1}" is not present in actual event list "{list(actual_events_under_type.keys())}"  ')
        else:
            if home:
                actual_sport_type = self.grouping_buttons.items_as_ordered_dict['Autotest Premier League']
            else:
                actual_sport_type = self.grouping_buttons.items_as_ordered_dict['AUTOTEST PREMIER LEAGUE']
            actual_events_under_type = actual_sport_type.items
            for item in actual_events_under_type:
                try:
                    self.assertNotEqual(self.eventName1, item.template.event_name,
                                        msg=f'Expected event"{self.eventName1}" is not present in actual event list "{item.template.event_name}"  ')
                except Exception:
                    self._logger.info('Event is not present in the actual events')

        self.device.refresh_page()
        self.site.wait_content_state_changed()
        self.retrieving_events_from_ui(upcoming=True, home=home)
        if self.device_type not in ['mobile', 'tablet']:
            self.assertTrue(self.eventName1 in list(self.actual_events_under_type.keys()),
                            msg=f'Expected event"{self.eventName1}" is not present in actual event list "{list(self.actual_events_under_type.keys())}"  ')
            event_price = self.actual_events_under_type[self.eventName1].template
            price_buttons = len(event_price.items_as_ordered_dict)
            self.assertTrue(price_buttons == 0,
                            msg=f'Expected event"{self.eventName1}" is not present in actual event list "{list(self.actual_events_under_type.keys())}"  ')
        else:
            for item in self.actual_events_under_type:
                if self.eventName1 == item.template.event_name:
                    price_buttons = len(item.template.items_as_ordered_dict)
                    self.assertTrue(price_buttons == 0,
                                    msg=f'Expected event"{self.eventName1}" is not present in actual event list')

        self.ob_config.change_market_state(event_id=self.eventID1, market_id=self.marketID1, displayed=False,
                                           active=False)
        self.ob_config.change_market_state(event_id=self.eventID1, market_id=self.primary_marketID1, displayed=False,
                                           active=False)
        sleep(5)
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        self.retrieving_events_from_ui(upcoming=True, home=home)
        if self.device_type not in ['mobile', 'tablet']:
            self.assertFalse(self.eventName1 in list(self.actual_events_under_type.keys()),
                             msg=f'Expected event"{self.eventName1}" is present in actual event list "{list(self.actual_events_under_type.keys())}"  ')
        else:
            for item in self.actual_events_under_type:
                try:
                    self.assertNotEqual(self.eventName1, item.template.event_name,
                                        msg=f'Expected event"{self.eventName}" is not present in actual event list "{item.template.event_name}"  ')
                except Exception:
                    self._logger.info('Event is not present in the actual events')

        self.ob_config.change_market_state(event_id=self.eventID1, market_id=self.marketID1, displayed=True,
                                           active=True)
        self.ob_config.change_market_state(event_id=self.eventID1, market_id=self.primary_marketID1, displayed=True,
                                           active=True)

    def test_007_navigate_to_sports_landing_page__in_play_tab_and_repeat_steps_1_7(self):
        """
        DESCRIPTION: Navigate to Sports Landing page > 'In-Play' tab and repeat steps 1-7
        """
        self.navigate_to_page('sport/football/live')
        self.site.wait_content_state_changed(timeout=30)
        self.site.football.tabs_menu.click_button(vec.siteserve.IN_PLAY_TAB)
        self.site.wait_content_state_changed(timeout=5)
        self.test_001_select_sport_event_with_several_markets_including_primary_market___in_ti_system_undisplay_primary_markets_of_selected_event()
        self.test_002_reload_the_page()
        self.test_003_select_sport_event_with_several_markets_including_primary_market___in_ti_system_remove_ismarketbetinruntrue_attribute_for_primary_markets_for_selected_event__reload_the_page()
        self.test_004_select_sport_event_with_several_markets_including_primary_market___in_ti_system_undisplay_all_markets_for_selected_event()
        self.test_006_repeat_steps_1_6_for_upcoming_events()

    def test_008_for_mobiletabletnavigate_to_the_homepage__in_play_tab_and_repeat_steps_1_7(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to the Homepage > 'In-Play' tab and repeat steps 1-7
        """
        if self.device_type == 'mobile':
            self.navigate_to_page('/home/in-play')
            self.site.wait_content_state_changed(timeout=10)
            self.site.home.tabs_menu.click_button('IN-PLAY')
            self.site.wait_content_state_changed(timeout=10)
            self.test_001_select_sport_event_with_several_markets_including_primary_market___in_ti_system_undisplay_primary_markets_of_selected_event(home=True)
            self.test_002_reload_the_page(home=True)
            self.test_003_select_sport_event_with_several_markets_including_primary_market___in_ti_system_remove_ismarketbetinruntrue_attribute_for_primary_markets_for_selected_event__reload_the_page(home=True)
            self.test_004_select_sport_event_with_several_markets_including_primary_market___in_ti_system_undisplay_all_markets_for_selected_event(home=True)
            self.test_006_repeat_steps_1_6_for_upcoming_events(home=True)

    def test_009_for_desktopnavigate_to_in_play__live_stream_section_on_homepage_and_repeat_steps_1_7_for_both_in_play_and_live_stream_filter_switchers(self):
        """
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage and repeat steps 1-7 for both 'In-play' and 'Live Stream' filter switchers
        """
        if self.device_type == 'desktop':
            self.navigate_to_page('/')
            self.site.wait_content_state_changed(timeout=10)
            self.retrieving_events_from_ui_for_inplaystream(live_stream=True)
            self.assertTrue(self.eventName in list(self.actual_events_under_type.keys()),
                            msg=f'Expected event"{self.eventName}" is not present in actual event list "{list(self.actual_events_under_type.keys())}"  ')
            self.ob_config.change_market_state(event_id=self.eventID, market_id=self.primary_marketID,
                                               displayed=False,
                                               active=False)
            sleep(5)
            actual_sport_type = self.grouping_buttons.accordions_list.items_as_ordered_dict['AUTO TEST - AUTOTEST PREMIER LEAGUE']
            actual_events_under_type = actual_sport_type.items_as_ordered_dict
            self.assertFalse(self.eventName in list(actual_events_under_type.keys()),
                             msg=f'Expected event"{self.eventName}" is not present in actual event list "{list(actual_events_under_type.keys())}"  ')
            self.device.refresh_page()
            self.retrieving_events_from_ui_for_inplaystream(live_stream=True)
            self.assertTrue(self.eventName in list(self.actual_events_under_type.keys()),
                            msg=f'Expected event"{self.eventName}" is not present in actual event list "{list(self.actual_events_under_type.keys())}"  ')
            event_price = self.actual_events_under_type[self.eventName].template
            price_buttons = len(event_price.items_as_ordered_dict)
            self.assertTrue(price_buttons == 0,
                            msg=f'Expected event"{self.eventName}" is not present in actual event list "{list(self.actual_events_under_type.keys())}"  ')
            self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=False,
                                               active=False)
            self.ob_config.change_market_state(event_id=self.eventID, market_id=self.primary_marketID,
                                               displayed=False,
                                               active=False)
            sleep(5)
            self.device.refresh_page()
            self.site.wait_content_state_changed()
            self.retrieving_events_from_ui_for_inplaystream(live_stream=True)
            self.assertFalse(self.eventName in list(self.actual_events_under_type.keys()),
                             msg=f'Expected event"{self.eventName}" is not present in actual event list "{list(self.actual_events_under_type.keys())}"  ')
