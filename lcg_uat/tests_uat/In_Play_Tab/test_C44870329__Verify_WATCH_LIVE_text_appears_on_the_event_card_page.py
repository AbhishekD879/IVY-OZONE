import pytest
import voltron.environments.constants as vec
from tests.Common import Common
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.p3
@pytest.mark.in_play
@vtest
class Test_C44870329__Verify_WATCH_LIVE_text_appears_on_the_event_card_page(Common):
    """
    TR_ID: C44870329
    NAME: "-Verify WATCH LIVE' text appears on the event card page"
    DESCRIPTION: "-Verify Watching now' text appears on the event card when 'In-Play' switcher is selected for active streame
    DESCRIPTION: - Verify only stream applicable events are available on Watch page"
    DESCRIPTION: -This test case verifies "Watch live" page in In-Play sports ribbon
    PRECONDITIONS: Login to Oxygen app and navigate to "In-Play" tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app and navigate to "In-Play" tab
        EXPECTED: User is logged in and navigated to "In-Play" tab
        """
        self.site.login()
        if self.device_type == 'mobile':
            if self.brand == 'ladbrokes':
                inplay = vec.bma.IN_PLAY
            else:
                inplay = vec.bma.IN_PLAY.upper()
            self.site.home.menu_carousel.click_item(item_name=inplay)
            self.site.wait_content_state(state_name=inplay)

    def test_001_verify_displaying_of_watch_live_icon_in_play_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify displaying of "Watch Live" icon In-Play Sports Ribbon tab
        EXPECTED: "Watch Live" icon is displayed as the FIRST icon in the ribbon
        """
        if self.device_type == 'mobile':
            self.__class__.inplay_menu = self.site.inplay.inplay_sport_menu
            self.__class__.watch_live = self.inplay_menu.items_as_ordered_dict.get(vec.SB.WATCH_LIVE_LABEL)
            self.assertTrue(self.watch_live, msg=f'"{vec.SB.WATCH_LIVE_LABEL}" is not present')
            self.assertEqual(self.inplay_menu.items_names[0], vec.SB.WATCH_LIVE_LABEL,
                             msg=f'"{vec.SB.WATCH_LIVE_LABEL}" icon is not the first icon in the ribbon')

    def test_002_verify_default_users_navigation_after_in_play_tab_opening(self):
        """
        DESCRIPTION: Verify default user's navigation after In-Play tab opening
        EXPECTED: The user is landed on the FIRST sport in the ribbon by default (not the Watch Live tab)
        """
        if self.device_type == 'mobile':
            self.assertFalse(self.watch_live.is_selected(), msg=f'"{vec.SB.WATCH_LIVE_LABEL}" tab is selected by default')
            self.assertTrue(self.inplay_menu.items[1].is_selected(), msg='The first sport is not selected by default')

    def test_003_click_on_watch_live_iconverify_displaying_of_events_with_mapped_streams_in_inplay_and_upcoming_sections(self):
        """
        DESCRIPTION: Click on "Watch Live" icon
        DESCRIPTION: Verify displaying of events with mapped streams in Inplay and upcoming sections
        EXPECTED: "Watch Live" page is opened
        EXPECTED: Inplay and upcoming sections are displayed
        EXPECTED: Events which are not started are displayed in "Upcoming" section
        EXPECTED: Events without available stream are not displayed in "Watch live" page
        """
        if self.device_type == 'mobile':
            self.inplay_menu.click_item(item_name=vec.SB.WATCH_LIVE_LABEL)
            self.assertTrue(self.watch_live.is_selected(), msg=f'"{vec.SB.WATCH_LIVE_LABEL}" tab is selected')
            inplay_tab = self.site.inplay.tab_content
            self.assertTrue(inplay_tab.live_now.is_displayed(),
                            msg=f'"{vec.inplay.LIVE_NOW_SWITCHER}" is not present')
            self.assertTrue(inplay_tab.live_now_counter, msg='"live now counter" is not present')
            self.assertTrue(inplay_tab.upcoming.is_displayed(),
                            msg=f'"{vec.inplay.UPCOMING_SWITCHER}" is not present')
            self.assertTrue(inplay_tab.upcoming_counter, msg='"upcoming counter" is not present')
            live_now_sports = inplay_tab.live_now.items_as_ordered_dict
            for each_live_now_sport in live_now_sports.values():
                if not each_live_now_sport.is_expanded():
                    each_live_now_sport.expand()
                    for each_competition in each_live_now_sport.items_as_ordered_dict.values():
                        for each_event in each_competition.items:
                            if self.brand == 'bma':
                                self.assertEqual(each_event.watch_live_label, vec.SB.WATCH_LIVE_LABEL,
                                                 msg=f'The event "{each_event.name}" has no "{vec.SB.WATCH_LIVE_LABEL}" label')
                            else:
                                self.assertEqual(each_event.watch_live_label, vec.SB.WATCH.upper(),
                                                 msg=f'The event "{each_event.name}" has no "{vec.SB.WATCH.upper()}" label')
            upcoming_sports = inplay_tab.upcoming.items_as_ordered_dict
            for each_upcoming_sport in upcoming_sports.values():
                if not each_upcoming_sport.is_expanded():
                    each_upcoming_sport.expand()
                    for each_competition in each_upcoming_sport.items_as_ordered_dict.values():
                        for each_event in each_competition.items:
                            self.assertTrue(each_event.has_stream(),
                                            msg=f'The event "{each_event.name}" has no stream attached')

    def test_004_for_desktopgo_to_hp__in_play_and_live_stream_module_is_displayedverify_displaying_of_watch_live_icon_in_in_play_and_live_stream_ribbon(self):
        """
        DESCRIPTION: For Desktop:
        DESCRIPTION: Go to HP > "In-Play and Live Stream" module is displayed
        DESCRIPTION: Verify displaying of "Watch Live" icon in "In-Play and Live Stream" Ribbon
        EXPECTED: "Watch Live" icon is not displayed in "In-Play and Live Stream" Ribbon
        """
        if self.device_type == 'desktop':
            self.assertTrue(self.site.home.desktop_modules.inplay_live_stream_module.is_displayed(),
                            msg='"In-play and live stream" ribbon is not present on Homepage')
            watch_live = self.site.home.menu_carousel.items_as_ordered_dict.get(vec.SB.WATCH_LIVE_LABEL)
            self.assertFalse(watch_live, msg=f'"{vec.SB.WATCH_LIVE_LABEL}" is present in "In-Play and Live Stream" ribbon')
