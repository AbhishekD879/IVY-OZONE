import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared.contents.inplay import InPlaySportCarouselButton
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.pages.shared.contents.inplay_watchlive import InPlayWatchLiveTabContent
from voltron.utils.waiters import wait_for_result


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.p1
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.slow
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.homepage_featured
@vtest
class Test_C44870175_Verify_Streaming_Tab_on_Home_Page_Verify_Live_Now_and_Upcoming_Tabs_and_check_if_streaming_is_working_properly(Common, InPlaySportCarouselButton, InPlayWatchLiveTabContent):
    """
    TR_ID: C44870175
    NAME: Verify Streaming Tab on Home Page. Verify Live Now and Upcoming Tabs and check if streaming is working properly.
    DESCRIPTION: "Verify user sees 'Streaming' tab on HP and 'Live Now' , 'upcoming' tabs - Verify 'Live now' page categorise into sports -Verify User can navigate to correct event on both 'Live Now' , 'upcoming' tabs events. - Verify user can check streaming properly
    PRECONDITIONS: User need to logged in in order to watch Live streaming
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User need to logged in in order to watch Live streaming
        EXPECTED: User is logged in successfully
        """
        self.site.login()

    def test_001_load_app(self):
        """
        DESCRIPTION: Load app
        EXPECTED: App is loaded user is landed on Home Page
        """
        self.site.wait_content_state('Homepage')

    def test_002_tap_on_live_stream_tab(self):
        """
        DESCRIPTION: Tap on LIVE STREAM TAB
        EXPECTED: Mobile & Tablet : Live Stream page is loaded with LIVE NOW and UPCOMING tabs, LIVE NOW tab is expanded by default.
        EXPECTED: Desktop : Live Stream tab displays events with Live streaming available with the highlighted events streaming at the top of the tab.
        """
        if self.device_type in ['mobile', 'tablet']:
            if self.brand == 'ladbrokes':
                self.site.home.tabs_menu.items_as_ordered_dict[vec.SB.LIVE_STREAM.upper()].click()
                self.site.contents.scroll_to_top()
                live_now_tab = self.site.live_stream.live_now_tab.text
                self.assertEqual(live_now_tab, vec.inplay.LIVE_NOW_SWITCHER.title(),
                                 msg=f'Actual text: "{live_now_tab}" is not same as'
                                     f'Expected text: "{vec.inplay.LIVE_NOW_SWITCHER.title()}"')
            else:
                self.site.home.menu_carousel.click_item(vec.SB.ALL_SPORTS.upper())
                self.site.all_sports.a_z_sports_section.items_as_ordered_dict[vec.SB.LIVE_STREAM].click()
                self.site.contents.scroll_to_top()
                live_now_tab = self.site.live_stream.live_now_tab.text
                self.assertEqual(live_now_tab, vec.inplay.LIVE_NOW_SWITCHER,
                                 msg=f'Actual text: "{live_now_tab}" is not same as'
                                     f'Expected text: "{vec.inplay.LIVE_NOW_SWITCHER}"')

            live_now_sports_list = self.site.live_stream.live_now.items_as_ordered_dict
            if live_now_sports_list:
                live_now_sports_list = self.site.live_stream.live_now.items_as_ordered_dict
                self.assertTrue(live_now_sports_list,
                                msg=f'No events found on "{vec.inplay.LIVE_NOW_SWITCHER}" tab')
                sports = list(live_now_sports_list.keys())
                section = live_now_sports_list.get(sports[0])
                self.site.contents.scroll_to_top()
                section.expand()
                wait_for_result(lambda: self.assertTrue(section.is_expanded(),
                                msg=f'Sport Section "{sports[0]}" is not expanded by default'), timeout=15)
            else:
                self._logger.debug('*** No events found in "LIVE NOW" tab ***')
        else:
            inplay_live_stream = self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu.items_as_ordered_dict
            self.assertTrue(inplay_live_stream, msg='No switchers found for "INPLAY" and "LIVE STREAM" tabs')
            live_stream_tab = inplay_live_stream.get(vec.SB.LIVE_STREAM.upper())
            live_stream_tab.click()
            self.assertTrue(live_stream_tab.is_selected(),
                            msg=f'"{vec.SB.LIVE_STREAM.upper()}" tab is not selected')

    def test_003_click_on_each_sport_category(self):
        """
        DESCRIPTION: Click on each sport category
        EXPECTED: Mobile : User should be able to expand /collapse each sport category and each event.
        EXPECTED: Desktop : user can switch between sports from 'In-Play and Live Stream' carousal.
        """
        if self.device_type in ['mobile', 'tablet']:
            live_stream_sports_list = self.site.live_stream.tab_content.accordions_list.items_as_ordered_dict
            if live_stream_sports_list:
                live_stream_sports_list = self.site.live_stream.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(live_stream_sports_list, msg=f'No events found')
                for sport in live_stream_sports_list.keys():
                    if sport is not None:
                        live_stream_sports_list = self.site.live_stream.tab_content.accordions_list.items_as_ordered_dict
                        sport_section = live_stream_sports_list.get(sport)
                        sport_section.expand()
                        self.assertTrue(sport_section.is_expanded(),
                                        msg=f'Sport Section "{sport}" is not expanded')
                        sport_section.collapse()
                        self.assertFalse(sport_section.is_expanded(expected_result=False), msg=f'Section "{sport}" is '
                                                                                               f'not collapsed')
            else:
                self._logger.debug('*** No events found in "Live Stream" tab ***')
        else:
            self.__class__.inplay_live_stream_sports_list = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            if self.inplay_live_stream_sports_list:
                self.__class__.sports_with_events = []
                for sport in self.inplay_live_stream_sports_list.keys():
                    sport_carousal = self.inplay_live_stream_sports_list.get(sport)
                    sport_carousal.click()
                    self.assertTrue(sport_carousal.is_selected(),
                                    msg=f'"{sport}" sport carousal is not selected')
                    if sport_carousal.counter > 0:
                        self.sports_with_events.append(sport)
            else:
                self._logger.debug('*** No events found in "Live Stream" tab ***')

    def test_004_click_on_any_event(self, tab_name='IN-PLAY AND LIVE STREAM'):
        """
        DESCRIPTION: Click on any event
        EXPECTED: User should navigate to the corresponding Event Landing Page
        """
        if self.device_type in ['mobile', 'tablet']:
            live_stream_sports_list = self.site.live_stream.tab_content.accordions_list.items_as_ordered_dict
            if len(live_stream_sports_list) == 0:
                self._logger.debug('*** No events found in "Live Stream" tab ***')
            else:
                live_stream_sports_list = self.site.live_stream.tab_content.accordions_list.items_as_ordered_dict
                sports = list(live_stream_sports_list.keys())
                section = live_stream_sports_list.get(sports[0])
                self.site.contents.scroll_to_top()
                section.click()
        else:
            if len(self.inplay_live_stream_sports_list) > 0:
                sport_carousal = self.inplay_live_stream_sports_list.get(self.sports_with_events[0])
                sport_carousal.click()
                leagues = self.site.home.get_module_content(module_name=tab_name).accordions_list.items_as_ordered_dict
                self.assertTrue(leagues, msg='leagues are not displayed')
                section = leagues.get(list(leagues.keys())[0])
                section.expand()
                events = section.items_as_ordered_dict
                self.assertTrue(events, msg='No events were found')
                event_name = list(events.keys())[0]
                events.get(event_name).click()
            else:
                self._logger.debug('*** No events found in "Live Stream" tab ***')
        if self.device_type == 'mobile' and self.brand == 'bma':
            section.expand()
            events = section.items_as_ordered_dict
            self.assertTrue(events, msg='No events were found')
            event_name = list(events.keys())[0]
            events.get(event_name).click()
        try:
            self.__class__.event_on_details_page = self.site.sport_event_details
            self.assertEqual(self.event_on_details_page.event_name.upper(), event_name.upper(),
                             msg=f'Event name on details page "{self.event_on_details_page.event_name.upper()}" '
                                 f'does not match expected "{event_name.upper()}"')
        except VoltronException:
            self.site.wait_content_state('EventDetails', raise_exceptions=False, timeout=15)
        self.device.driver.implicitly_wait(3)
        try:
            self.assertTrue(self.site.sport_event_details.watch_live_button,
                            msg='"Watch Live" icon is not found')
            self.site.sport_event_details.watch_live_button.click()
            self.assertTrue(self.event_on_details_page.streaming,
                            msg=f'Live Streaming of the "{self.event_on_details_page.event_name.upper()}" is not available')
        except VoltronException:
            self.site.wait_content_state('EventDetails', raise_exceptions=False, timeout=15)

    def test_005_click_back(self):
        """
        DESCRIPTION: Click back
        EXPECTED: User should navigate back to LIVE STREAM tab
        """
        if self.brand == 'bma':
            self.device.go_back()
            self.device.driver.implicitly_wait(3)
            if self.device_type == 'mobile':
                self.site.wait_content_state('live-stream')
            else:
                self.site.wait_content_state('Homepage')

        if self.brand == 'ladbrokes':
            if self.device_type == 'mobile':
                self.device.go_back()
                self.site.wait_content_state_changed()
            else:
                self.event_on_details_page.back_button_click()
                self.site.wait_content_state('Homepage')

    def test_006_click_on_any_event_and_click_on_watch_icon_at_the_top(self):
        """
        DESCRIPTION: Click on any event and click on WATCH icon at the top
        EXPECTED: User should be able to watch Streaming of the event.
        """
        pass
        # covered in step 04

    def test_007_only_mobile__tablet__click_on_upcoming(self):
        """
        DESCRIPTION: Only mobile & Tablet : Click on 'UPCOMING'
        EXPECTED: Upcoming events are listed under this tab categorised by Sport type and sub-categorised by competition type.
        """
        if self.device_type in ['mobile', 'tablet']:
            self.site.contents.scroll_to()
            upcoming_tab = self.site.live_stream.upcoming_tab.text
            self.assertEqual(upcoming_tab, vec.inplay.UPCOMING_EVENTS_SECTION,
                             msg=f'Actual text: "{upcoming_tab}" is not same as'
                                 f'Expected text: "{vec.inplay.UPCOMING_EVENTS_SECTION}"')
            upcoming_sports_list = self.site.live_stream.upcoming.items_as_ordered_dict
            if upcoming_sports_list:
                upcoming_sports_list = self.site.live_stream.upcoming.items_as_ordered_dict
                self.assertTrue(upcoming_sports_list,
                                msg=f'No events found on "{vec.inplay.UPCOMING_EVENTS_SECTION}" tab')
            else:
                self._logger.debug('*** No events found in "UPCOMING EVENTS" tab ***')

    def test_008_only_mobile__table__repeat_steps_4_5(self):
        """
        DESCRIPTION: Only mobile & Table : repeat steps 4-5
        """
        if self.device_type in ['mobile', 'tablet']:
            self.test_004_click_on_any_event()
            self.test_005_click_back()
