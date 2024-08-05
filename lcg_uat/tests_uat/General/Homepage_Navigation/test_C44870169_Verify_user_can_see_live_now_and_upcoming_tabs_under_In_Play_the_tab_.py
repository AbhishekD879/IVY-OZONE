import pytest
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.p2
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870169_Verify_user_can_see_live_now_and_upcoming_tabs_under_In_Play_the_tab_(Common):
    """
    TR_ID: C44870169
    NAME: "Verify user can see  'live now' and 'upcoming' tabs under  In-Play the tab."
    DESCRIPTION: -This test case verifies 'Live Now' section on 'In-Play' page
    DESCRIPTION: -This test case verifies  'Upcoming' filter on 'In-Play Sports' page.
    PRECONDITIONS: 1.Load https://beta-sports.coral.co.uk/
    PRECONDITIONS: Navigate to 'In-Play' page from the Sports Menu Ribbon for mobile/tablet/Desktop
    PRECONDITIONS: Make sure that Live events are present in 'Live Now' section for mobile/tablet/ Desktop
    PRECONDITIONS: Make sure that upcoming events are present in 'upcoming' section for mobile/tablet/Desktop
    """
    keep_browser_open = True

    def verify_events_displayed_or_not(self, events):
        for event_name, event in events.items():
            self.assertTrue(event.is_displayed(),
                            msg=f'{event_name} is not displayed ')

    def test_001_load_httpsbeta_sportscoralcouk__log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Load https://beta-sports.coral.co.uk & log in with valid credentials.
        EXPECTED: App is loaded and user is on Home page
        """
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_002_for_mobiletabletnavigate_to_in_play_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: For Mobile/Tablet:
        DESCRIPTION: Navigate to 'In-Play' page from the Sports Menu Ribbon
        DESCRIPTION: For Desktop:
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: In-Play page is loaded with 'Live Now' section is displayed with top 4 events expanded in the list followed by 'UPCOMING EVENTS' on mobile.
        EXPECTED: For Desktop: The 'UPCOMING' switcher is available next to 'LIVE NOW'
        """
        comp_count = []
        if self.device_type in ['mobile', 'tablet']:
            self.site.open_sport(name=vec.inplay.BY_IN_PLAY, timeout=10)
            self.site.wait_content_state(state_name='In-Play')
            grouping_buttons = self.site.inplay.tab_content.items_as_ordered_dict
            self.assertTrue(grouping_buttons, msg='"In-play" tab contents are not available ')
            live_now = self.site.inplay.tab_content.live_now.items_as_ordered_dict
            self.assertTrue(live_now, msg='"Live Now" section is not loaded')
            accordion = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
            for each_event_name, each_event in list(accordion.items())[:4]:
                self.assertTrue(wait_for_result(lambda: each_event.is_expanded()),
                                msg=f'first sport "{each_event_name}" is not expanded by default')
                competitions = each_event.items
                for each_competition in competitions:
                    if len(comp_count) < 4:
                        comp_count.append(each_competition)
                self.assertTrue(each_event.is_expanded(), msg="first 4 events are not expanded by default")
            if self.brand == 'ladbrokes':
                self.assertTrue(grouping_buttons[vec.inplay.UPCOMING_EVENTS].is_displayed(),
                                msg='Upcoming events tab is not displayed')
            else:
                self.assertTrue(grouping_buttons[vec.inplay.UPCOMING_EVENTS_SECTION].is_displayed(),
                                msg='Upcoming events tab is not displayed')
        else:
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn('IN-PLAY', sports.keys(), msg='IN-PLAY is not found in the header sport menu')
            inplay = sports.get(vec.siteserve.IN_PLAY_TAB, None)
            self.assertTrue(inplay, msg='Can not get "IN-PLAY" sport tab')
            inplay.click()
            self.site.wait_content_state(state_name='In-Play')
            sports = list(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.keys())
            first_sport = list(sports)[1]
            is_selected = self.site.inplay.inplay_sport_menu.items_as_ordered_dict.get(first_sport).is_selected()
            self.assertTrue(is_selected, msg=f'"{first_sport}" tab is not selected by default')
            self.__class__.grouping_buttons = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict
            self.assertTrue(self.grouping_buttons[vec.inplay.LIVE_NOW_SWITCHER].is_selected(),
                            msg='"LIVE NOW" button is not Selected')
            self.assertTrue(self.grouping_buttons[vec.inplay.UPCOMING_SWITCHER].is_displayed(),
                            msg='"UPCOMING" button is not displayed ')
            competitions = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
            for comp_name, comp in list(competitions.items()):
                if len(comp_count) < 4:
                    comp_count.append(comp)
                    self.assertTrue(comp.is_expanded(), msg='First 4 events are not expanded by default')

    def test_003_choose_upcoming_switcher(self):
        """
        DESCRIPTION: Choose 'Upcoming' switcher
        EXPECTED: If there are no events in the filter:
        EXPECTED: "There are currently no upcoming Live events available" message is shown
        EXPECTED: If there are events in the filter: Events are loaded.
        """
        if self.device_type in ['mobile', 'tablet']:
            events = self.site.inplay.tab_content.upcoming.items_as_ordered_dict
        else:
            self.grouping_buttons[vec.inplay.UPCOMING_SWITCHER].click()
            self.assertTrue(self.grouping_buttons[vec.inplay.UPCOMING_SWITCHER].is_selected(),
                            msg='UPCOMING tab is not present')
            events = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        if len(events) != 0:
            self.assertTrue(events, msg='No Upcoming events are available')
        else:
            self._logger.info('*** No Upcoming events')

    def test_004_click_on_each_sport_icon_and_verify_all_the_live__upcoming_events_for_the_corresponding_sport__competition_are_displayed(self):
        """
        DESCRIPTION: Click on each Sport icon and verify All the live & upcoming events for the corresponding sport / competition are displayed.
        EXPECTED: All the live & upcoming events for the corresponding sport / competition are displayed.
        """
        sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        for each_sport in range(len(sports)):
            sports = list(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.values())
            sports[each_sport].click()
            if self.device_type in ['mobile', 'tablet']:
                live_now = self.site.inplay.tab_content.live_now.items_as_ordered_dict
                self.verify_events_displayed_or_not(live_now)
                upcoming = self.site.inplay.tab_content.upcoming.items_as_ordered_dict
                self.verify_events_displayed_or_not(upcoming)
            else:
                grouping_buttons = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict
                for switcher, button in grouping_buttons.items():
                    button.click()
                    events = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
                    self.verify_events_displayed_or_not(events)
